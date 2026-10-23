# Classroom REST API - MVC Architecture & The Forgetting Test

This repository implements all classroom exercises, the complete homework assignment, and the container lifecycle experiment: **The Forgetting Test**.

> 📊 **Data Design Specification:**
> For comprehensive entity definitions, schema constraints, data dictionary, and Entity-Relationship Diagrams (ERD), see the **[Data Design Document (ddd.md)](./ddd.md)**.

---

## 🧪 The Forgetting Test (Container Lifecycle & Persistence)

### 📌 What is the Forgetting Test?
The **Forgetting Test** demonstrates the ephemeral (temporary) nature of Docker containers without persistent storage (volumes) or an external database.

```text
  [Step 1: Start App]
  docker compose up -d
         │
         ▼
  [Step 2: Create Record]
  POST /api/users/ ───► Record saved in Container RAM (in-memory)
         │
         ▼
  [Step 3: Destroy Container]
  docker compose down ───► Container stopped & destroyed (Process memory wiped)
         │
         ▼
  [Step 4: Re-start Container]
  docker compose up -d ───► Container boots fresh from image
         │
         ▼
  [Step 5: Check Record]
  GET /api/users/ ────► ❌ Record is FORGOTTEN (Amnesia)!
```

### 🔬 How to Run the Forgetting Test

#### Option A: Run Automated Demonstration Script
```bash
python3 forgetting_test.py
```

#### Option B: Run with Docker Compose
1. **Start the Container:**
   ```bash
   docker compose up --build -d
   ```

2. **Step 1 - Create a new record:**
   ```bash
   curl -X POST http://localhost:8000/api/users/ \
     -H "Content-Type: application/json" \
     -d '{"name": "Temporary Record", "age": 25, "email": "temp@example.com"}'
   ```
   *Verify it exists:*
   ```bash
   curl http://localhost:8000/api/users/
   ```
   *(You will see the new user with ID 3).*

3. **Step 2 - Stop and destroy container:**
   ```bash
   docker compose down
   ```

4. **Step 3 - Start the container again:**
   ```bash
   docker compose up -d
   ```

5. **Step 4 - Check the record:**
   ```bash
   curl http://localhost:8000/api/users/
   ```
   *Result:* **The record is FORGOTTEN!** Only the default hardcoded records (ID 1 & 2) exist.

### 💡 Why did it forget?
* **In-Memory Store:** The data lived only in Python's memory (RAM) inside the container.
* **Ephemeral Containers:** `docker compose down` removes the container and its write layer. Without a persistent volume (`volumes:` in `docker-compose.yml`) or a database, any state changes are lost.

---

## 🏛️ MVC (Model-View-Controller) Architecture Documentation

The application strictly decouples concerns across three distinct layers:

```
  +-------------------------------------------------------------+
  |                        CLIENT                               |
  |             (Web Browser, Postman, Swagger UI)              |
  +-------------------------------------------------------------+
                               |    ^
                1. HTTP Request|    | 4. HTTP Response (HTML/JSON)
                               v    |
  +-------------------------------------------------------------+
  |                      CONTROLLER                             |
  |   (UserController, AnnouncementController, ApiControllers)  |
  |   - Intercepts requests & path parameters                   |
  |   - Validates data via Pydantic schemas                     |
  |   - Executes business logic & calls Model methods           |
  |   - Returns HTML from View or JSON for API                  |
  +-------------------------------------------------------------+
               |                                ^
  2. Read/Write|                                | 3. Validated Data
               v                                |
  +--------------------------+    +-----------------------------+
  |          MODEL           |    |            VIEW             |
  |  (UserModel, AnnModel)   |--->|   (user_view, ann_view)     |
  | - In-memory CRUD methods |    | - HTML Management Interfaces|
  | - Pydantic data schemas  |    | - JSON serialization        |
  | - Auto-incrementing IDs  |    | - Swagger UI Documentation  |
  +--------------------------+    +-----------------------------+
```

---

### 📂 Directory & File Structure (Tree View)

```text
fastapi-app/
│
├── Dockerfile                          # Docker container build specification
├── docker-compose.yml                  # Docker Compose (PostgreSQL 15 + Web API)
├── .dockerignore                       # Build context exclusion rules
├── .env.example                        # Template for environment variables (committed)
├── .env                                # Local environment secrets (git-ignored)
├── database.py                         # SQLAlchemy engine & session configuration
├── seed.py                             # Database seeder (baseline & factory data)
│
├── alembic/                            # Database migrations directory
│   ├── env.py                          # Alembic migration environment
│   └── versions/                       # Migration version scripts
├── factories/                          # Synthetic data factories (Faker)
│   ├── user_factory.py                 # User data generator
│   └── announcement_factory.py         # Announcement data generator
│
├── models/                             # [M] MODEL LAYER (Database & Pydantic DTOs)
│   ├── __init__.py
│   ├── db_entities.py                  # SQLAlchemy ORM Entities (User, Ann, JobPosting, Application)
│   ├── user.py                         # UserModel: DB CRUD & Pydantic schemas
│   ├── announcement.py                 # AnnouncementModel: DB CRUD & Pydantic schemas
│   ├── job_posting.py                  # JobPostingModel: DB CRUD & Pydantic schemas
│   └── application.py                  # ApplicationModel: DB CRUD & Pydantic schemas
│
├── views/                              # [V] VIEW LAYER (HTML Management Interfaces)
│   ├── __init__.py
│   ├── user_view.py                    # HTML View for User Management
│   ├── announcement_view.py            # HTML View for Announcement Management
│   ├── job_posting_view.py             # HTML View for Career & Job Postings
│   └── application_view.py             # HTML View for Student Job Applications
│
├── controllers/                        # [C] CONTROLLER LAYER
│   ├── __init__.py
│   ├── user_controller.py              # UserController: Handles .../users/ with View Layer
│   ├── api_user_controller.py          # ApiUserController: Handles .../api/users/ (JSON)
│   ├── announcement_controller.py      # AnnouncementController: Handles .../announcements/
│   ├── api_announcement_controller.py  # ApiAnnouncementController: Handles .../api/announcements/
│   ├── job_posting_controller.py       # JobPostingController: Handles .../job-postings/
│   ├── api_job_posting_controller.py   # ApiJobPostingController: Direct & Nested routes
│   ├── application_controller.py       # ApplicationController: Handles .../applications/
│   └── api_application_controller.py   # ApiApplicationController: Direct & Nested routes
│
├── main.py                             # Main Application Hub with lifespan DB init
├── forgetting_test.py                  # Automated script for The Forgetting Test
├── postman_collection.json             # Postman Test Suite
├── requirements.txt                    # Project Dependencies (SQLAlchemy, Alembic, Faker)
├── test_api.py                         # Automated Pytest Suite
├── ddd.md                              # Data Design Document
└── README.md                           # Documentation & Architecture Guide
```

---

## 📊 Data Design Documentation (DDD)

A dedicated, formal **[Data Design Document (ddd.md)](./ddd.md)** is maintained for this project to specify data contracts, entity relationships, validation schemas, and lifecycle constraints.

> 🔗 **Direct Document Link:** **[Open Data Design Document (ddd.md)](./ddd.md)**

### Key Topics Covered in `ddd.md`:
* **Domain Entities & Data Dictionary:** Comprehensive schema specifications, data types, nullability, auto-increment rules, and constraints for `User`, `Announcement`, and `JobPosting` (along with reference entities `Alumni` and `Auto`).
* **Entity-Relationship Diagram (ERD):** Visual representation of domain entities with primary keys and constraints using Mermaid.
* **Pydantic Schemas & DTOs:** Separation of request and response representations (`Base`, `Create`, `Update`, `Patch`, `Full Model`).
* **CRUD to Controller Mapping:** Detailed mapping table connecting HTTP methods (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) and route paths to model methods.
* **Storage Lifecycle & The Forgetting Test:** Architectural analysis of volatile in-memory container RAM versus persistent volume and relational database storage strategies.

---

## 📋 Route & Controller Mapping

### 1. 👥 User Module
* **Web View Controller (`.../users/`):** [`controllers/user_controller.py`](./controllers/user_controller.py)
  * `GET /users/` ➔ Interactive HTML Management Interface (Listing & Creating).
* **REST API Controller (`.../api/users/`):** [`controllers/api_user_controller.py`](./controllers/api_user_controller.py)
  * Full JSON CRUD API for users.

### 2. 📢 Announcement Module
* **Web View Controller (`.../announcements/`):** [`controllers/announcement_controller.py`](./controllers/announcement_controller.py)
  * `GET /announcements/` ➔ Interactive Web Management Interface.
* **REST API Controller (`.../api/announcements/`):** [`controllers/api_announcement_controller.py`](./controllers/api_announcement_controller.py)
  * Full JSON CRUD API for announcements.

### 3. 💼 Job Posting Module (Direct & Nested Routes)
* **Web View Controller (`.../job-postings/`):** [`controllers/job_posting_controller.py`](./controllers/job_posting_controller.py)
  * `GET /job-postings/` ➔ Interactive Career Portal & Job Management Interface.
* **Direct REST API Controller (`.../api/job-postings/`):** [`controllers/api_job_posting_controller.py`](./controllers/api_job_posting_controller.py)
  * `GET /api/job-postings` ➔ List all job postings (supports `active_only`, `user_id` query filters).
  * `GET /api/job-postings/{id}` ➔ Retrieve single job posting with publisher details.
  * `POST /api/job-postings` ➔ Create a new job posting.
  * `PUT /api/job-postings/{id}` ➔ Full update.
  * `PATCH /api/job-postings/{id}` ➔ Partial update.
  * `DELETE /api/job-postings/{id}` ➔ Delete job posting.
* **Nested REST API Routes (`.../api/users/{user_id}/job-postings/`):**
  * `GET /api/users/{user_id}/job-postings` ➔ List all postings created by a specific user (1-to-many relationship).
  * `POST /api/users/{user_id}/job-postings` ➔ Create a job posting under a specific user (binds `user_id`).
  * `GET /api/users/{user_id}/job-postings/{job_id}` ➔ Retrieve specific user-owned posting.
  * `DELETE /api/users/{user_id}/job-postings/{job_id}` ➔ Delete specific user-owned posting.

### 4. 📝 Application Module (Direct & Nested Routes - Step 5)
* **Web View Controller (`.../applications/`):** [`controllers/application_controller.py`](./controllers/application_controller.py)
  * `GET /applications/` ➔ Interactive Student Job Application Management Interface.
* **Direct REST API Controller (`.../api/applications/`):** [`controllers/api_application_controller.py`](./controllers/api_application_controller.py)
  * `GET /api/applications` ➔ List all applications (supports `job_id`, `user_id`, `status` filters).
  * `GET /api/applications/{id}` ➔ Retrieve application with resolved applicant & job posting details.
  * `POST /api/applications` ➔ Direct application submission.
  * `PUT /api/applications/{id}` ➔ Full update.
  * `PATCH /api/applications/{id}` ➔ Partial update (e.g. status transition: Pending -> Reviewed -> Accepted).
  * `DELETE /api/applications/{id}` ➔ Delete application.
* **Nested REST API Routes (JobPostings -> Applications):**
  * `GET /api/job-postings/{job_id}/applications` ➔ List all applications submitted for a specific job opening.
  * `POST /api/job-postings/{job_id}/applications` ➔ Submit an application directly to a target job opening.
  * `GET /api/job-postings/{job_id}/applications/{id}` ➔ View specific application under a job posting.
  * `DELETE /api/job-postings/{job_id}/applications/{id}` ➔ Withdraw/delete application under a job posting.
* **Nested REST API Routes (Users -> Applications):**
  * `GET /api/users/{user_id}/applications` ➔ List all applications submitted by a specific student/user.
  * `POST /api/users/{user_id}/applications` ➔ Submit an application as a specific student/user.
  * `GET /api/users/{user_id}/applications/{id}` ➔ View user's specific application.
  * `DELETE /api/users/{user_id}/applications/{id}` ➔ Withdraw user's application.

---

## 🗄️ Database, Migrations & Seeding

The application uses **SQLAlchemy 2.0** with **Alembic** migrations and support for both PostgreSQL (in Docker) and SQLite (for standalone local development).

### 1. Environment Configuration (`.env`)
Copy the environment template:
```bash
cp .env.example .env
```
*(The `.env` file is git-ignored to prevent credential leaks).*

### 2. Running Database Migrations
Apply all schema changes:
```bash
alembic upgrade head
```

To create a new migration after editing models:
```bash
alembic revision --autogenerate -m "describe changes"
```

### 3. Database Seeding (Baseline & Factories)
Populate the database with baseline classroom records and realistic synthetic records generated via Faker:
```bash
# Seed default users (8) and announcements (4)
python3 seed.py

# Clean database first and seed custom batch sizes:
python3 seed.py --clean --users 15 --announcements 8
```

---

## 🚀 How to Run Locally

1. Navigate to the project directory:
   ```bash
   cd /Users/zsudedogan/.gemini/antigravity/scratch/fastapi-app
   ```

2. Activate virtual environment and install dependencies:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Launch server:
   ```bash
   python3 main.py
   ```

---

## 🌐 Interactive Web Interfaces

Open your browser to test each component:
* 🏛️ **Main Application Hub:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* 👥 **User Management Interface (View Layer):** [http://127.0.0.1:8000/users/](http://127.0.0.1:8000/users/)
* 📢 **Announcement Management Interface:** [http://127.0.0.1:8000/announcements/](http://127.0.0.1:8000/announcements/)
* 💼 **Job Postings Management Interface:** [http://127.0.0.1:8000/job-postings/](http://127.0.0.1:8000/job-postings/)
* 📝 **Applications Management Interface:** [http://127.0.0.1:8000/applications/](http://127.0.0.1:8000/applications/)
* 📖 **Swagger UI Documentation:** [http://127.0.0.1:8000/api/swagger](http://127.0.0.1:8000/api/swagger)

