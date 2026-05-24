"""
models.py — All 9 SQLAlchemy ORM models.
Each class = one database table. Relationships are declared so SQLAlchemy
can JOIN tables automatically when you access related objects.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


# ---------------------------------------------------------------------------
# 1. User
# ---------------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String, nullable=False)
    email         = Column(String, unique=True, index=True, nullable=False)
    # Investment goal chosen during onboarding: e.g. "emergency_fund", "vacation"
    goal          = Column(String, nullable=True)
    # KYC = Know Your Customer. True once the user has passed identity checks.
    kyc_verified  = Column(Boolean, default=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())

    # One user → one portfolio (uselist=False turns it into a scalar, not a list)
    portfolio     = relationship("Portfolio", back_populates="owner", uselist=False)
    # One user → many XP events
    xp_events     = relationship("XPEvent", back_populates="user")
    # One user → one streak record
    streak        = relationship("Streak", back_populates="user", uselist=False)
    # One user → many redeemed rewards (through UserReward)
    user_rewards  = relationship("UserReward", back_populates="user")
    # One user → many habit completions
    habit_completions = relationship("HabitCompletion", back_populates="user")


# ---------------------------------------------------------------------------
# 2. Portfolio
# ---------------------------------------------------------------------------
class Portfolio(Base):
    __tablename__ = "portfolios"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Total cash balance sitting in the portfolio (not yet invested)
    balance         = Column(Float, default=0.0)
    # Total amount that has been invested (roundups + manual deposits)
    total_invested  = Column(Float, default=0.0)
    # Simulated market value of the invested amount (balance * growth factor)
    market_value    = Column(Float, default=0.0)
    updated_at      = Column(DateTime(timezone=True), onupdate=func.now(),
                             server_default=func.now())

    owner        = relationship("User", back_populates="portfolio")
    transactions = relationship("Transaction", back_populates="portfolio")


# ---------------------------------------------------------------------------
# 3. Transaction
# ---------------------------------------------------------------------------
class Transaction(Base):
    __tablename__ = "transactions"

    id           = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    # Type examples: "deposit", "roundup", "reward_redemption"
    type         = Column(String, nullable=False)
    amount       = Column(Float, nullable=False)
    # Human-readable label shown in the transaction feed
    description  = Column(Text, nullable=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    portfolio = relationship("Portfolio", back_populates="transactions")


# ---------------------------------------------------------------------------
# 4. XPEvent
# ---------------------------------------------------------------------------
class XPEvent(Base):
    __tablename__ = "xp_events"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Category of action that earned XP: "habit", "deposit", "streak", "reward"
    event_type = Column(String, nullable=False)
    points     = Column(Integer, nullable=False)   # XP awarded for this event
    # Optional label shown in the XP activity feed
    label      = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="xp_events")


# ---------------------------------------------------------------------------
# 5. Streak
# ---------------------------------------------------------------------------
class Streak(Base):
    __tablename__ = "streaks"

    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    # How many consecutive days the user has been active
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    # The last date the user completed any habit (used to detect breaks)
    last_active    = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="streak")


# ---------------------------------------------------------------------------
# 6. Reward
# ---------------------------------------------------------------------------
class Reward(Base):
    __tablename__ = "rewards"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    # Cost in XP points the user must spend to redeem this reward
    xp_cost     = Column(Integer, nullable=False)
    # e.g. "fee_waiver", "cashback", "bonus_interest"
    category    = Column(String, nullable=True)
    # False = reward has been retired or is out of stock
    is_active   = Column(Boolean, default=True)

    user_rewards = relationship("UserReward", back_populates="reward")


# ---------------------------------------------------------------------------
# 7. UserReward  (junction table: User ↔ Reward)
# ---------------------------------------------------------------------------
class UserReward(Base):
    __tablename__ = "user_rewards"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    reward_id   = Column(Integer, ForeignKey("rewards.id"), nullable=False)
    redeemed_at = Column(DateTime(timezone=True), server_default=func.now())
    # XP that was deducted at the time of redemption (snapshot in case cost changes)
    xp_spent    = Column(Integer, nullable=False)

    user   = relationship("User", back_populates="user_rewards")
    reward = relationship("Reward", back_populates="user_rewards")


# ---------------------------------------------------------------------------
# 8. Habit
# ---------------------------------------------------------------------------
class Habit(Base):
    __tablename__ = "habits"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    # XP awarded each time the user completes this habit
    xp_reward   = Column(Integer, default=10)
    # "daily" or "weekly"
    frequency   = Column(String, default="daily")
    is_active   = Column(Boolean, default=True)

    completions = relationship("HabitCompletion", back_populates="habit")


# ---------------------------------------------------------------------------
# 9. HabitCompletion
# ---------------------------------------------------------------------------
class HabitCompletion(Base):
    __tablename__ = "habit_completions"

    id           = Column(Integer, primary_key=True, index=True)
    habit_id     = Column(Integer, ForeignKey("habits.id"), nullable=False)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    habit = relationship("Habit", back_populates="completions")
    user  = relationship("User", back_populates="habit_completions")
