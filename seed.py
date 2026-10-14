"""
Database Seeder Script
Initializes the database schema and seeds baseline classroom records plus factory-generated data.

Usage:
    python seed.py
    python seed.py --clean
    python seed.py --users 15 --announcements 8
"""

import argparse
import sys
from database import engine, SessionLocal, Base
from models.db_entities import UserEntity, AnnouncementEntity
from factories.user_factory import UserFactory
from factories.announcement_factory import AnnouncementFactory

# Classroom Baseline Records
BASELINE_USERS = [
    {"id": 1, "name": "Emre Yilmaz", "age": 24, "email": "emre@example.com"},
    {"id": 2, "name": "Sude Dogan", "age": 22, "email": "sude@example.com"},
]

BASELINE_ANNOUNCEMENTS = [
    {
        "id": 1,
        "title": "Welcome to Week 04 MVC Architecture",
        "content": "We have successfully modularized our API into Model, View, and Controller layers.",
        "author": "Department of Management Information Systems",
        "category": "Academic",
        "date": "2026-10-07"
    },
    {
        "id": 2,
        "title": "Midterm Project Submissions",
        "content": "Please ensure your repository has updated README documentation and all CRUD routes working.",
        "author": "Course Instructor",
        "category": "Urgent",
        "date": "2026-10-08"
    }
]


def seed_database(clean: bool = False, num_users: int = 8, num_announcements: int = 4):
    """Executes database schema setup and data seeding"""
    print("=" * 60)
    print("🌱 Starting Classroom MVC Database Seeder")
    print(f"   Target Engine: {engine.url}")
    print("=" * 60)

    # 1. Ensure tables exist
    Base.metadata.create_all(bind=engine)
    print("✓ Schema verified (tables 'users' and 'announcements' exist).")

    db = SessionLocal()
    try:
        # 2. Clean if requested
        if clean:
            print("🧹 Wiping existing data (--clean specified)...")
            db.query(AnnouncementEntity).delete()
            db.query(UserEntity).delete()
            db.commit()

        # 3. Seed Baseline Users
        existing_user_count = db.query(UserEntity).count()
        seeded_baseline_users = 0
        for u in BASELINE_USERS:
            if not db.query(UserEntity).filter(UserEntity.id == u["id"]).first():
                db.add(UserEntity(id=u["id"], name=u["name"], age=u["age"], email=u["email"]))
                seeded_baseline_users += 1
        db.commit()

        # 4. Seed Factory Users
        factory_users = UserFactory.build_batch(count=num_users)
        for u in factory_users:
            db.add(UserEntity(**u))
        db.commit()
        print(f"✓ Users seeded: {seeded_baseline_users} baseline, {len(factory_users)} factory generated.")

        # 5. Seed Baseline Announcements
        seeded_baseline_ann = 0
        for a in BASELINE_ANNOUNCEMENTS:
            if not db.query(AnnouncementEntity).filter(AnnouncementEntity.id == a["id"]).first():
                db.add(AnnouncementEntity(
                    id=a["id"],
                    title=a["title"],
                    content=a["content"],
                    author=a["author"],
                    category=a["category"],
                    date=a["date"]
                ))
                seeded_baseline_ann += 1
        db.commit()

        # 6. Seed Factory Announcements
        factory_ann = AnnouncementFactory.build_batch(count=num_announcements)
        for a in factory_ann:
            db.add(AnnouncementEntity(**a))
        db.commit()
        print(f"✓ Announcements seeded: {seeded_baseline_ann} baseline, {len(factory_ann)} factory generated.")

        # Final Summary
        total_users = db.query(UserEntity).count()
        total_ann = db.query(AnnouncementEntity).count()
        print("-" * 60)
        print(f"🎉 Database Seeding Complete!")
        print(f"   Total Users in DB:         {total_users}")
        print(f"   Total Announcements in DB: {total_ann}")
        print("=" * 60)

    except Exception as e:
        db.rollback()
        print(f"❌ Error during seeding: {e}", file=sys.stderr)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the classroom MVC database.")
    parser.add_argument("--clean", action="store_true", help="Truncate tables before seeding")
    parser.add_argument("--users", type=int, default=8, help="Number of factory users to generate")
    parser.add_argument("--announcements", type=int, default=4, help="Number of factory announcements to generate")
    args = parser.parse_args()

    seed_database(clean=args.clean, num_users=args.users, num_announcements=args.announcements)
