"""
User View - MVC Architecture
Renders the HTML View Layer for User Management Interface (VoltAgent DESIGN.md Standard).
"""

from typing import List
from models.user import User
from views.components import get_base_css, render_navbar, render_footer


def render_user_management_page(users: List[User]) -> str:
    """
    Renders an interactive HTML view for listing users (R) and creating users (C),
    with full client-side actions for edit (PUT/PATCH) and delete (D),
    displaying roles, departments, and profile stats.
    """
    user_rows = ""
    for u in users:
        age_display = f"{u.age} yrs" if u.age is not None else "-"
        email_display = u.email if u.email else "-"
        role_name = getattr(u, "role", "Student") or "Student"
        role_css = {
            "Student": "badge-student",
            "Alumni": "badge-alumni",
            "Recruiter": "badge-recruiter",
            "Academic": "badge-academic"
        }.get(role_name, "badge-info")
        dept_val = getattr(u, "department", "") or ""
        dept_display = f" • {dept_val}" if dept_val else ""

        # Get initials
        parts = u.name.split()
        initials = "".join([p[0].upper() for p in parts[:2]]) if parts else "U"

        user_rows += f"""
        <tr id="user-row-{u.id}">
            <td>
                <div style="display:flex; align-items:center; gap:0.75rem;">
                    <div style="width:36px; height:36px; border-radius:50%; background:#204729; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.85rem; color:white; box-shadow:0 2px 6px rgba(32,71,41,0.2);">
                        {initials}
                    </div>
                    <div>
                        <div style="font-weight:700; color:var(--text-main);">{u.name}</div>
                        <div style="font-size:0.75rem; color:var(--text-muted); font-family:monospace;">ID #{u.id}{dept_display}</div>
                    </div>
                </div>
            </td>
            <td><span class="badge {role_css}">{role_name}</span></td>
            <td><span class="badge badge-info">{age_display}</span></td>
            <td><span style="color:var(--text-muted); font-family:monospace; font-size:0.85rem;">{email_display}</span></td>
            <td style="text-align:right;">
                <div style="display:inline-flex; gap:0.4rem;">
                    <button class="btn btn-sm btn-secondary" onclick="editUser({u.id}, '{u.name}', {u.age or 0}, '{u.email or ''}', '{role_name}', '{dept_val}')">✏️ Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteUser({u.id})">🗑️ Delete</button>
                </div>
            </td>
        </tr>
        """

    total_users = len(users)

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>User Management - Alumni OS</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
        <style>
            {get_base_css()}
            .user-layout {{
                display: grid;
                grid-template-columns: 340px 1fr;
                gap: 1.75rem;
                align-items: start;
            }}
            @media (max-width: 900px) {{
                .user-layout {{ grid-template-columns: 1fr; }}
            }}
            .search-box {{
                margin-bottom: 1rem;
                position: relative;
            }}
            .search-box input {{
                width: 100%;
                background: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.12);
                border-radius: var(--radius-input);
                padding: 0.65rem 1rem 0.65rem 2.25rem;
                color: var(--text-main);
                font-size: 0.9rem;
            }}
            .search-box input:focus {{
                outline: none;
                border-color: var(--primary);
                box-shadow: 0 0 0 3px rgba(32, 71, 41, 0.12);
            }}
            .search-icon {{
                position: absolute;
                left: 0.8rem;
                top: 50%;
                transform: translateY(-50%);
                color: var(--text-muted);
                font-size: 0.85rem;
            }}
        </style>
    </head>
    <body>
        {render_navbar(active_route="users")}

        <div class="container">
            <div class="page-header">
                <div>
                    <h1>👥 User Directory & Management</h1>
                    <p>MVC View Layer: Full CRUD lifecycle for students, alumni, and departmental recruiters.</p>
                </div>
                <div style="display:flex; gap:0.75rem; align-items:center;">
                    <a href="/register/" class="btn btn-primary btn-sm">✨ Register Portal</a>
                    <a href="/api/users" target="_blank" class="btn btn-secondary btn-sm">🔗 JSON API</a>
                    <a href="/api/swagger" target="_blank" class="btn btn-secondary btn-sm">📖 Swagger Docs</a>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Total Registered</div>
                    <div class="stat-value">{total_users} Users</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Roles Supported</div>
                    <div class="stat-value" style="color: var(--accent-gold);">4 Ecosystem</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Database Storage</div>
                    <div class="stat-value" style="color: var(--primary);">SQLAlchemy</div>
                </div>
            </div>

            <div class="user-layout">
                <!-- FORM: Create / Edit User -->
                <div class="card" style="position: sticky; top: 5rem;">
                    <div class="card-header">
                        <span class="card-title" id="form-title">➕ Add New User</span>
                        <span class="badge badge-info">Create</span>
                    </div>
                    <form id="user-form" onsubmit="handleFormSubmit(event)">
                        <input type="hidden" id="user-id" value="">
                        <div class="form-group" style="margin-bottom: 1rem;">
                            <label class="form-label" for="name">Full Name *</label>
                            <input class="form-input" type="text" id="name" required placeholder="e.g. Canan Ozturk">
                        </div>
                        <div class="form-group" style="margin-bottom: 1rem;">
                            <label class="form-label" for="role">Role *</label>
                            <select class="form-input" id="role">
                                <option value="Student">🎓 Student</option>
                                <option value="Alumni">💼 Alumni</option>
                                <option value="Recruiter">🏢 Recruiter</option>
                                <option value="Academic">🏛️ Academic</option>
                            </select>
                        </div>
                        <div class="form-group" style="margin-bottom: 1rem;">
                            <label class="form-label" for="department">Department / Company</label>
                            <input class="form-input" type="text" id="department" placeholder="e.g. Software Engineering">
                        </div>
                        <div class="form-group" style="margin-bottom: 1rem;">
                            <label class="form-label" for="age">Age</label>
                            <input class="form-input" type="number" id="age" placeholder="e.g. 24">
                        </div>
                        <div class="form-group" style="margin-bottom: 1.5rem;">
                            <label class="form-label" for="email">Email Address</label>
                            <input class="form-input" type="email" id="email" placeholder="e.g. canan@example.com">
                        </div>
                        <button type="submit" class="btn btn-primary" style="width: 100%;" id="submit-btn">Save User Record</button>
                        <button type="button" class="btn btn-secondary" style="width: 100%; margin-top: 0.5rem; display: none;" id="cancel-btn" onclick="resetForm()">Cancel Edit</button>
                    </form>
                </div>

                <!-- TABLE: List Users -->
                <div class="card">
                    <div class="card-header">
                        <span class="card-title">📋 Registered Users</span>
                        <span class="badge badge-accepted">{total_users} Active</span>
                    </div>

                    <div class="search-box">
                        <span class="search-icon">🔍</span>
                        <input type="text" id="user-search" placeholder="Filter users by name or email..." oninput="filterUsers()">
                    </div>

                    <div class="table-responsive">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>User Profile</th>
                                    <th>Role</th>
                                    <th>Age</th>
                                    <th>Email</th>
                                    <th style="text-align: right;">Actions</th>
                                </tr>
                            </thead>
                            <tbody id="user-table-body">
                                {user_rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            {render_footer()}
        </div>

        <script>
            async function handleFormSubmit(e) {{
                e.preventDefault();
                const id = document.getElementById('user-id').value;
                const name = document.getElementById('name').value;
                const role = document.getElementById('role').value;
                const department = document.getElementById('department').value || null;
                const age = document.getElementById('age').value ? parseInt(document.getElementById('age').value) : null;
                const email = document.getElementById('email').value || null;

                const payload = {{ name, role, department, age, email }};

                if (id) {{
                    const res = await fetch(`/users/${{id}}`, {{
                        method: 'PUT',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }});
                    if (res.ok) window.location.reload();
                    else alert('Update failed');
                }} else {{
                    const res = await fetch('/users/', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }});
                    if (res.ok) window.location.reload();
                    else alert('Creation failed');
                }}
            }}

            function editUser(id, name, age, email, role, department) {{
                document.getElementById('user-id').value = id;
                document.getElementById('name').value = name;
                document.getElementById('age').value = age || '';
                document.getElementById('email').value = email || '';
                if (role) document.getElementById('role').value = role;
                if (department) document.getElementById('department').value = department;
                document.getElementById('form-title').innerText = '✏️ Edit User #' + id;
                document.getElementById('submit-btn').innerText = 'Update User Record';
                document.getElementById('cancel-btn').style.display = 'block';
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }}

            function resetForm() {{
                document.getElementById('user-form').reset();
                document.getElementById('user-id').value = '';
                document.getElementById('form-title').innerText = '➕ Add New User';
                document.getElementById('submit-btn').innerText = 'Save User Record';
                document.getElementById('cancel-btn').style.display = 'none';
            }}

            async function deleteUser(id) {{
                if (!confirm('Are you sure you want to delete User #' + id + '?')) return;
                const res = await fetch(`/users/${{id}}`, {{ method: 'DELETE' }});
                if (res.ok) {{
                    const row = document.getElementById('user-row-' + id);
                    if (row) row.remove();
                }} else {{
                    alert('Delete failed');
                }}
            }}

            function filterUsers() {{
                const term = document.getElementById('user-search').value.toLowerCase();
                const rows = document.querySelectorAll('#user-table-body tr');
                rows.forEach(r => {{
                    const text = r.innerText.toLowerCase();
                    r.style.display = text.includes(term) ? '' : 'none';
                }});
            }}
        </script>
    </body>
    </html>
    """
    return html
