"""
routers/rewards.py — XP rewards marketplace.

Endpoints:
  GET  /rewards/{userId}            — full catalog with per-user redemption status
  POST /rewards/{rewardId}/redeem   — spend XP to unlock a reward
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from routers.xp import get_total_xp   # shared helper: SQL SUM of XPEvent.points

router = APIRouter(prefix="/rewards", tags=["Rewards"])


# ---------------------------------------------------------------------------
# GET /rewards/{user_id}
# ---------------------------------------------------------------------------
@router.get("/{user_id}", response_model=schemas.RewardCatalog)
def get_rewards(user_id: int, db: Session = Depends(get_db)):
    """
    Return every active reward in the catalog together with:
      - The user's current total XP (so the frontend can show affordability)
      - A 'redeemed' flag on each reward (True if this user has already claimed it)

    The frontend uses this to grey out rewards the user can't afford or
    has already redeemed, and to highlight ones within reach.
    """
    # --- Confirm user exists ---
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # --- Get user's current XP balance ---
    total_xp = get_total_xp(user_id, db)

    # --- Fetch all active rewards from the catalog ---
    all_rewards = (
        db.query(models.Reward)
        .filter(models.Reward.is_active == True)
        .order_by(models.Reward.xp_cost.asc())   # cheapest first
        .all()
    )

    # --- Build set of reward IDs this user has already redeemed ---
    # Using a set gives O(1) lookup when iterating rewards below
    redeemed_ids = set(
        row.reward_id
        for row in db.query(models.UserReward.reward_id)
        .filter(models.UserReward.user_id == user_id)
        .all()
    )

    # --- Build response list with per-user 'redeemed' flag ---
    reward_list = []
    for reward in all_rewards:
        reward_list.append(
            schemas.RewardOut(
                id=reward.id,
                name=reward.name,
                description=reward.description,
                xp_cost=reward.xp_cost,
                category=reward.category,
                is_active=reward.is_active,
                # True if this user has already redeemed this specific reward
                redeemed=reward.id in redeemed_ids,
            )
        )

    return schemas.RewardCatalog(
        user_id=user_id,
        total_xp=total_xp,
        rewards=reward_list,
    )


# ---------------------------------------------------------------------------
# POST /rewards/{reward_id}/redeem
# ---------------------------------------------------------------------------
@router.post("/{reward_id}/redeem", response_model=schemas.RedeemOut)
def redeem_reward(
    reward_id: int,
    user_id: int,           # passed as a query param: /rewards/2/redeem?user_id=1
    db: Session = Depends(get_db),
):
    """
    Spend XP to redeem a reward. Four guard rails run in order:
      1. Reward must exist and be active
      2. User must exist
      3. User must not have already redeemed this reward
      4. User must have enough XP to cover the cost

    On success:
      - Creates a UserReward row (permanent record of redemption)
      - Logs a NEGATIVE XPEvent so the activity feed shows the deduction
      - Returns remaining XP so the frontend can update the XP bar instantly
    """

    # --- Guard 1: reward exists and is active ---
    reward = db.query(models.Reward).filter(models.Reward.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    if not reward.is_active:
        raise HTTPException(status_code=400, detail="This reward is no longer available")

    # --- Guard 2: user exists ---
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # --- Guard 3: not already redeemed ---
    already_redeemed = db.query(models.UserReward).filter(
        models.UserReward.user_id == user_id,
        models.UserReward.reward_id == reward_id,
    ).first()
    if already_redeemed:
        raise HTTPException(
            status_code=400,
            detail=f"You have already redeemed '{reward.name}'",
        )

    # --- Guard 4: sufficient XP ---
    total_xp = get_total_xp(user_id, db)
    if total_xp < reward.xp_cost:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Insufficient XP. You have {total_xp} XP but "
                f"'{reward.name}' costs {reward.xp_cost} XP."
            ),
        )

    # --- All guards passed — process the redemption ---

    # 1. Record the redemption in the UserReward junction table
    user_reward = models.UserReward(
        user_id=user_id,
        reward_id=reward_id,
        xp_spent=reward.xp_cost,   # snapshot cost at time of redemption
    )
    db.add(user_reward)

    # 2. Deduct XP by logging a NEGATIVE XP event
    #    This keeps the ledger accurate without a separate "balance" column
    deduction_event = models.XPEvent(
        user_id=user_id,
        event_type="reward",
        points=-reward.xp_cost,    # negative = XP spent
        label=f"Redeemed: {reward.name}",
    )
    db.add(deduction_event)

    db.commit()

    # Recalculate remaining XP after the deduction
    remaining_xp = get_total_xp(user_id, db)

    return schemas.RedeemOut(
        user_id=user_id,
        reward_id=reward_id,
        reward_name=reward.name,
        xp_spent=reward.xp_cost,
        remaining_xp=remaining_xp,
        message=f"'{reward.name}' redeemed successfully! {remaining_xp} XP remaining.",
    )
