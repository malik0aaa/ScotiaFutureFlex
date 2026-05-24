"""
routers/goals.py — Dedicated investment goals API.

Endpoints:
    GET /goals/{user_id}      — fetch the user's latest stored goal
    POST /goals/{user_id}     — add a new goal row for the user
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/goals", tags=["Goals"])


def _sync_user_goal_fields(user: models.User, goal_row: models.InvestmentGoal | None) -> models.User:
    if goal_row:
        user.goal = goal_row.goal
        user.goal_target_amount = goal_row.target_amount
    else:
        user.goal = user.goal
        user.goal_target_amount = user.goal_target_amount
    return user


@router.get("/{user_id}", response_model=schemas.GoalRecord)
def get_goal(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    goal_row = db.query(models.InvestmentGoal).filter(models.InvestmentGoal.user_id == user_id).order_by(
        models.InvestmentGoal.created_at.desc(),
        models.InvestmentGoal.id.desc(),
    ).first()
    if not goal_row:
        raise HTTPException(status_code=404, detail="Goal not found")

    _sync_user_goal_fields(user, goal_row)
    return goal_row


@router.get("/{user_id}/all", response_model=schemas.GoalList)
def get_goals(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    goals = db.query(models.InvestmentGoal).filter(models.InvestmentGoal.user_id == user_id).order_by(
        models.InvestmentGoal.created_at.desc(),
        models.InvestmentGoal.id.desc(),
    ).all()

    latest_goal = goals[0] if goals else None
    _sync_user_goal_fields(user, latest_goal)
    return schemas.GoalList(user_id=user_id, goals=goals)


@router.post("/{user_id}", response_model=schemas.GoalOut)
def add_goal(user_id: int, body: schemas.GoalUpsert, db: Session = Depends(get_db)):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    goal_row = models.InvestmentGoal(
        user_id=user_id,
        goal=body.goal,
        target_amount=body.target_amount,
    )
    db.add(goal_row)

    # Keep legacy user fields in sync so existing screens remain functional.
    user.goal = body.goal
    user.goal_target_amount = body.target_amount

    db.commit()
    db.refresh(goal_row)

    return schemas.GoalOut(
        user_id=user_id,
        goal=goal_row.goal,
        target_amount=goal_row.target_amount,
        message=f"Goal set to '{goal_row.goal}'. Let's start building your future!",
    )