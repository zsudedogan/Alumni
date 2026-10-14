"""
Announcement Data Factory
Generates realistic fake announcement records for testing and seeding using Faker.
"""

from typing import List, Dict, Any
import random
from faker import Faker
from models.announcement import AnnouncementCreate

fake = Faker()

CATEGORIES = ["Academic", "General", "Events", "Urgent"]
AUTHORS = [
    "Department of Management Information Systems",
    "Faculty Dean's Office",
    "Student Council",
    "Career Center",
    "Library Directorate",
    "Course Instructor"
]

SAMPLE_TOPICS = [
    ("Midterm Exam Schedule Announced", "The midterm examination timetable for the current semester is now published on the student portal."),
    ("Guest Seminar: Modern Cloud Architecture", "Join us this Friday at the main auditorium for a guest lecture on containerized microservices and Kubernetes."),
    ("Library Hours Extended for Final Preparation", "The central university library will remain open 24/7 during the upcoming exam period."),
    ("Student Software Hackathon Registration Open", "Registrations are now open for the annual 48-hour campus software innovation hackathon."),
    ("System Maintenance Notification", "The campus learning management system will undergo scheduled database maintenance this Sunday between 02:00 and 06:00."),
    ("Career Fair & Internship Networking Day", "Meet with top industry software engineering and management consulting firms next Tuesday in the campus courtyard.")
]


class AnnouncementFactory:
    """Factory for creating synthetic Announcement data"""

    @staticmethod
    def build_payload() -> Dict[str, Any]:
        """Builds a single realistic announcement payload"""
        if random.random() < 0.6:
            title, content = random.choice(SAMPLE_TOPICS)
        else:
            title = fake.sentence(nb_words=6).rstrip(".")
            content = fake.paragraph(nb_sentences=3)

        return {
            "title": title,
            "content": content,
            "author": random.choice(AUTHORS),
            "category": random.choice(CATEGORIES),
            "date": fake.date_between(start_date="-30d", end_date="today").isoformat()
        }

    @classmethod
    def build_schema(cls) -> AnnouncementCreate:
        """Builds a validated Pydantic AnnouncementCreate model"""
        return AnnouncementCreate(**cls.build_payload())

    @classmethod
    def build_batch(cls, count: int = 5) -> List[Dict[str, Any]]:
        """Builds a batch of announcement payloads"""
        return [cls.build_payload() for _ in range(count)]
