"""
schemas.py — Pydantic request/response DTOs.
FastAPI uses these to validate incoming JSON and serialize outgoing JSON.
'orm_mode = True' (or 'from_attributes = True' in Pydantic v2) lets Pydantic
read data directly from SQLAlchemy model instances instead of plain dicts.
"""

from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr  # type: ignore


# ---------------------------------------------------------------------------
# Shared config mixin — enables ORM mode for all response schemas
# ---------------------------------------------------------------------------
class ORMBase(BaseModel):
    class Config:
        from_attributes = True   # Pydantic v2 equivalent of orm_mode


# ===========================================================================
# USER
# ===========================================================================

class UserCreate(BaseModel):
    """Body for creating a new user (POST /onboard or seed)."""
    name:  str
    email: EmailStr


class UserOut(ORMBase):
    """Returned whenever user data is included in a response."""
    id:           int
    name:         str
    email:        str
    goal:         Optional[str]
    goal_target_amount: Optional[float]
    kyc_verified: bool
    created_at:   datetime


class GoalRecord(ORMBase):
    """Stored investment goal for a user."""
    id:            int
    user_id:       int
    goal:          str
    target_amount: Optional[float]
    created_at:    datetime
    updated_at:    Optional[datetime]


class GoalList(ORMBase):
    """All stored investment goals for a user."""
    user_id: int
    goals:   List[GoalRecord]


class DashboardOut(ORMBase):
    """Aggregated data for the frontend landing page and live dashboard cards."""
    user_id:                int
    name:                   str
    goal:                   Optional[str]
    goal_target_amount:     Optional[float]
    kyc_verified:           bool
    kyc_status:             str
    balance:                float
    total_invested:         float
    market_value:           float
    total_xp:               int
    level:                  int
    current_streak:         int
    longest_streak:         int
    active_rewards:         int
    habits_today_completed: int
    habits_total:           int
    roundup_total:          float
    updated_at:             Optional[datetime]


# ===========================================================================
# ONBOARDING
# ===========================================================================

class GoalSet(BaseModel):
    """Body for POST /onboard/goal — user picks their investment goal."""
    user_id: int
    # e.g. "emergency_fund", "vacation", "first_home", "retirement"
    goal:    str
    target_amount: Optional[float] = None


class GoalOut(ORMBase):
    """Confirmation response after goal is saved."""
    user_id: int
    goal:    str
    target_amount: Optional[float] = None
    message: str


class GoalUpsert(BaseModel):
    """Body for PUT /goals/{user_id} — update the user's current goal."""
    goal:          str
    target_amount: Optional[float] = None


class DepositCreate(BaseModel):
    """Body for POST /onboard/deposit — user makes their first deposit."""
    user_id: int
    amount:  float   # in CAD dollars


class DepositOut(ORMBase):
    """Response after a deposit is processed."""
    transaction_id: int
    user_id:        int
    amount:         float
    new_balance:    float
    xp_earned:      int
    message:        str


class KYCStatus(ORMBase):
    """Response for GET /onboard/kyc-status/{userId}."""
    user_id:      int
    kyc_verified: bool
    # Human-readable status string for the frontend badge
    status:       str   # "Verified" | "Pending" | "Not Started"


# ===========================================================================
# XP
# ===========================================================================

class XPEventCreate(BaseModel):
    """Body for POST /xp/event — manually log an XP-earning action."""
    user_id:    int
    event_type: str    # "habit", "deposit", "streak", "reward"
    points:     int
    label:      Optional[str] = None


class XPEventOut(ORMBase):
    """One entry in the XP activity history feed."""
    id:         int
    event_type: str
    points:     int
    label:      Optional[str]
    created_at: datetime


class XPSummary(ORMBase):
    """
    Response for GET /xp/{userId}.
    Includes total XP calculated by summing all XPEvent rows for this user,
    plus the full history list so the frontend can render a feed.
    """
    user_id:     int
    total_xp:    int
    level:       int          # derived: total_xp // 100
    history:     List[XPEventOut]


# ===========================================================================
# ROUNDUPS
# ===========================================================================

class RoundupProcess(BaseModel):
    """
    Body for POST /roundups/process.
    The frontend sends the raw purchase amount; the backend rounds it up
    to the next whole dollar and invests the difference.
    Example: amount=4.35 → roundup=0.65
    """
    user_id: int
    amount:  float   # raw transaction amount, e.g. 4.35


class RoundupOut(ORMBase):
    """Response after a roundup is processed and invested."""
    user_id:       int
    original:      float   # the raw amount sent in
    roundup:       float   # the cents rounded up, e.g. 0.65
    new_balance:   float   # portfolio balance after roundup is added
    xp_earned:     int
    transaction_id: int


class RoundupHistoryItem(ORMBase):
    """One roundup entry for the history list."""
    id:          int
    amount:      float
    description: Optional[str]
    created_at:  datetime


class RoundupHistory(ORMBase):
    """Response for GET /roundups/{userId}."""
    user_id:  int
    roundups: List[RoundupHistoryItem]
    total_rounded_up: float   # running sum of all roundup amounts


# ===========================================================================
# REWARDS
# ===========================================================================

class RewardOut(ORMBase):
    """One reward from the catalog (GET /rewards/{userId})."""
    id:          int
    name:        str
    description: Optional[str]
    xp_cost:     int
    category:    Optional[str]
    is_active:   bool
    # Whether the current user has already redeemed this reward
    redeemed:    bool


class RewardCatalog(ORMBase):
    """Full response for GET /rewards/{userId}."""
    user_id:  int
    total_xp: int          # so the frontend can show "you have X XP"
    rewards:  List[RewardOut]


class RedeemOut(BaseModel):
    """Confirmation response after POST /rewards/{rewardId}/redeem."""
    user_id:        int
    reward_id:      int
    reward_name:    str
    xp_spent:       int
    remaining_xp:   int
    message:        str


# ===========================================================================
# HABITS
# ===========================================================================

class HabitOut(ORMBase):
    """
    One habit in today's list (GET /habits/today/{userId}).
    'completed_today' is computed in the router by checking HabitCompletion
    rows for today's date — it is NOT stored directly on the Habit model.
    """
    id:              int
    name:            str
    description:     Optional[str]
    xp_reward:       int
    frequency:       str
    completed_today: bool


class HabitListOut(ORMBase):
    """Full response for GET /habits/today/{userId}."""
    user_id:         int
    date:            str            # ISO date string, e.g. "2025-06-01"
    habits:          List[HabitOut]
    completed_count: int
    total_count:     int


class HabitCompleteOut(BaseModel):
    """Response after POST /habits/{habitId}/complete/{userId}."""
    user_id:        int
    habit_id:       int
    habit_name:     str
    xp_earned:      int
    new_streak:     int
    total_xp:       int
    message:        str
