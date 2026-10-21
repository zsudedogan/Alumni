"""
SQLAlchemy ORM Entities
Formal database schema definitions matching Data Design Document (ddd.md).
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class UserEntity(Base):
    """Database ORM mapping for users table"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=True)
    email = Column(String(255), nullable=True)

    # Relationships
    job_postings = relationship("JobPostingEntity", back_populates="user", cascade="all, delete-orphan")

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


class JobPostingEntity(Base):
    """Database ORM mapping for job_postings table"""
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True, default="Remote")
    job_type = Column(String(50), nullable=True, default="Full-time")
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=True)
    salary_range = Column(String(100), nullable=True)
    application_deadline = Column(String(20), nullable=True)
    contact_email = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(String(20), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    user = relationship("UserEntity", back_populates="job_postings")

    def __repr__(self):
        return f"<JobPostingEntity(id={self.id}, title='{self.title}', company='{self.company}', is_active={self.is_active})>"


