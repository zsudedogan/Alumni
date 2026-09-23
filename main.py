"""
Classroom Web API Assignment
All routes from the whiteboard implementation using FastAPI.
"""

from typing import List, Optional
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel

# Initialize the FastAPI application
app = FastAPI(
    title="Classroom Routes Demo",
    description="Implementation of the routes from the classroom whiteboard in FastAPI.",
    version="1.0.0"
)

# ---------------------------------------------------------
# Pydantic Models (Schemas for POST requests)
# ---------------------------------------------------------
class Alumni(BaseModel):
    id: Optional[int] = None
    full_name: str
    department: str
    graduation_year: int
    email: Optional[str] = None


class Auto(BaseModel):
    id: Optional[int] = None
    brand: str
    model: str
    year: int
    color: Optional[str] = None


# In-memory mock databases
alumni_db: List[Alumni] = [
    Alumni(id=1, full_name="Emre Yilmaz", department="Computer Engineering", graduation_year=2023, email="emre@example.com"),
    Alumni(id=2, full_name="Sude Dogan", department="Software Engineering", graduation_year=2024, email="sude@example.com"),
]

auto_db: List[Auto] = [
    Auto(id=1, brand="Toyota", model="Corolla", year=2021, color="White"),
    Auto(id=2, brand="Tesla", model="Model 3", year=2023, color="Red"),
]


# ---------------------------------------------------------
# Whiteboard Routes 1 to 5
# ---------------------------------------------------------

# 1. GET / -> "ok"
@app.get(
    "/",
    response_class=PlainTextResponse,
    summary="Route 1: Status check",
    tags=["Classroom Exercises"]
)
async def root():
    """
    Route 1:
    Returns simple text "ok"
    """
    return "ok"


# 2. GET /hello -> "Hello, World!"
@app.get(
    "/hello",
    response_class=PlainTextResponse,
    summary="Route 2: Basic greeting",
    tags=["Classroom Exercises"]
)
async def say_hello():
    """
    Route 2:
    Returns the standard greeting "Hello, World!"
    """
    return "Hello, World!"


# 3. GET /hello/{name} -> "Hello, Emre!" (e.g. /hello/emre)
@app.get(
    "/hello/{name}",
    response_class=PlainTextResponse,
    summary="Route 3: Personalized greeting",
    tags=["Classroom Exercises"]
)
async def say_hello_name(name: str):
    """
    Route 3:
    Takes a path parameter `name` and returns "Hello, {name}!"
    Capitalizes the name properly (e.g., 'emre' -> 'Hello, Emre!').
    """
    formatted_name = name.strip().capitalize()
    return f"Hello, {formatted_name}!"


# 4. GET /sum/{number1}/{number2} -> sum of numbers
@app.get(
    "/sum/{number1}/{number2}",
    summary="Route 4: Calculate sum of two numbers",
    tags=["Classroom Exercises"]
)
async def calculate_sum(number1: int, number2: int):
    """
    Route 4:
    Takes two integer path parameters and computes their sum.
    Returns both the numeric result and a formatted message.
    """
    total = number1 + number2
    return {
        "number1": number1,
        "number2": number2,
        "sum": total,
        "message": f"The sum of {number1} and {number2} is {total}"
    }


# 5. GET /main (or /page) -> "temporary one main page"
@app.get(
    "/main",
    response_class=HTMLResponse,
    summary="Route 5: Temporary main page",
    tags=["Classroom Exercises"]
)
async def temporary_main_page():
    """
    Route 5:
    Returns a temporary HTML main page.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Temporary Main Page</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #f8fafc;
                color: #1e293b;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }
            .card {
                background: white;
                padding: 2.5rem;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
                max-width: 520px;
                width: 90%;
            }
            h1 {
                font-size: 1.75rem;
                color: #0f172a;
                margin-top: 0;
            }
            p {
                color: #64748b;
                line-height: 1.6;
            }
            ul {
                list-style: none;
                padding: 0;
            }
            li {
                margin: 10px 0;
            }
            a {
                display: inline-block;
                color: #2563eb;
                text-decoration: none;
                font-weight: 500;
                padding: 6px 12px;
                background: #eff6ff;
                border-radius: 6px;
                transition: background 0.2s;
            }
            a:hover {
                background: #dbeafe;
            }
            .badge {
                font-size: 0.75rem;
                background: #e2e8f0;
                color: #475569;
                padding: 2px 6px;
                border-radius: 4px;
                margin-left: 6px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 Temporary Main Page</h1>
            <p>Welcome! This is the temporary main landing page served by the API.</p>
            <h3>Available Endpoints:</h3>
            <ul>
                <li><a href="/">GET /</a> <span class="badge">returns "ok"</span></li>
                <li><a href="/hello">GET /hello</a> <span class="badge">"Hello, World!"</span></li>
                <li><a href="/hello/emre">GET /hello/emre</a> <span class="badge">"Hello, Emre!"</span></li>
                <li><a href="/sum/15/25">GET /sum/15/25</a> <span class="badge">Sum: 40</span></li>
                <li><a href="/alumni">GET /alumni</a> <span class="badge">Alumni list</span></li>
                <li><a href="/auto">GET /auto</a> <span class="badge">Auto list</span></li>
                <li><a href="/docs" target="_blank">GET /docs</a> <span class="badge">Swagger UI Docs</span></li>
            </ul>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# ---------------------------------------------------------
# Top Section of Whiteboard: Alumni & Auto (GET & POST)
# ---------------------------------------------------------

# Alumni Endpoints
@app.get(
    "/alumni",
    response_model=List[Alumni],
    summary="Get all alumni members",
    tags=["Alumni"]
)
async def get_alumni():
    """
    (GET) http://localhost:8000/alumni
    Retrieves the list of all alumni.
    """
    return alumni_db


@app.post(
    "/alumni",
    response_model=Alumni,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new alumni member",
    tags=["Alumni"]
)
async def create_alumni(alumni: Alumni):
    """
    (POST) http://localhost:8000/alumni
    Adds a new alumni member to the database.
    """
    new_id = len(alumni_db) + 1
    alumni.id = new_id
    alumni_db.append(alumni)
    return alumni


# Auto Endpoints
@app.get(
    "/auto",
    response_model=List[Auto],
    summary="Get all vehicles",
    tags=["Auto"]
)
async def get_autos():
    """
    (GET) http://localhost:8000/auto
    Retrieves the list of all vehicles.
    """
    return auto_db


@app.post(
    "/auto",
    response_model=Auto,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new vehicle",
    tags=["Auto"]
)
async def create_auto(auto: Auto):
    """
    (POST) http://localhost:8000/auto
    Adds a new vehicle to the database.
    """
    new_id = len(auto_db) + 1
    auto.id = new_id
    auto_db.append(auto)
    return auto


# ---------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    # Run server locally on port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
