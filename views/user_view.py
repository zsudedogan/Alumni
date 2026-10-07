"""
User View - MVC Architecture
Renders the HTML View Layer for User Management Interface (Whiteboard Items 5 & 6).
"""

from typing import List
from models.user import User


def render_user_management_page(users: List[User]) -> str:
    """
    Renders an interactive HTML view for listing users (R) and creating users (C),
    with full client-side actions for edit (PUT/PATCH) and delete (D).
    """
    user_rows = ""
    for u in users:
        age_display = u.age if u.age is not None else "-"
        email_display = u.email if u.email else "-"
        user_rows += f"""
        <tr id="user-row-{u.id}">
            <td><strong>#{u.id}</strong></td>
            <td>{u.name}</td>
            <td>{age_display}</td>
            <td>{email_display}</td>
            <td class="actions">
                <button class="btn btn-sm btn-edit" onclick="editUser({u.id}, '{u.name}', {u.age or 0}, '{u.email or ''}')">Edit</button>
                <button class="btn btn-sm btn-delete" onclick="deleteUser({u.id})">Delete</button>
            </td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>User Management - View Layer</title>
        <style>
            :root {{
                --primary: #3b82f6;
                --primary-dark: #1d4ed8;
                --success: #10b981;
                --danger: #ef4444;
                --bg: #f8fafc;
                --card: #ffffff;
                --text: #0f172a;
                --text-muted: #64748b;
                --border: #e2e8f0;
            }}
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: var(--bg);
                color: var(--text);
                padding: 2rem 1rem;
                line-height: 1.5;
            }}
            .container {{ max-width: 960px; margin: 0 auto; }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 2rem;
                flex-wrap: wrap;
                gap: 1rem;
            }}
            .nav-links a {{
                color: var(--primary);
                text-decoration: none;
                font-weight: 500;
                margin-left: 1rem;
                padding: 0.4rem 0.8rem;
                border-radius: 6px;
                background: #eff6ff;
            }}
            .nav-links a:hover {{ background: #dbeafe; }}
            .grid {{ display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; }}
            @media (max-width: 768px) {{ .grid {{ grid-template-columns: 1fr; }} }}
            .card {{
                background: var(--card);
                border-radius: 12px;
                padding: 1.5rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
                border: 1px solid var(--border);
            }}
            h2 {{ font-size: 1.25rem; margin-bottom: 1rem; color: #1e293b; }}
            .form-group {{ margin-bottom: 1rem; }}
            label {{ display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.25rem; color: var(--text-muted); }}
            input {{
                width: 100%;
                padding: 0.6rem 0.8rem;
                border: 1px solid var(--border);
                border-radius: 6px;
                font-size: 0.95rem;
            }}
            input:focus {{ outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2); }}
            .btn {{
                display: inline-block;
                padding: 0.6rem 1.2rem;
                font-size: 0.95rem;
                font-weight: 500;
                border-radius: 6px;
                border: none;
                cursor: pointer;
                transition: background 0.2s;
            }}
            .btn-primary {{ background: var(--primary); color: white; width: 100%; }}
            .btn-primary:hover {{ background: var(--primary-dark); }}
            .btn-sm {{ padding: 0.3rem 0.6rem; font-size: 0.8rem; }}
            .btn-edit {{ background: #fef3c7; color: #92400e; }}
            .btn-edit:hover {{ background: #fde68a; }}
            .btn-delete {{ background: #fee2e2; color: #b91c1c; }}
            .btn-delete:hover {{ background: #fecaca; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 0.75rem; text-align: left; border-bottom: 1px solid var(--border); }}
            th {{ font-size: 0.8rem; text-transform: uppercase; color: var(--text-muted); background: #f1f5f9; }}
            .badge {{
                display: inline-block;
                padding: 0.2rem 0.5rem;
                font-size: 0.75rem;
                font-weight: 600;
                border-radius: 4px;
                background: #e0f2fe;
                color: #0369a1;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div>
                    <h1>👥 User Management Interface</h1>
                    <p style="color: var(--text-muted); font-size: 0.9rem;">
                        MVC View Layer: <span class="badge">Listing (R)</span> & <span class="badge">Creating (C)</span> via <code>.../users/</code>
                    </p>
                </div>
                <div class="nav-links">
                    <a href="/announcements/">📢 Announcements</a>
                    <a href="/api/swagger" target="_blank">📖 Swagger Docs</a>
                    <a href="/api/users" target="_blank">🔗 JSON API</a>
                </div>
            </div>

            <div class="grid">
                <!-- FORM: Create / Edit User -->
                <div class="card">
                    <h2 id="form-title">➕ Create User (C)</h2>
                    <form id="user-form" onsubmit="handleFormSubmit(event)">
                        <input type="hidden" id="user-id" value="">
                        <div class="form-group">
                            <label for="name">Full Name *</label>
                            <input type="text" id="name" required placeholder="e.g. John Doe">
                        </div>
                        <div class="form-group">
                            <label for="age">Age</label>
                            <input type="number" id="age" placeholder="e.g. 24">
                        </div>
                        <div class="form-group">
                            <label for="email">Email Address</label>
                            <input type="email" id="email" placeholder="e.g. john@example.com">
                        </div>
                        <button type="submit" class="btn btn-primary" id="submit-btn">Save User</button>
                        <button type="button" class="btn" style="background:#e2e8f0; width:100%; margin-top:0.5rem; display:none;" id="cancel-btn" onclick="resetForm()">Cancel Edit</button>
                    </form>
                </div>

                <!-- TABLE: List Users -->
                <div class="card">
                    <h2>📋 User Directory (R)</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Age</th>
                                <th>Email</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="user-table-body">
                            {user_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <script>
            async function handleFormSubmit(e) {{
                e.preventDefault();
                const id = document.getElementById('user-id').value;
                const name = document.getElementById('name').value;
                const age = document.getElementById('age').value ? parseInt(document.getElementById('age').value) : null;
                const email = document.getElementById('email').value || null;

                const payload = {{ name, age, email }};

                if (id) {{
                    // Update (PUT)
                    const res = await fetch(`/users/${{id}}`, {{
                        method: 'PUT',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }});
                    if (res.ok) window.location.reload();
                    else alert('Update failed');
                }} else {{
                    // Create (POST)
                    const res = await fetch('/users/', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }});
                    if (res.ok) window.location.reload();
                    else alert('Creation failed');
                }}
            }}

            function editUser(id, name, age, email) {{
                document.getElementById('user-id').value = id;
                document.getElementById('name').value = name;
                document.getElementById('age').value = age || '';
                document.getElementById('email').value = email || '';
                document.getElementById('form-title').innerText = '✏️ Edit User #' + id;
                document.getElementById('submit-btn').innerText = 'Update User';
                document.getElementById('cancel-btn').style.display = 'block';
            }}

            function resetForm() {{
                document.getElementById('user-form').reset();
                document.getElementById('user-id').value = '';
                document.getElementById('form-title').innerText = '➕ Create User (C)';
                document.getElementById('submit-btn').innerText = 'Save User';
                document.getElementById('cancel-btn').style.display = 'none';
            }}

            async function deleteUser(id) {{
                if (!confirm('Are you sure you want to delete User #' + id + '?')) return;
                const res = await fetch(`/users/${{id}}`, {{ method: 'DELETE' }});
                if (res.ok) {{
                    document.getElementById('user-row-' + id)?.remove();
                }} else {{
                    alert('Delete failed');
                }}
            }}
        </script>
    </body>
    </html>
    """
    return html
