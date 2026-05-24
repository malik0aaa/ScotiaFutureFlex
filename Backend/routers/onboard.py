"""
routers/onboard.py — First-time user setup flow.

Endpoints:
  POST /onboard/goal              — save user's investment goal
  POST /onboard/deposit           — process first deposit, award XP
  GET  /onboard/kyc-status/{userId} — return KYC verification status
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

# All routes in this file are prefixed with /onboard automatically
# when this router is registered in main.py
router = APIRouter(prefix="/onboard", tags=["Onboarding"])


# ---------------------------------------------------------------------------
# POST /onboard/goal
# ---------------------------------------------------------------------------
@router.post("/goal", response_model=schemas.GoalOut)
def set_goal(body: schemas.GoalSet, db: Session = Depends(get_db)):
    """
    Save the user's investment goal chosen during onboarding.
    The goal is a short string key: 'first_home', 'vacation',
    'emergency_fund', or 'retirement'.
    """
    # Look up the user — 404 if they don't exist
    user = db.query(models.User).filter(models.User.id == body.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    goal_row = models.InvestmentGoal(
        user_id=body.user_id,
        goal=body.goal,
        target_amount=body.target_amount,
    )
    db.add(goal_row)

    # Persist the chosen goal on the user record for legacy screens.
    user.goal = body.goal
    user.goal_target_amount = body.target_amount
    db.commit()
    db.refresh(goal_row)

    return schemas.GoalOut(
        user_id=user.id,
        goal=goal_row.goal,
        target_amount=goal_row.target_amount,
        message=f"Goal set to '{goal_row.goal}'. Let's start building your future!",
    )


# ---------------------------------------------------------------------------
# POST /onboard/deposit
# ---------------------------------------------------------------------------
@router.post("/deposit", response_model=schemas.DepositOut)
def make_deposit(body: schemas.DepositCreate, db: Session = Depends(get_db)):
    """
    Process a deposit:
      1. Validate the user and their portfolio exist.
      2. Add a Transaction row of type 'deposit'.
      3. Increase portfolio.balance by the deposit amount.
      4. Award 50 XP (100 XP if this is the very first deposit).
      5. Log an XPEvent so the activity feed stays up to date.
    """
    if body.amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")

    # --- Fetch user ---
    user = db.query(models.User).filter(models.User.id == body.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # --- KYC guard: user must be verified before any money moves ---
    if not user.kyc_verified:
        raise HTTPException(
            status_code=403,
            detail="KYC verification required before making a deposit. "
                   "Please complete identity verification first.",
        )

    # --- Fetch or create portfolio ---
    # A portfolio should exist from onboarding, but we create one defensively
    portfolio = db.query(models.Portfolio).filter(
        models.Portfolio.user_id == body.user_id
    ).first()

    if not portfolio:
        portfolio = models.Portfolio(user_id=body.user_id, balance=0.0,
                                     total_invested=0.0, market_value=0.0)
        db.add(portfolio)
        db.flush()   # get portfolio.id before using it below

    # --- Determine XP reward ---
    # First-ever deposit earns a 100 XP bonus; subsequent deposits earn 50 XP
    existing_deposits = db.query(models.Transaction).filter(
        models.Transaction.portfolio_id == portfolio.id,
        models.Transaction.type == "deposit",
    ).count()
    xp_earned = 100 if existing_deposits == 0 else 50

    # --- Record the transaction ---
    transaction = models.Transaction(
        portfolio_id=portfolio.id,
        type="deposit",
        amount=body.amount,
        description=f"Deposit of ${body.amount:.2f}",
    )
    db.add(transaction)

    # --- Update portfolio balance ---
    portfolio.balance += body.amount
    portfolio.total_invested += body.amount
    # Simulate a 5.75% growth on total invested for market_value display
    portfolio.market_value = round(portfolio.total_invested * 1.0575, 2)

    # --- Log the XP event ---
    xp_event = models.XPEvent(
        user_id=body.user_id,
        event_type="deposit",
        points=xp_earned,
        label=f"Deposit bonus — ${body.amount:.2f}",
    )
    db.add(xp_event)

    db.commit()
    db.refresh(transaction)

    return schemas.DepositOut(
        transaction_id=transaction.id,
        user_id=body.user_id,
        amount=body.amount,
        new_balance=round(portfolio.balance, 2),
        xp_earned=xp_earned,
        message=f"Deposit successful! You earned {xp_earned} XP.",
    )


# ---------------------------------------------------------------------------
# GET /onboard/kyc-status/{userId}
# ---------------------------------------------------------------------------
@router.get("/kyc-status/{user_id}", response_model=schemas.KYCStatus)
def get_kyc_status(user_id: int, db: Session = Depends(get_db)):
    """
    Return the KYC (Know Your Customer) verification status for a user.
    In a real Scotiabank integration this would call an identity-verification
    service; here we read the kyc_verified flag set during onboarding/seeding.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Map the boolean flag to a human-readable label for the frontend badge
    if user.kyc_verified:
        status_label = "Verified"
    else:
        # Could extend this to "Pending" if a KYC submission is in progress
        status_label = "Not Started"

    return schemas.KYCStatus(
        user_id=user.id,
        kyc_verified=user.kyc_verified,
        status=status_label,
    )
