# Classroom REST API - Week 03: Full Users CRUD & Swagger

This repository implements all the exercises from Week 03 of the classroom whiteboard.

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
2. Click **Import** (top left).
3. Select `postman_collection.json` from this folder.
4. You will see all 7 requests ready to test with pre-configured JSON payloads!

---

## 📖 Swagger UI (Item 7)

Open your browser and visit:
👉 **`http://127.0.0.1:8000/api/swagger`**
*(Also automatically redirects from `/docs`)*

You can execute all GET, POST, PUT, PATCH, and DELETE requests interactively directly in your browser.
