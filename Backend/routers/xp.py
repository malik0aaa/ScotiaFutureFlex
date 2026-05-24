"""
routers/xp.py — XP (Experience Points) engine.

Endpoints:
  GET  /xp/{userId}  — fetch total XP, computed level, and full event history
  POST /xp/event     — log any new XP-earning (or XP-spending) action
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

import models
import schemas
from database import get_db

router = APIRouter(prefix="/xp", tags=["XP"])


# ---------------------------------------------------------------------------
# Helper — compute total XP for a user
# Used by both endpoints in this file and importable by other routers
# ---------------------------------------------------------------------------
def get_total_xp(user_id: int, db: Session) -> int:
    """
    Sum all XPEvent.points rows for this user.
    Points can be negative (e.g. reward redemptions), so we use SQL SUM
    rather than counting rows.
    Returns 0 if the user has no events yet.
    """
    result = db.query(func.sum(models.XPEvent.points)).filter(
        models.XPEvent.user_id == user_id
    ).scalar()

    # scalar() returns None if there are no rows — coerce to 0
    return int(result) if result is not None else 0


# ---------------------------------------------------------------------------
# GET /xp/{user_id}
# ---------------------------------------------------------------------------
@router.get("/{user_id}", response_model=schemas.XPSummary)
def get_xp_summary(user_id: int, db: Session = Depends(get_db)):
    """
    Return the full XP picture for a user:
      - total_xp  : sum of all XPEvent.points (deposits, habits, streaks, -redemptions)
      - level     : total_xp // 100  (level 1 @ 100 XP, level 6 @ 620 XP, etc.)
      - history   : all XPEvent rows, newest first, for the activity feed
    """
    # Confirm the user exists before doing anything else
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # --- Total XP (SQL SUM is faster than loading every row into Python) ---
    total_xp = get_total_xp(user_id, db)

    # --- Level: one level per 100 XP, starting at level 0 ---
    # level 0 = 0–99 XP  |  level 1 = 100–199 XP  |  level 6 = 600–699 XP
    level = total_xp // 100

    # --- History: all events, newest first ---
    history_rows = (
        db.query(models.XPEvent)
        .filter(models.XPEvent.user_id == user_id)
        .order_by(models.XPEvent.created_at.desc())
        .all()
    )

    # Convert ORM rows → Pydantic schemas (from_attributes handles the mapping)
    history = [schemas.XPEventOut.model_validate(row) for row in history_rows]

    return schemas.XPSummary(
        user_id=user_id,
        total_xp=total_xp,
        level=level,
        history=history,
    )


# ---------------------------------------------------------------------------
# POST /xp/event
# ---------------------------------------------------------------------------
@router.post("/event", response_model=schemas.XPEventOut)
def log_xp_event(body: schemas.XPEventCreate, db: Session = Depends(get_db)):
    """
    Log a new XP event for any action type.
    This endpoint is a generic hook — called directly by the frontend for
    one-off actions, or internally by other routers (habits, roundups, rewards)
    that need to record XP without duplicating the insert logic.

    Positive points = XP earned.
    Negative points = XP spent (e.g. reward redemption recorded separately
    here for the activity feed).
    """
    # Confirm the user exists
    user = db.query(models.User).filter(models.User.id == body.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate points — 0 XP events are meaningless
    if body.points == 0:
        raise HTTPException(status_code=400, detail="Points cannot be zero")

    # Build and persist the event row
    event = models.XPEvent(
        user_id=body.user_id,
        event_type=body.event_type,
        points=body.points,
        label=body.label,
    )
    db.add(event)
    db.commit()
    db.refresh(event)  # reload to get server-set created_at timestamp

    return schemas.XPEventOut.model_validate(event)
