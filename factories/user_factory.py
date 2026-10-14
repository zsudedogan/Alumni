"""
User Data Factory
Generates realistic fake user records for testing and seeding using Faker.
"""

from typing import List, Dict, Any
from faker import Faker
from models.user import UserCreate

fake = Faker()


class UserFactory:
    """Factory for creating synthetic User data"""

    @staticmethod
    def build_payload() -> Dict[str, Any]:
        """Builds a single user payload dictionary"""
        return {
            "name": fake.name(),
            "age": fake.random_int(min=19, max=30),
            "email": fake.unique.email()
        }

    @classmethod
    def build_schema(cls) -> UserCreate:
        """Builds a validated Pydantic UserCreate model"""
        return UserCreate(**cls.build_payload())

    @classmethod
    def build_batch(cls, count: int = 10) -> List[Dict[str, Any]]:
        """Builds a batch of user payloads"""
        return [cls.build_payload() for _ in range(count)]
