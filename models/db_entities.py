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
    role = Column(String(50), nullable=False, default="Student")
    department = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    password = Column(String(255), nullable=True)
    created_at = Column(String(20), nullable=True)

    # Relationships
    job_postings = relationship("JobPostingEntity", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("ApplicationEntity", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<UserEntity(id={self.id}, name='{self.name}', role='{self.role}', email='{self.email}')>"


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
    title = Column(String(120), nullable=False)
    company = Column(String(255), nullable=False)
    city = Column(String(100), nullable=True)
    location = Column(String(255), nullable=True, default="Remote")
    job_type = Column(String(50), nullable=True, default="Full-time")
    description = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    salary_range = Column(String(100), nullable=True)
    application_deadline = Column(String(20), nullable=True)
    contact_email = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(String(20), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    user = relationship("UserEntity", back_populates="job_postings")
    applications = relationship("ApplicationEntity", back_populates="job_posting", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<JobPostingEntity(id={self.id}, title='{self.title}', company='{self.company}', is_active={self.is_active})>"


class ApplicationEntity(Base):
    """Database ORM mapping for applications table"""
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    resume_url = Column(String(500), nullable=True)
    cover_note = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="Pending")
    created_at = Column(String(20), nullable=True)

    # Relationships
    user = relationship("UserEntity", back_populates="applications")
    job_posting = relationship("JobPostingEntity", back_populates="applications")

    def __repr__(self):
        return f"<ApplicationEntity(id={self.id}, job_id={self.job_id}, user_id={self.user_id}, status='{self.status}')>"



