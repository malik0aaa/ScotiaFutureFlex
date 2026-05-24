"""
routers/habits.py — Daily habit tracking and streak management.

Endpoints:
  GET  /habits/today/{userId}              — today's habits with completion status
  POST /habits/{habitId}/complete/{userId} — mark a habit done, update streak, award XP
"""

from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from routers.xp import get_total_xp   # shared XP helper

router = APIRouter(prefix="/habits", tags=["Habits"])


# ---------------------------------------------------------------------------
# Helper — check if a habit was already completed today by this user
# ---------------------------------------------------------------------------
def _completed_today(habit_id: int, user_id: int, db: Session) -> bool:
    """
    Return True if there is at least one HabitCompletion row for this
    habit + user combination where completed_at falls on today's UTC date.
    """
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end   = today_start + timedelta(days=1)

    match = db.query(models.HabitCompletion).filter(
        models.HabitCompletion.habit_id == habit_id,
        models.HabitCompletion.user_id  == user_id,
        models.HabitCompletion.completed_at >= today_start,
        models.HabitCompletion.completed_at <  today_end,
    ).first()

    return match is not None


# ---------------------------------------------------------------------------
# GET /habits/today/{user_id}
# ---------------------------------------------------------------------------
@router.get("/today/{user_id}", response_model=schemas.HabitListOut)
def get_today_habits(user_id: int, db: Session = Depends(get_db)):
    """
    Return all active habits for today, each annotated with whether
    the user has already completed it today.

    The frontend uses completed_count / total_count to render the
    circular progress ring on the habits card.
    """
    # --- Confirm user exists ---
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # --- Fetch all active habits ---
    habits = (
        db.query(models.Habit)
        .filter(models.Habit.is_active == True)
        .order_by(models.Habit.id.asc())
        .all()
    )

    # --- Annotate each habit with today's completion status ---
    habit_list = []
    completed_count = 0

    for habit in habits:
        done = _completed_today(habit.id, user_id, db)
        if done:
            completed_count += 1

        habit_list.append(
            schemas.HabitOut(
                id=habit.id,
                name=habit.name,
                description=habit.description,
                xp_reward=habit.xp_reward,
                frequency=habit.frequency,
                completed_today=done,
            )
        )

    return schemas.HabitListOut(
        user_id=user_id,
        date=date.today().isoformat(),   # e.g. "2025-06-01"
        habits=habit_list,
        completed_count=completed_count,
        total_count=len(habit_list),
    )


# ---------------------------------------------------------------------------
# POST /habits/{habit_id}/complete/{user_id}
# ---------------------------------------------------------------------------
@router.post("/{habit_id}/complete/{user_id}", response_model=schemas.HabitCompleteOut)
def complete_habit(habit_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Mark a habit as completed for today. Steps:
      1. Validate habit and user exist.
      2. Prevent duplicate completions on the same day.
      3. Log a HabitCompletion row.
      4. Award XP and log an XPEvent.
      5. Update the streak (extend, maintain, or reset).
      6. Update longest_streak if current_streak beats it.
      7. Return new streak count and updated total XP.
    """

    # --- Guard: habit exists and is active ---
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    if not habit.is_active:
        raise HTTPException(status_code=400, detail="This habit is no longer active")

    # --- Guard: user exists ---
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # --- Guard: not already completed today ---
    if _completed_today(habit_id, user_id, db):
        raise HTTPException(
            status_code=400,
            detail=f"'{habit.name}' already completed today. Come back tomorrow!",
        )

    # --- 3. Log the completion ---
    completion = models.HabitCompletion(
        habit_id=habit_id,
        user_id=user_id,
        completed_at=datetime.utcnow(),
    )
    db.add(completion)

    # --- 4. Award XP ---
    xp_event = models.XPEvent(
        user_id=user_id,
        event_type="habit",
        points=habit.xp_reward,
        label=f"Completed: {habit.name}",
    )
    db.add(xp_event)

    # --- 5. Update streak ---
    streak = db.query(models.Streak).filter(models.Streak.user_id == user_id).first()

    if not streak:
        # First time this user has ever completed a habit — create streak record
        streak = models.Streak(
            user_id=user_id,
            current_streak=1,
            longest_streak=1,
            last_active=datetime.utcnow(),
        )
        db.add(streak)
    else:
        today = date.today()

        if streak.last_active is None:
            # No previous activity recorded — start at 1
            streak.current_streak = 1

        else:
            last_active_date = streak.last_active.date()

            if last_active_date == today:
                # User already completed a DIFFERENT habit earlier today —
                # streak count doesn't change, we're still on the same day
                pass

            elif last_active_date == today - timedelta(days=1):
                # User was active yesterday — perfect streak, extend it
                streak.current_streak += 1

            else:
                # Gap of 2+ days — streak is broken, reset to 1
                streak.current_streak = 1

        # Always update last_active to now
        streak.last_active = datetime.utcnow()

        # --- 6. Update longest streak if beaten ---
        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak

        # Bonus XP milestone: award extra 50 XP on 7-day streak
        if streak.current_streak == 7:
            milestone_event = models.XPEvent(
                user_id=user_id,
                event_type="streak",
                points=50,
                label="🔥 7-day streak bonus!",
            )
            db.add(milestone_event)

        # Bonus XP milestone: award extra 100 XP on 30-day streak
        elif streak.current_streak == 30:
            milestone_event = models.XPEvent(
                user_id=user_id,
                event_type="streak",
                points=100,
                label="🏆 30-day streak bonus!",
            )
            db.add(milestone_event)

    db.commit()

    # --- 7. Return updated totals ---
    # Recalculate total XP after the new event(s) are committed
    total_xp = get_total_xp(user_id, db)

    return schemas.HabitCompleteOut(
        user_id=user_id,
        habit_id=habit_id,
        habit_name=habit.name,
        xp_earned=habit.xp_reward,
        new_streak=streak.current_streak,
        total_xp=total_xp,
        message=(
            f"'{habit.name}' completed! +{habit.xp_reward} XP. "
            f"🔥 {streak.current_streak}-day streak!"
        ),
    )
