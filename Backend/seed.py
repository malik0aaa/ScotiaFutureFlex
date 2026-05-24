"""
seed.py — Pre-populate the database with demo user Alex Chen.
Run once after starting the app:  python seed.py
Safe to run multiple times — checks if Alex already exists before inserting.
"""

from datetime import datetime, timedelta
from database import engine, SessionLocal
import models

# Create all tables defined in models.py (no-op if they already exist)
models.Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()

    try:
        # ---------------------------------------------------------------
        # Guard: skip if Alex already exists
        # ---------------------------------------------------------------
        existing = db.query(models.User).filter_by(email="alex@demo.com").first()
        if existing:
            print("✓ Seed data already present — skipping.")
            return

        print("Seeding database with demo user Alex Chen...")

        # ---------------------------------------------------------------
        # 1. User — Alex Chen
        # ---------------------------------------------------------------
        alex = models.User(
            name="Alex Chen",
            email="alex@demo.com",
            goal="first_home",       # saving toward a first home purchase
            goal_target_amount=50000.0,
            kyc_verified=True,
        )
        db.add(alex)
        db.flush()   # flush so alex.id is populated before we reference it

        goal = models.InvestmentGoal(
            user_id=alex.id,
            goal="first_home",
            target_amount=50000.0,
        )
        db.add(goal)

        # ---------------------------------------------------------------
        # 2. Portfolio
        # ---------------------------------------------------------------
        portfolio = models.Portfolio(
            user_id=alex.id,
            balance=142.50,          # uninvested cash sitting in the account
            total_invested=380.00,   # sum of all deposits + roundups invested
            market_value=401.85,     # 380 * 1.0575 — simulated 5.75% growth
        )
        db.add(portfolio)
        db.flush()   # flush so portfolio.id is available for transactions

        # ---------------------------------------------------------------
        # 3. Transactions (5 — mix of deposits and roundups)
        # ---------------------------------------------------------------
        now = datetime.utcnow()

        transactions = [
            models.Transaction(
                portfolio_id=portfolio.id,
                type="deposit",
                amount=200.00,
                description="Initial deposit — onboarding",
                created_at=now - timedelta(days=30),
            ),
            models.Transaction(
                portfolio_id=portfolio.id,
                type="roundup",
                amount=0.65,
                description="Roundup: Tim Hortons $4.35",
                created_at=now - timedelta(days=25),
            ),
            models.Transaction(
                portfolio_id=portfolio.id,
                type="deposit",
                amount=100.00,
                description="Manual deposit",
                created_at=now - timedelta(days=18),
            ),
            models.Transaction(
                portfolio_id=portfolio.id,
                type="roundup",
                amount=0.45,
                description="Roundup: Subway $9.55",
                created_at=now - timedelta(days=10),
            ),
            models.Transaction(
                portfolio_id=portfolio.id,
                type="roundup",
                amount=0.90,
                description="Roundup: Shoppers Drug Mart $12.10",
                created_at=now - timedelta(days=3),
            ),
        ]
        db.add_all(transactions)

        # ---------------------------------------------------------------
        # 4. XP Events — totalling 620 XP
        # ---------------------------------------------------------------
        xp_events = [
            # Onboarding bonus
            models.XPEvent(
                user_id=alex.id, event_type="deposit",
                points=100, label="First deposit bonus",
                created_at=now - timedelta(days=30),
            ),
            # Habit completions over the past weeks
            models.XPEvent(
                user_id=alex.id, event_type="habit",
                points=40, label="Completed 4 habits",
                created_at=now - timedelta(days=28),
            ),
            models.XPEvent(
                user_id=alex.id, event_type="habit",
                points=40, label="Completed 4 habits",
                created_at=now - timedelta(days=21),
            ),
            models.XPEvent(
                user_id=alex.id, event_type="habit",
                points=40, label="Completed 4 habits",
                created_at=now - timedelta(days=14),
            ),
            # Streak milestones
            models.XPEvent(
                user_id=alex.id, event_type="streak",
                points=50, label="3-day streak bonus",
                created_at=now - timedelta(days=27),
            ),
            models.XPEvent(
                user_id=alex.id, event_type="streak",
                points=100, label="7-day streak bonus",
                created_at=now - timedelta(days=23),
            ),
            # Manual deposit XP
            models.XPEvent(
                user_id=alex.id, event_type="deposit",
                points=50, label="Deposit bonus",
                created_at=now - timedelta(days=18),
            ),
            # Roundup XP
            models.XPEvent(
                user_id=alex.id, event_type="habit",
                points=40, label="Completed 4 habits",
                created_at=now - timedelta(days=7),
            ),
            models.XPEvent(
                user_id=alex.id, event_type="habit",
                points=40, label="Completed 4 habits",
                created_at=now - timedelta(days=3),
            ),
            # Recent habit completions
            models.XPEvent(
                user_id=alex.id, event_type="habit",
                points=40, label="Completed 4 habits",
                created_at=now - timedelta(days=1),
            ),
            # Today's activity
            models.XPEvent(
                user_id=alex.id, event_type="habit",
                points=40, label="Completed 4 habits",
                created_at=now,
            ),
            # Reward redemption (XP deducted — stored as negative)
            models.XPEvent(
                user_id=alex.id, event_type="reward",
                points=-100, label="Redeemed: Monthly Fee Waiver",
                created_at=now - timedelta(days=15),
            ),
        ]
        # Total = 100+40+40+40+50+100+50+40+40+40+40-100 = 620 XP ✓
        db.add_all(xp_events)

        # ---------------------------------------------------------------
        # 5. Streak
        # ---------------------------------------------------------------
        streak = models.Streak(
            user_id=alex.id,
            current_streak=7,
            longest_streak=12,
            last_active=now,   # active today
        )
        db.add(streak)

        # ---------------------------------------------------------------
        # 6. Rewards catalog (4 rewards)
        # ---------------------------------------------------------------
        rewards = [
            models.Reward(
                name="Monthly Fee Waiver",
                description="Waive your monthly account fee for one month.",
                xp_cost=100,
                category="fee_waiver",
                is_active=True,
            ),
            models.Reward(
                name="1% Cashback Boost",
                description="Earn 1% extra cashback on all purchases for 7 days.",
                xp_cost=200,
                category="cashback",
                is_active=True,
            ),
            models.Reward(
                name="Bonus Interest Rate",
                description="Get 0.5% bonus interest on your savings for 30 days.",
                xp_cost=300,
                category="bonus_interest",
                is_active=True,
            ),
            models.Reward(
                name="Free ETF Trade",
                description="One commission-free ETF trade on Scotia iTRADE.",
                xp_cost=500,
                category="free_trade",
                is_active=True,
            ),
        ]
        db.add_all(rewards)
        db.flush()   # flush so reward IDs are available below

        # ---------------------------------------------------------------
        # 7. UserReward — Alex already redeemed the Fee Waiver
        # ---------------------------------------------------------------
        fee_waiver = rewards[0]
        user_reward = models.UserReward(
            user_id=alex.id,
            reward_id=fee_waiver.id,
            xp_spent=fee_waiver.xp_cost,
            redeemed_at=now - timedelta(days=15),
        )
        db.add(user_reward)

        # ---------------------------------------------------------------
        # 8. Habits (4 daily habits)
        # ---------------------------------------------------------------
        habits = [
            models.Habit(
                name="Check Your Portfolio",
                description="Open the app and review your portfolio balance.",
                xp_reward=10,
                frequency="daily",
                is_active=True,
            ),
            models.Habit(
                name="No-Spend Day",
                description="Go the whole day without an unnecessary purchase.",
                xp_reward=15,
                frequency="daily",
                is_active=True,
            ),
            models.Habit(
                name="Read a Finance Tip",
                description="Read one financial literacy tip in the app.",
                xp_reward=10,
                frequency="daily",
                is_active=True,
            ),
            models.Habit(
                name="Transfer $1 to Savings",
                description="Move at least $1 into your investment portfolio.",
                xp_reward=15,
                frequency="daily",
                is_active=True,
            ),
        ]
        db.add_all(habits)
        db.flush()   # flush so habit IDs are available for completions

        # ---------------------------------------------------------------
        # 9. HabitCompletions — back the 7-day streak
        #    All 4 habits completed each day for the past 7 days
        # ---------------------------------------------------------------
        completions = []
        for days_ago in range(7, 0, -1):   # 7 days ago → 1 day ago
            for habit in habits:
                completions.append(
                    models.HabitCompletion(
                        habit_id=habit.id,
                        user_id=alex.id,
                        completed_at=now - timedelta(days=days_ago),
                    )
                )
        # Also add today's completions (all 4 done today)
        for habit in habits:
            completions.append(
                models.HabitCompletion(
                    habit_id=habit.id,
                    user_id=alex.id,
                    completed_at=now,
                )
            )
        db.add_all(completions)

        # ---------------------------------------------------------------
        # Commit everything in one transaction — all or nothing
        # ---------------------------------------------------------------
        db.commit()
        print("✓ Seed complete!")
        print(f"  User:       Alex Chen (id={alex.id})")
        print(f"  Portfolio:  balance=${portfolio.balance}, invested=${portfolio.total_invested}")
        print(f"  XP:         620 total")
        print(f"  Streak:     {streak.current_streak} days current, {streak.longest_streak} days longest")
        print(f"  Rewards:    {len(rewards)} in catalog, 1 redeemed")
        print(f"  Habits:     {len(habits)} active")
        print(f"  Completions:{len(completions)} logged")

    except Exception as e:
        db.rollback()
        print(f"✗ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
