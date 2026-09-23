"""
Classroom Web API Assignment - Flask Version
All routes from the whiteboard implementation using Flask.
"""

from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# In-memory mock database
alumni_db = [
    {"id": 1, "full_name": "Emre Yilmaz", "department": "Computer Engineering", "graduation_year": 2023, "email": "emre@example.com"},
    {"id": 2, "full_name": "Sude Dogan", "department": "Software Engineering", "graduation_year": 2024, "email": "sude@example.com"},
]

auto_db = [
    {"id": 1, "brand": "Toyota", "model": "Corolla", "year": 2021, "color": "White"},
    {"id": 2, "brand": "Tesla", "model": "Model 3", "year": 2023, "color": "Red"},
]

# ---------------------------------------------------------
# Whiteboard Routes 1 to 5
# ---------------------------------------------------------

# 1. GET / -> "ok"
@app.route("/", methods=["GET"])
def root():
    return "ok"


# 2. GET /hello -> "Hello, World!"
@app.route("/hello", methods=["GET"])
def hello():
    return "Hello, World!"


# 3. GET /hello/{name} -> "Hello, Emre!"
@app.route("/hello/<name>", methods=["GET"])
def hello_name(name):
    formatted_name = name.strip().capitalize()
    return f"Hello, {formatted_name}!"


# 4. GET /sum/{number1}/{number2}
@app.route("/sum/<int:number1>/<int:number2>", methods=["GET"])
def calculate_sum(number1, number2):
    total = number1 + number2
    return jsonify({
        "number1": number1,
        "number2": number2,
        "sum": total,
        "message": f"The sum of {number1} and {number2} is {total}"
    })


# 5. GET /main -> temporary one main page
@app.route("/main", methods=["GET"])
def temporary_main_page():
    html_template = """
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
            h1 { font-size: 1.75rem; color: #0f172a; margin-top: 0; }
            p { color: #64748b; line-height: 1.6; }
            ul { list-style: none; padding: 0; }
            li { margin: 10px 0; }
            a {
                display: inline-block;
                color: #2563eb;
                text-decoration: none;
                font-weight: 500;
                padding: 6px 12px;
                background: #eff6ff;
                border-radius: 6px;
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
            <p>Welcome! This is the temporary main landing page served by Flask.</p>
            <h3>Available Endpoints:</h3>
            <ul>
                <li><a href="/">GET /</a> <span class="badge">returns "ok"</span></li>
                <li><a href="/hello">GET /hello</a> <span class="badge">"Hello, World!"</span></li>
                <li><a href="/hello/emre">GET /hello/emre</a> <span class="badge">"Hello, Emre!"</span></li>
                <li><a href="/sum/15/25">GET /sum/15/25</a> <span class="badge">Sum: 40</span></li>
                <li><a href="/alumni">GET /alumni</a> <span class="badge">Alumni list</span></li>
                <li><a href="/auto">GET /auto</a> <span class="badge">Auto list</span></li>
            </ul>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)


# ---------------------------------------------------------
# Alumni & Auto (GET & POST)
# ---------------------------------------------------------

@app.route("/alumni", methods=["GET"])
def get_alumni():
    return jsonify(alumni_db)


@app.route("/alumni", methods=["POST"])
def create_alumni():
    data = request.get_json() or {}
    new_id = len(alumni_db) + 1
    new_item = {
        "id": new_id,
        "full_name": data.get("full_name", "Anonymous"),
        "department": data.get("department", "General"),
        "graduation_year": data.get("graduation_year", 2024),
        "email": data.get("email", "")
    }
    alumni_db.append(new_item)
    return jsonify(new_item), 201


@app.route("/auto", methods=["GET"])
def get_autos():
    return jsonify(auto_db)


@app.route("/auto", methods=["POST"])
def create_auto():
    data = request.get_json() or {}
    new_id = len(auto_db) + 1
    new_item = {
        "id": new_id,
        "brand": data.get("brand", "Unknown"),
        "model": data.get("model", "Unknown"),
        "year": data.get("year", 2024),
        "color": data.get("color", "Black")
    }
    auto_db.append(new_item)
    return jsonify(new_item), 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
