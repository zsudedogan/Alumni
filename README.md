# Classroom REST API - MVC Architecture & The Forgetting Test

This repository implements all classroom exercises, the complete homework assignment, and the container lifecycle experiment: **The Forgetting Test**.

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
├── docker-compose.yml                  # Docker Compose service definition
├── .dockerignore                       # Build context exclusion rules
├── forgetting_test.py                  # Automated script for The Forgetting Test
│
├── main.py                             # Main Application Entrypoint & Hub
│
├── models/                             # [M] MODEL LAYER (In-Memory without DB)
│   ├── __init__.py
│   ├── user.py                         # UserModel: In-memory store & CRUD methods
│   └── announcement.py                 # AnnouncementModel: In-memory store & CRUD methods
│
├── views/                              # [V] VIEW LAYER (HTML Management Interfaces)
│   ├── __init__.py
│   ├── user_view.py                    # HTML View for User Management (Listing & Creating)
│   └── announcement_view.py            # HTML View for Announcement Management
│
├── controllers/                        # [C] CONTROLLER LAYER
│   ├── __init__.py
│   ├── user_controller.py              # UserController: Handles .../users/ with View Layer
│   ├── api_user_controller.py          # ApiUserController: Handles .../api/users/ (JSON REST API)
│   ├── announcement_controller.py      # AnnouncementController: Handles .../announcements/ with View Layer
│   └── api_announcement_controller.py  # ApiAnnouncementController: Handles .../api/announcements/ (JSON)
│
├── postman_collection.json             # Postman Test Suite (Users & Announcements)
├── requirements.txt                    # Project Dependencies
├── test_api.py                         # Automated Test Suite
└── README.md                           # Documentation & Architecture Guide
```

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
* 📖 **Swagger UI Documentation:** [http://127.0.0.1:8000/api/swagger](http://127.0.0.1:8000/api/swagger)
