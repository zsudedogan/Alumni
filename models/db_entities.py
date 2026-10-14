"""
SQLAlchemy ORM Entities
Formal database schema definitions matching Data Design Document (ddd.md).
"""

from sqlalchemy import Column, Integer, String, Text
from database import Base


class UserEntity(Base):
    """Database ORM mapping for users table"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=True)
    email = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<UserEntity(id={self.id}, name='{self.name}', email='{self.email}')>"


class AnnouncementEntity(Base):
    """Database ORM mapping for announcements table"""
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100), default="Admin", nullable=True)
    category = Column(String(50), default="General", nullable=True)
    date = Column(String(20), nullable=True)

    def __repr__(self):
        return f"<AnnouncementEntity(id={self.id}, title='{self.title}', category='{self.category}')>"
