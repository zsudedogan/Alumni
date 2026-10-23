# Classroom Web API Homework - Step-by-Step Submission Report
**Course:** Web API & MVC Architecture  
**Student:** Z. Sude Doğan  
**Repository:** [https://github.com/zsudedogan/Alumni](https://github.com/zsudedogan/Alumni)

---

## 📋 Summary of Completed Assignment Steps

| Step | Task Description | Status | Key Output / Files |
| :--- | :--- | :---: | :--- |
| **Step 1** | Update `ddd.md` with `job-postings` table | ✅ Completed | [ddd.md](file:///Users/zsudedogan/.gemini/antigravity/scratch/fastapi-app/ddd.md) (ERD, data dictionary, schema constraints) |
| **Step 2** | Create Alembic migration file for `job_postings` | ✅ Completed | `alembic/versions/ed325ba68409_create_job_postings_table.py` |
| **Step 3** | Define models & relationships, run migration | ✅ Completed | `models/db_entities.py`, `models/job_posting.py`, `alembic upgrade head` |
| **Step 4** | Define direct and nested routes for job postings | ✅ Completed | `controllers/api_job_posting_controller.py`, `controllers/job_posting_controller.py` |
| **Step 5** | Repeat Steps 1–4 for `applications` table | ✅ Completed | `ddd.md`, `alembic/versions/1fe5ae6806fb_create_applications_table.py`, `models/application.py`, `controllers/api_application_controller.py` |
| **Step 6** | Seed `job_postings` table using Faker factory | ✅ Completed | `factories/job_posting_factory.py`, `seed.py` |
| **Step 7** | Prepare Basic UIs for Job Postings and Applications | ✅ Completed | `views/job_posting_view.py` (`/job-postings/`), `views/application_view.py` (`/applications/`) |

---

## 🛠️ Step-by-Step Technical Documentation

### Step 1: Update `ddd.md` (Job-Postings Table)
- **File:** `ddd.md`
- **Actions:**
  - Added Entity-Relationship Diagram (ERD) with Mermaid syntax showing `users.id` (1) ➔ `job_postings.user_id` (N).
  - Defined table schema: `id`, `title`, `company`, `location`, `job_type`, `description`, `requirements`, `salary_range`, `application_deadline`, `contact_email`, `is_active`, `user_id`, `created_at`, `updated_at`.
  - Added Data Dictionary with data types, nullability, defaults, and foreign key definitions.
  - Specified Pydantic DTO schemas (`JobPostingCreate`, `JobPostingUpdate`, `JobPostingPatch`, `JobPostingResponse`).

---

### Step 2: Create Alembic Migration File (`job_postings`)
- **File:** `alembic/versions/ed325ba68409_create_job_postings_table.py`
- **Actions:**
  - Generated revision script using Alembic with `upgrade()` and `downgrade()` routines.
  - Configured PostgreSQL / SQLite compatible column definitions, indexes (`title`, `company`), and foreign key constraint pointing to `users.id` with `ondelete="CASCADE"`.

---

### Step 3: Define Models & Relationships and Run Migration
- **Files:**
  - `models/db_entities.py` (SQLAlchemy ORM Entities)
  - `models/job_posting.py` (Repository Model & Pydantic DTOs)
- **Relationships Defined:**
  - `UserEntity.job_postings = relationship("JobPostingEntity", back_populates="creator", cascade="all, delete-orphan")`
  - `JobPostingEntity.creator = relationship("UserEntity", back_populates="job_postings")`
- **Migration Command Executed:**
  ```bash
  alembic upgrade head
  ```
  *(Verified table creation in database schema).*

---

### Step 4: Define Direct & Nested Routes (`job_postings`)
- **Files:**
  - `controllers/api_job_posting_controller.py`
  - `controllers/job_posting_controller.py`
- **Direct REST API Routes (`/api/job-postings`):**
  - `GET /api/job-postings`: List all jobs (supports `active_only`, `user_id` filters)
  - `GET /api/job-postings/{id}`: Retrieve single job
  - `POST /api/job-postings`: Create job posting (HTTP 201)
  - `PUT /api/job-postings/{id}`: Full update (HTTP 200)
  - `PATCH /api/job-postings/{id}`: Partial update (HTTP 200)
  - `DELETE /api/job-postings/{id}`: Delete job posting (HTTP 200)
- **Nested REST API Routes (`/api/users/{user_id}/job-postings`):**
  - Demonstrates 1-to-many relationship:
    - `GET /api/users/{user_id}/job-postings`: List jobs published by a specific user
    - `POST /api/users/{user_id}/job-postings`: Create a job automatically bound to that user

---

### Step 5: Repeat Steps 1–4 for `applications` Table
- **Step 5.1 (DDD):** Updated `ddd.md` with `applications` schema, linking `job_postings.id` and `users.id`.
- **Step 5.2 (Migration):** Created Alembic migration `alembic/versions/1fe5ae6806fb_create_applications_table.py` with foreign keys to `job_postings` and `users`.
- **Step 5.3 (Models):**
  - `ApplicationEntity` in `models/db_entities.py` with bidirectional relationships to `UserEntity` and `JobPostingEntity`.
  - `ApplicationModel` and Pydantic schemas in `models/application.py`.
- **Step 5.4 (Direct & Nested Routes):**
  - Direct: `/api/applications` (GET, POST, GET/{id}, PUT/{id}, PATCH/{id}, DELETE/{id})
  - Nested Route 1: `/api/job-postings/{job_id}/applications` (List & submit applications under a specific job)
  - Nested Route 2: `/api/users/{user_id}/applications` (List & manage applications submitted by a specific student/user)

---

### Step 6: Seed `job_postings` Table (Faker Factory & Seeder)
- **Files:**
  - `factories/job_posting_factory.py` (Implements realistic Faker seed generator with positions, tech stacks, salaries, Turkish & Global company names)
  - `seed.py` (Command-line database seeder)
- **Execution Command:**
  ```bash
  python3 seed.py --jobs 10
  ```
  *(Seeded baseline records and synthetic job postings into database).*

---

### Step 7: Basic UIs for Job Postings & Applications (MVC View Layer)
- **Job Postings UI (`/job-postings/`):**
  - Stat counters: Total Positions, Active Listings, Internships, Full-time Roles.
  - Instant JavaScript filters: *All Positions*, *Internships*, *Full-time*, *Remote Roles*.
  - Job card listing with details, salary, deadline, and inline delete button.
  - "📝 Apply to this Job" button linking directly to the application form with pre-selected `job_id`.
  - Form to publish new opportunities with dynamic Recruiter User dropdown.
- **Applications UI (`/applications/`):**
  - Stat counters: Total, Pending, Reviewed, Accepted/Shortlisted, Rejected.
  - Interactive status badges and status update dropdown calling `PATCH /api/applications/{id}` dynamically.
  - Application submission form with populated `<select>` dropdowns for both Open Positions and Registered Candidates.
  - Automatic URL query binding (`/applications/?job_id=3#apply-form`) that pre-selects the position and highlights the form.

---

### 🧪 Automated Test Verification
- All 16 automated tests passed:
  ```bash
  pytest -v
  ```
- Tests covering all requested steps:
  - `test_8_direct_job_postings_crud`: PASSED
  - `test_9_nested_user_job_postings`: PASSED
  - `test_10_job_postings_web_view`: PASSED
  - `test_11_direct_applications_crud`: PASSED
  - `test_12_nested_job_applications`: PASSED
  - `test_13_nested_user_applications`: PASSED
  - `test_14_applications_web_view`: PASSED
