# Classroom REST API - Week 04: Full MVC Architecture & Homework

This repository implements all classroom exercises and the complete homework assignment:
* **Item 5:** `GET .../users` ➔ listing (R), `POST .../users` ➔ creating (C), 2 routes with View Layer.
* **Item 6:** All CRUD operations on User route and controller with View Layer.
* **Homework Assignment:**
  * ✅ Create Announcement model (in-memory without database).
  * ✅ Create 2 controllers (`AnnouncementController` & `ApiAnnouncementController`).
  * ✅ Create routes for both controllers (`.../announcements/` and `.../api/announcements/`).
  * ✅ Create interactive Web Management Interface without database.
* **Swagger UI:** Categorized interactive API documentation at `/api/swagger`.

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
├── main.py                             # Main Application Entrypoint & Hub (Mounts all Routers)
│
├── models/                             # [M] MODEL LAYER (In-Memory without DB)
│   ├── __init__.py
│   ├── user.py                         # UserModel: In-memory store & CRUD methods
│   └── announcement.py                 # AnnouncementModel: In-memory store & CRUD methods (Homework)
│
├── views/                              # [V] VIEW LAYER (HTML Management Interfaces)
│   ├── __init__.py
│   ├── user_view.py                    # HTML View for User Management (Listing & Creating)
│   └── announcement_view.py            # HTML View for Announcement Management (Homework)
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

### 1. 👥 User Module (Items 5 & 6)
* **Web View Controller (`.../users/`):** [`controllers/user_controller.py`](./controllers/user_controller.py)
  * `GET /users/` ➔ Interactive HTML Management Interface:
    * **Listing (R):** Displays all users in a formatted table.
    * **Creating (C):** Web form to submit new users (`POST /users/`).
    * **Full CRUD:** Client-side edit (PUT/PATCH) and delete (DELETE) actions.
* **REST API Controller (`.../api/users/`):** [`controllers/api_user_controller.py`](./controllers/api_user_controller.py)
  * `GET /api/users/` ➔ Returns raw JSON user list.
  * `GET /api/users/{id}` ➔ Returns user by ID (or 404).
  * `POST /api/users/` ➔ Creates user (201 Created).
  * `PUT /api/users/{id}` ➔ Full update.
  * `PATCH /api/users/{id}` ➔ Partial update.
  * `DELETE /api/users/{id}` ➔ Deletes user.

### 2. 📢 Announcement Module (Homework Assignment)
* **Web View Controller (`.../announcements/`):** [`controllers/announcement_controller.py`](./controllers/announcement_controller.py)
  * `GET /announcements/` ➔ Interactive Web Management Interface:
    * Displays published announcements cards with badges.
    * Form to publish new announcements (Title, Content, Author, Category).
    * Inline buttons to Edit and Delete announcements.
* **REST API Controller (`.../api/announcements/`):** [`controllers/api_announcement_controller.py`](./controllers/api_announcement_controller.py)
  * Full JSON CRUD API for announcements.

---

## 🚀 How to Run

1. Navigate to the project directory:
   ```bash
   cd /Users/zsudedogan/.gemini/antigravity/scratch/fastapi-app
   ```

2. Activate virtual environment and install dependencies:
   ```bash
   source venv/bin/activate
   pip install fastapi "uvicorn[standard]" jinja2 python-multipart
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
* 📢 **Announcement Management Interface (Homework):** [http://127.0.0.1:8000/announcements/](http://127.0.0.1:8000/announcements/)
* 📖 **Swagger UI Documentation:** [http://127.0.0.1:8000/api/swagger](http://127.0.0.1:8000/api/swagger)
