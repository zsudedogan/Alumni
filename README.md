# Classroom REST API - Week 03 & 04: Full Users CRUD, Swagger & MVC Architecture

This repository implements all the exercises from the classroom whiteboard, featuring a full RESTful CRUD API, Swagger documentation, and an architectural design based on the **MVC (Model-View-Controller)** pattern.

---

## 🏛️ MVC (Model-View-Controller) Architecture Documentation

The **MVC (Model-View-Controller)** pattern is an architectural design pattern that separates an application into three interconnected components. In this REST API application, the responsibilities are decoupled as follows:

```
  +-------------------------------------------------------------+
  |                        CLIENT                               |
  |             (Postman, Web Browser, Swagger UI)              |
  +-------------------------------------------------------------+
                               |    ^
                1. HTTP Request|    | 4. HTTP Response (JSON/HTML)
                               v    |
  +-------------------------------------------------------------+
  |                      CONTROLLER                             |
  |                (Route Handlers / Endpoints)                 |
  |   - Parses incoming requests & path parameters              |
  |   - Validates incoming payload using Schemas                |
  |   - Coordinates business logic & CRUD operations            |
  +-------------------------------------------------------------+
               |                                ^
  2. Read/Write|                                | 3. Validated Data
               v                                |
  +--------------------------+    +-----------------------------+
  |          MODEL           |    |            VIEW             |
  | (Data Entities & Store)  |--->|    (Presentation Layer)     |
  | - Pydantic Data Models   |    | - JSON Response Format      |
  | - Data validation rules  |    | - HTTP Status Codes (201,   |
  | - In-memory Database     |    |   404, 200, etc.)           |
  |   (users_db, next_id)    |    | - Swagger UI Documentation  |
  +--------------------------+    +-----------------------------+
```

---

### 📂 Directory & File Structure (Tree View)

```text
fastapi-app/
│
├── main.py                             # Application Entrypoint (Mounts Controllers & Swagger)
│
├── models/                             # [M] MODEL LAYER
│   ├── __init__.py
│   └── user.py                         # UserModel with In-Memory CRUD functions & Schemas
│
├── controllers/                        # [C] CONTROLLER LAYER
│   ├── __init__.py
│   ├── user_controller.py              # UserController (CRUD operations for /users)
│   └── api_user_controller.py          # ApiUserController (CRUD operations for /api/users)
│
├── postman_collection.json             # Postman Test Suite (API Client)
├── requirements.txt                    # Python Dependencies
├── test_api.py                         # Automated Integration Tests
├── README.md                           # System Architecture & API Documentation
└── flask_app.py                        # Alternative Framework Reference
```

---

### 🧱 Detailed MVC Component Breakdown

#### 1. 🗄️ Model Layer (M)
* **Definition:** Responsible for data representation, data structures, state management, and business validation rules.
* **Location in Code:** Defined within `main.py` under the data schemas section:
  * `UserBase`: Base entity defining core fields (`name: str`, `age: Optional[int]`, `email: Optional[str]`).
  * `UserCreate`: Schema for incoming user creation data.
  * `UserUpdate`: Schema for full updates via `PUT`.
  * `UserPatch`: Schema for partial updates via `PATCH` (all fields optional).
  * `User`: Model representing the stored user entity, including the system-assigned `id: int`.
  * `users_db`: In-memory storage acting as the temporary database repository (`users_db: List[User]`).
  * `next_user_id`: Auto-incrementing identifier counter.

#### 2. 👁️ View Layer (V)
* **Definition:** Responsible for how data is presented, formatted, and exposed to the client.
* **In REST APIs:** The View is not a set of traditional HTML pages; it is the **structured JSON representation**, **HTTP status codes**, and **API documentation interfaces**.
  * **JSON Responses:** Automatic serialization of `User` models into JSON payloads.
  * **HTTP Status Codes:** Semantic HTTP response codes:
    * `200 OK`: Successful retrieval, update, or deletion.
    * `201 Created`: Successful resource creation on `POST /api/users`.
    * `404 Not Found`: Meaningful error response when a requested resource does not exist.
  * **Swagger UI Documentation:** Accessible at `/api/swagger`, providing an interactive visual representation of all API endpoints and schemas.
  * **HTML View (`/main`):** An aesthetic landing page rendered via `HTMLResponse`.

#### 3. 🎮 Controller Layer (C)
* **Definition:** Acts as the intermediary between the client, the Model, and the View. It intercepts HTTP requests, extracts parameters, coordinates business operations, and directs the response.
* **Location in Code:** The endpoint functions decorated with `@app` routes:
  * `health_check()`: Controller for `GET /api/health`.
  * `create_user(user_in: UserCreate)`: Controller for `POST /api/users`. Validates input, assigns an incremental ID, inserts the entity into `users_db`, and returns the created resource.
  * `list_users()`: Controller for `GET /api/users`. Reads all entities from storage.
  * `get_user_by_id(id: int)`: Controller for `GET /api/users/{id}`. Finds by ID or raises 404.
  * `update_user_put(id: int, user_in: UserUpdate)`: Controller for `PUT /api/users/{id}`. Overwrites entity fields.
  * `update_user_patch(id: int, user_in: UserPatch)`: Controller for `PATCH /api/users/{id}`. Partially updates fields.
  * `delete_user(id: int)`: Controller for `DELETE /api/users/{id}`. Removes entity by ID.

---

### 📊 Summary Table of MVC Architecture Mapping

| Component | Architecture Role | File / Location | Responsibility |
|---|---|---|---|
| **Model** | Data & State | `main.py` (`User`, `UserBase`, `users_db`) | Defines data schemas, type constraints, and in-memory persistence. |
| **View** | Presentation | `main.py` (`response_model`, status codes, `/api/swagger`) | Serializes JSON responses, emits HTTP statuses, generates Swagger docs. |
| **Controller** | Logic & Routing | `main.py` (Functions decorated with `@app.get/post/put/patch/delete`) | Receives client requests, processes input, interacts with models, returns views. |
| **Client** | Consumer / Tester | `postman_collection.json`, Swagger UI | Sends HTTP requests and inspects server responses. |
| **Testing** | Verification | `test_api.py` | Automated tests verifying Controller-Model-View integration. |

---

## 📋 Week 03 Whiteboard Items & Endpoints

| # | HTTP Method | Endpoint | Request Body | Description |
|---|---|---|---|---|
| **1** | `GET` | `/api/health` | None | Returns JSON system health status (`{"status": "UP"}`) |
| **2** | - | *Install Postman* | - | Included `postman_collection.json` ready for 1-click import |
| **3** | `POST` | `/api/users` | `{"name": "...", "age": 24, "email": "..."}` | Creates new user in-memory ("what you sent comes back") |
| **4** | `GET` | `/api/users` | None | Lists all users |
| **4b**| `GET` | `/api/users/{id}` | None | Retrieves single user by ID (or 404 if not found) |
| **5** | `PUT` | `/api/users/{id}` | Full User object | Completely updates user fields |
| **5** | `PATCH` | `/api/users/{id}` | Partial fields (e.g. `{"age": 25}`) | Partially updates specified user fields |
| **6** | `DELETE`| `/api/users/{id}` | None | Removes user from memory (or 404 if not found) |
| **7** | `GET` | `/api/swagger` | None | Interactive Swagger UI API documentation |

---

## 🚀 Running the API

1. Navigate to the project directory:
   ```bash
   cd /Users/zsudedogan/.gemini/antigravity/scratch/fastapi-app
   ```

2. Activate virtual environment and install dependencies:
   ```bash
   source venv/bin/activate
   pip install fastapi "uvicorn[standard]"
   ```

3. Start server:
   ```bash
   python3 main.py
   ```
   *(or `uvicorn main:app --reload --port 8000`)*

API will be live at: **`http://127.0.0.1:8000`**

---

## 📮 Testing with Postman (Item 2)

A pre-built Postman collection is included in this repository:
[`postman_collection.json`](./postman_collection.json)

1. Open **Postman**.
2. Press **`Cmd + O`** (or drag and drop `postman_collection.json` into Postman).
3. You will see all 7 requests ready to test with pre-configured JSON payloads!

---

## 📖 Swagger UI (Item 7)

Open your browser and visit:
👉 **`http://127.0.0.1:8000/api/swagger`**
*(Also automatically redirects from `/docs`)*
