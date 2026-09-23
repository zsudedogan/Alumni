# Classroom API Assignment: Web Routes Implementation

This project implements all the web routes and concepts written on the whiteboard during class.

---

## 📋 Whiteboard Route Mapping

| # | HTTP Method | Endpoint | Expected Output / Behavior | Example |
|---|---|---|---|---|
| **1** | `GET` | `/` | `"ok"` | `http://localhost:8000/` |
| **2** | `GET` | `/hello` | `"Hello, World!"` | `http://localhost:8000/hello` |
| **3** | `GET` | `/hello/{name}` | `"Hello, Emre!"` (personalized greeting) | `http://localhost:8000/hello/emre` |
| **4** | `GET` | `/sum/{number1}/{number2}` | Returns sum of the two numbers | `http://localhost:8000/sum/15/25` -> `40` |
| **5** | `GET` | `/main` | Temporary main page (HTML landing page) | `http://localhost:8000/main` |
| **Top** | `GET` | `/alumni` | List of alumni records | `http://localhost:8000/alumni` |
| **Top** | `POST` | `/alumni` | Add a new alumni record | POST JSON body to `/alumni` |
| **Top** | `GET` | `/auto` | List of vehicle records | `http://localhost:8000/auto` |
| **Top** | `POST` | `/auto` | Add a new vehicle record | POST JSON body to `/auto` |

---

## 🚀 Quick Start Guide (FastAPI - Recommended)

The whiteboard features route parameter syntax `{name}`, `{number1}/{number2}`, and Swagger UI references (`/docs`), which directly correspond to **FastAPI**.

### 1. Prerequisites & Setup

Open your terminal, navigate to the project directory, and create a virtual environment:

```bash
cd /Users/zsudedogan/.gemini/antigravity/scratch/fastapi-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Server

Start the development server using **Uvicorn**:

```bash
uvicorn main:app --reload --port 8000
```
Or simply run:
```bash
python3 main.py
```

The server will be running at: **`http://127.0.0.1:8000`**

---

## 🔍 How to Test Each Route

### Route 1: Health / Status Check
- **URL**: `http://localhost:8000/`
- **Method**: `GET`
- **Response**:
  ```text
  ok
  ```

### Route 2: Default Greeting
- **URL**: `http://localhost:8000/hello`
- **Method**: `GET`
- **Response**:
  ```text
  Hello, World!
  ```

### Route 3: Personalized Greeting with Path Parameter
- **URL**: `http://localhost:8000/hello/emre`
- **Method**: `GET`
- **Response**:
  ```text
  Hello, Emre!
  ```
  *(Note: The code automatically formats and capitalizes the input parameter name)*

### Route 4: Sum of Two Numbers
- **URL**: `http://localhost:8000/sum/10/25`
- **Method**: `GET`
- **Response (JSON)**:
  ```json
  {
    "number1": 10,
    "number2": 25,
    "sum": 35,
    "message": "The sum of 10 and 25 is 35"
  }
  ```

### Route 5: Temporary Main Page
- **URL**: `http://localhost:8000/main`
- **Method**: `GET`
- **Response**: An interactive, responsive HTML page listing all endpoints and documentation links.

---

## 🎓 Alumni & Auto Endpoints (Top Section)

### Get All Alumni
```bash
curl -X GET http://localhost:8000/alumni
```

### Create a New Alumnus
```bash
curl -X POST http://localhost:8000/alumni \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Ahmet Yildiz", "department": "Computer Science", "graduation_year": 2022}'
```

### Get All Autos
```bash
curl -X GET http://localhost:8000/auto
```

### Add a New Auto
```bash
curl -X POST http://localhost:8000/auto \
  -H "Content-Type: application/json" \
  -d '{"brand": "BMW", "model": "320i", "year": 2022, "color": "Blue"}'
```

---

## 📖 Interactive Documentation (Swagger UI)

FastAPI automatically generates interactive API documentation. While your server is running, open:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

You can test all endpoints, path parameters, and request bodies directly from this interface!

---

## 🐍 Flask Alternative

If your teacher preferred **Flask**, run:
```bash
pip install flask
python3 flask_app.py
```
Flask runs by default on: **`http://127.0.0.1:5000`**
