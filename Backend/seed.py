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
            # (No pre-seeded reward redemption.)
        ]
        # Compute current total and adjust to land between 700-800 XP for demo.
        # We pick a target of 750 XP and add one adjustment event if needed.
        current_total = sum(ev.points for ev in xp_events)
        target_total = 750
        delta = target_total - current_total
        if delta != 0:
            # Create a single adjustment event so the seeded demo shows ~750 XP
            adj_label = f"Seed adjustment ({'+' if delta>0 else ''}{delta} XP)"
            xp_events.append(
                models.XPEvent(
                    user_id=alex.id,
                    event_type="seed_adjust",
                    points=delta,
                    label=adj_label,
                    created_at=now,
                )
            )
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
        # 6. Rewards catalog (user-requested list)
        # ---------------------------------------------------------------
        rewards = [
            models.Reward(
                name="2x Scene+ boost — 1 week",
                description="Double your Scene+ earn rate for 7 days (10 bonus Scene+ points).",
                xp_cost=800,
                category="scene",
                is_active=True,
            ),
            models.Reward(
                name="Scotia Smart Money — 30 days",
                description="Unlock premium budgeting insights and personalized tips for 30 days.",
                xp_cost=200,
                category="premium",
                is_active=True,
            ),
            models.Reward(
                name="Scotia Advisor Chat — 30 min",
                description="30-minute financial wellness session with an advisor.",
                xp_cost=600,
                category="advisor",
                is_active=True,
            ),
            models.Reward(
                name="Tuesday Movie On Us",
                description="One free Cineplex ticket redeemable on Tuesdays.",
                xp_cost=300,
                category="entertainment",
                is_active=True,
            ),
        ]
        db.add_all(rewards)
        db.flush()   # flush so reward IDs are available below

        # No pre-redeemed rewards for the demo user.

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
        # Recompute and display the actual total XP inserted (including adjustment)
        total_xp = sum(ev.points for ev in xp_events)
        print(f"  XP:         {total_xp} total")
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
