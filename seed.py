"""
Database Seeder Script
Initializes the database schema and seeds baseline classroom records plus factory-generated data.

Usage:
    python seed.py
    python seed.py --clean
    python seed.py --users 15 --announcements 8 --jobs 10
"""

import argparse
import sys
from database import engine, SessionLocal, Base
from models.db_entities import UserEntity, AnnouncementEntity, JobPostingEntity, ApplicationEntity
from factories.user_factory import UserFactory
from factories.announcement_factory import AnnouncementFactory
from factories.job_posting_factory import JobPostingFactory

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

BASELINE_JOB_POSTINGS = [
    {
        "id": 1,
        "title": "Junior Python / FastAPI Developer",
        "company": "TechNova Solutions",
        "location": "Istanbul / Hybrid",
        "job_type": "Full-time",
        "description": "Develop and maintain RESTful API microservices, database schemas, and cloud deployments using FastAPI, PostgreSQL, and Docker.",
        "requirements": "Proficiency in Python 3.11+, basic SQL / ORM experience (SQLAlchemy), REST API principles, Git.",
        "salary_range": "₺38,000 - ₺48,000 / month",
        "application_deadline": "2026-11-30",
        "contact_email": "careers@technova.com",
        "is_active": True,
        "created_at": "2026-10-15",
        "user_id": 1
    },
    {
        "id": 2,
        "title": "Frontend Engineering Intern (React / Tailwind)",
        "company": "InnoWave Digital",
        "location": "Remote",
        "job_type": "Internship",
        "description": "Collaborate with UI/UX designers and senior engineers to build accessible, responsive user interfaces for modern web applications.",
        "requirements": "Strong HTML, CSS, JavaScript / TypeScript fundamentals, basic familiarity with React components.",
        "salary_range": "Paid Internship + Mentorship",
        "application_deadline": "2026-11-15",
        "contact_email": "internships@innowave.com",
        "is_active": True,
        "created_at": "2026-10-18",
        "user_id": 2
    },
    {
        "id": 3,
        "title": "Data Science & BI Specialist",
        "company": "Peak Data Systems",
        "location": "Izmir / Hybrid",
        "job_type": "Full-time",
        "description": "Extract actionable business insights, design automated ETL pipelines, and develop predictive analytics models.",
        "requirements": "Python (pandas, numpy, scikit-learn), advanced SQL, data visualization tools (Tableau/PowerBI).",
        "salary_range": "₺45,000 - ₺60,000 / month",
        "application_deadline": "2026-12-01",
        "contact_email": "jobs@peakdata.com",
        "is_active": True,
        "created_at": "2026-10-20",
        "user_id": 1
    }
]


def seed_database(clean: bool = False, num_users: int = 8, num_announcements: int = 4, num_jobs: int = 6):
    """Executes database schema setup and data seeding for Users, Announcements, and Job Postings"""
    print("=" * 60)
    print("🌱 Starting Classroom MVC Database Seeder")
    print(f"   Target Engine: {engine.url}")
    print("=" * 60)

    # 1. Ensure tables exist
    Base.metadata.create_all(bind=engine)
    print("✓ Schema verified (tables 'users', 'announcements', 'job_postings', 'applications' exist).")

    db = SessionLocal()
    try:
        # 2. Clean if requested (respecting foreign key relationships)
        if clean:
            print("🧹 Wiping existing data (--clean specified)...")
            db.query(ApplicationEntity).delete()
            db.query(JobPostingEntity).delete()
            db.query(AnnouncementEntity).delete()
            db.query(UserEntity).delete()
            db.commit()

        # 3. Seed Baseline Users
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

        # 7. Seed Baseline Job Postings
        existing_user_ids = [u.id for u in db.query(UserEntity.id).all()]
        seeded_baseline_jobs = 0
        for j in BASELINE_JOB_POSTINGS:
            if not db.query(JobPostingEntity).filter(JobPostingEntity.id == j["id"]).first():
                # Make sure the foreign key user_id is valid
                uid = j["user_id"] if j["user_id"] in existing_user_ids else None
                db.add(JobPostingEntity(
                    id=j["id"],
                    title=j["title"],
                    company=j["company"],
                    location=j["location"],
                    job_type=j["job_type"],
                    description=j["description"],
                    requirements=j["requirements"],
                    salary_range=j["salary_range"],
                    application_deadline=j["application_deadline"],
                    contact_email=j["contact_email"],
                    is_active=j["is_active"],
                    created_at=j["created_at"],
                    user_id=uid
                ))
                seeded_baseline_jobs += 1
        db.commit()

        # 8. Seed Factory Job Postings (Step 6 requirement)
        factory_jobs = JobPostingFactory.build_batch(count=num_jobs, user_ids=existing_user_ids)
        for j in factory_jobs:
            db.add(JobPostingEntity(**j))
        db.commit()
        print(f"✓ Job Postings seeded: {seeded_baseline_jobs} baseline, {len(factory_jobs)} factory generated.")

        # Final Summary
        total_users = db.query(UserEntity).count()
        total_ann = db.query(AnnouncementEntity).count()
        total_jobs = db.query(JobPostingEntity).count()
        total_apps = db.query(ApplicationEntity).count()
        print("-" * 60)
        print(f"🎉 Database Seeding Complete!")
        print(f"   Total Users in DB:         {total_users}")
        print(f"   Total Announcements in DB: {total_ann}")
        print(f"   Total Job Postings in DB:  {total_jobs}")
        print(f"   Total Applications in DB:  {total_apps}")
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
    parser.add_argument("--jobs", type=int, default=6, help="Number of factory job postings to generate")
    args = parser.parse_args()

    seed_database(
        clean=args.clean,
        num_users=args.users,
        num_announcements=args.announcements,
        num_jobs=args.jobs
    )
