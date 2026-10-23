"""
Job Posting Data Factory
Generates realistic fake job posting records for testing and seeding using Faker.
"""

from typing import List, Dict, Any, Optional
import random
from faker import Faker
from models.job_posting import JobPostingCreate

fake = Faker()

JOB_TYPES = ["Full-time", "Part-time", "Internship", "Contract"]
LOCATIONS = [
    "Remote",
    "Istanbul / Hybrid",
    "Istanbul / On-site",
    "Izmir / Hybrid",
    "Ankara / On-site",
    "Remote (Europe)",
    "Remote (Global)"
]

TECH_COMPANIES = [
    "TechNova Solutions",
    "Peak Data Systems",
    "FinTrust Software",
    "InnoWave Digital",
    "CloudScale Networks",
    "Alpha HealthTech",
    "HyperLogic AI Labs",
    "Starlight Mobile Interactive",
    "Quantum Dynamics",
    "NextGen Cyber Security"
]

SAMPLE_JOB_POSTINGS = [
    {
        "title": "Junior Backend Developer (Python / FastAPI)",
        "company": "TechNova Solutions",
        "job_type": "Full-time",
        "location": "Istanbul / Hybrid",
        "description": "We are seeking a junior backend engineer passionate about building high-performance REST APIs with FastAPI, PostgreSQL, and Docker microservices.",
        "requirements": "Strong Python knowledge, basic understanding of relational databases (SQLAlchemy / PostgreSQL), RESTful API concepts, Git workflows.",
        "salary_range": "₺35,000 - ₺45,000 / month",
    },
    {
        "title": "Frontend Engineering Intern (React / TypeScript)",
        "company": "InnoWave Digital",
        "job_type": "Internship",
        "location": "Remote",
        "description": "Exciting internship opportunity to participate in building modern, responsive web user interfaces using React, Next.js, and Tailwind CSS.",
        "requirements": "Proficiency in JavaScript / TypeScript, modern HTML/CSS, basic React experience, enthusiasm to learn cloud deployment.",
        "salary_range": "Paid Internship + Mentorship",
    },
    {
        "title": "Data Analyst & Business Intelligence Intern",
        "company": "Peak Data Systems",
        "job_type": "Internship",
        "location": "Izmir / Hybrid",
        "description": "Analyze operational business metrics, build interactive dashboards, and optimize business intelligence reporting pipelines.",
        "requirements": "SQL querying skills, Python (pandas / numpy), basic PowerBI or Tableau experience, strong analytical problem-solving skills.",
        "salary_range": "₺25,000 - ₺30,000 / month",
    },
    {
        "title": "DevOps & Cloud Infrastructure Engineer",
        "company": "CloudScale Networks",
        "job_type": "Full-time",
        "location": "Remote (Europe)",
        "description": "Help manage, automate, and scale our containerized infrastructure utilizing Docker, Kubernetes, GitHub Actions CI/CD pipelines, and AWS.",
        "requirements": "Experience with Linux administration, Docker containerization, CI/CD pipelines, and cloud computing fundamentals.",
        "salary_range": "€2,500 - €3,500 / month",
    },
    {
        "title": "Software Quality Assurance (QA) Intern",
        "company": "FinTrust Software",
        "job_type": "Internship",
        "location": "Ankara / On-site",
        "description": "Join our QA testing team to design automated test scripts with pytest, write test plans, and ensure enterprise software reliability.",
        "requirements": "Basic programming fundamentals, attention to detail, understanding of software testing methodologies (unit, integration, regression).",
        "salary_range": "Paid Internship",
    },
    {
        "title": "Machine Learning & AI Research Fellow",
        "company": "HyperLogic AI Labs",
        "job_type": "Part-time",
        "location": "Istanbul / Hybrid",
        "description": "Assist our core research team with training and evaluating state-of-the-art transformer models, data preprocessing, and model benchmarking.",
        "requirements": "Python, PyTorch or TensorFlow, solid mathematical foundations, linear algebra, and curiosity for cutting-edge LLMs.",
        "salary_range": "₺40,000 - ₺55,000 / month",
    }
]


class JobPostingFactory:
    """Factory for creating synthetic Job Posting data"""

    @staticmethod
    def build_payload(user_id: Optional[int] = None) -> Dict[str, Any]:
        """Builds a single realistic job posting payload"""
        if random.random() < 0.7:
            template = random.choice(SAMPLE_JOB_POSTINGS)
            title = template["title"]
            company = template["company"]
            job_type = template["job_type"]
            location = template["location"]
            description = template["description"]
            requirements = template["requirements"]
            salary_range = template["salary_range"]
        else:
            role = random.choice(["Software Developer", "Product Manager", "Data Engineer", "UI/UX Designer", "Security Analyst"])
            level = random.choice(["Junior", "Associate", "Intern"])
            title = f"{level} {role}"
            company = random.choice(TECH_COMPANIES)
            job_type = random.choice(JOB_TYPES)
            location = random.choice(LOCATIONS)
            description = fake.paragraph(nb_sentences=3)
            requirements = fake.paragraph(nb_sentences=2)
            salary_range = f"₺{random.randint(25, 60)},000 / month"

        created_date = fake.date_between(start_date="-20d", end_date="today").isoformat()
        deadline_date = fake.date_between(start_date="+10d", end_date="+60d").isoformat()
        contact = f"jobs@{company.lower().replace(' ', '')}.com"

        return {
            "title": title,
            "company": company,
            "location": location,
            "job_type": job_type,
            "description": description,
            "requirements": requirements,
            "salary_range": salary_range,
            "application_deadline": deadline_date,
            "contact_email": contact,
            "is_active": True,
            "created_at": created_date,
            "user_id": user_id
        }

    @classmethod
    def build_schema(cls, user_id: Optional[int] = None) -> JobPostingCreate:
        """Builds a validated Pydantic JobPostingCreate model"""
        return JobPostingCreate(**cls.build_payload(user_id=user_id))

    @classmethod
    def build_batch(cls, count: int = 6, user_ids: Optional[List[int]] = None) -> List[Dict[str, Any]]:
        """Builds a batch of job posting payloads with optional user ID associations"""
        batch = []
        for _ in range(count):
            assigned_user_id = random.choice(user_ids) if user_ids else None
            batch.append(cls.build_payload(user_id=assigned_user_id))
        return batch
