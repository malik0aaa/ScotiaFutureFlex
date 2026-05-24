"""
routers/roundups.py — Spare-change investing via ceiling roundups.

Endpoints:
  POST /roundups/process      — compute roundup, invest it, award XP
  GET  /roundups/{userId}     — full roundup history + running total
"""

import math
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

import models
import schemas
from database import get_db
from routers.xp import get_total_xp   # reuse the shared XP helper

router = APIRouter(prefix="/roundups", tags=["Roundups"])


# ---------------------------------------------------------------------------
# POST /roundups/process
# ---------------------------------------------------------------------------
@router.post("/process", response_model=schemas.RoundupOut)
def process_roundup(body: schemas.RoundupProcess, db: Session = Depends(get_db)):
    """
    Core product feature: round a purchase amount UP to the next whole dollar
    and invest the difference automatically.

    Math example:
      amount = 4.35
      ceil(4.35) = 5
      roundup = 5 - 4.35 = 0.65  ← this gets invested

    Edge case:
      amount = 7.00
      ceil(7.00) = 7
      roundup = 0.00  ← nothing to invest, return early
    """
    if body.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    # --- Ceiling math ---
    # round(..., 2) strips floating-point drift (e.g. 0.6499999... → 0.65)
    roundup = round(math.ceil(body.amount) - body.amount, 2)

    # If the purchase was already a whole dollar, nothing to invest
    if roundup == 0.0:
        raise HTTPException(
            status_code=400,
            detail=f"Amount ${body.amount:.2f} is already a whole dollar — no roundup needed."
        )

    # --- Fetch user ---
    user = db.query(models.User).filter(models.User.id == body.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # --- KYC guard: user must be verified before any money moves ---
    if not user.kyc_verified:
        raise HTTPException(
            status_code=403,
            detail="KYC verification required before investing roundups. "
                   "Please complete identity verification first.",
        )

    # --- Fetch portfolio ---
    portfolio = db.query(models.Portfolio).filter(
        models.Portfolio.user_id == body.user_id
    ).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found. Complete onboarding first.")

    # --- Record the roundup as a Transaction ---
    transaction = models.Transaction(
        portfolio_id=portfolio.id,
        type="roundup",
        amount=roundup,
        # Description shown in the transaction feed on the frontend
        description=f"Roundup: ${body.amount:.2f} → ${math.ceil(body.amount):.2f}",
    )
    db.add(transaction)

    # --- Update portfolio balance ---
    # The roundup amount is added to balance (uninvested cash)
    # and also counted toward total_invested immediately
    portfolio.balance        = round(portfolio.balance + roundup, 2)
    portfolio.total_invested = round(portfolio.total_invested + roundup, 2)
    # Recalculate simulated market value (5.75% growth factor)
    portfolio.market_value   = round(portfolio.total_invested * 1.0575, 2)

    # --- Award XP for the roundup ---
    # If this is the very first investment EVER (no prior deposits or roundups),
    # award a 100 XP "first investment" bonus instead of the standard 5 XP.
    prior_investments = db.query(models.Transaction).filter(
        models.Transaction.portfolio_id == portfolio.id,
        models.Transaction.type.in_(["deposit", "roundup"]),
    ).count()

    # prior_investments will be 1 at this point because we already added the
    # current roundup transaction above (db.add but not yet committed).
    # So count == 1 means this is the first ever investment.
    if prior_investments <= 1:
        xp_earned = 100
        xp_label  = "First investment bonus — roundup!"
    else:
        xp_earned = 5
        xp_label  = f"Roundup invested: ${roundup:.2f}"

    xp_event = models.XPEvent(
        user_id=body.user_id,
        event_type="roundup",
        points=xp_earned,
        label=xp_label,
    )
    db.add(xp_event)

    db.commit()
    db.refresh(transaction)

    return schemas.RoundupOut(
        user_id=body.user_id,
        original=body.amount,
        roundup=roundup,
        new_balance=portfolio.balance,
        xp_earned=xp_earned,
        transaction_id=transaction.id,
    )


# ---------------------------------------------------------------------------
# GET /roundups/{user_id}
# ---------------------------------------------------------------------------
@router.get("/{user_id}", response_model=schemas.RoundupHistory)
def get_roundup_history(user_id: int, db: Session = Depends(get_db)):
    """
    Return all roundup transactions for a user plus a running total.
    The frontend uses this to display the 'Spare Change Invested' card
    showing how much the user has saved without even thinking about it.
    """
    # Confirm user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch the user's portfolio to scope transactions correctly
    portfolio = db.query(models.Portfolio).filter(
        models.Portfolio.user_id == user_id
    ).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    # --- Fetch all roundup transactions, newest first ---
    roundup_rows = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.portfolio_id == portfolio.id,
            models.Transaction.type == "roundup",
        )
        .order_by(models.Transaction.created_at.desc())
        .all()
    )

    # --- Compute running total with SQL SUM (faster than Python sum) ---
    total = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.portfolio_id == portfolio.id,
        models.Transaction.type == "roundup",
    ).scalar()
    total_rounded_up = round(float(total), 2) if total else 0.0

    # Convert ORM rows → Pydantic schemas
    roundups = [schemas.RoundupHistoryItem.model_validate(row) for row in roundup_rows]

    return schemas.RoundupHistory(
        user_id=user_id,
        roundups=roundups,
        total_rounded_up=total_rounded_up,
    )
