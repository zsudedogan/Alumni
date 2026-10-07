"""
Announcement View - MVC Architecture
Renders the HTML View Layer for Announcement Management Interface (Homework Requirement).
"""

from typing import List


def render_announcement_management_page(announcements: list) -> str:
    """
    Renders an interactive HTML view for managing announcements (listing, creating, editing, deleting).
    Homework requirement: 'Create interface to manage without database yet'.
    """
    cards_html = ""
    for a in announcements:
        category_badge = f'<span class="badge badge-cat">{a.category or "General"}</span>'
        cards_html += f"""
        <div class="announcement-card" id="ann-card-{a.id}">
            <div class="card-header">
                <div>
                    <span class="ann-id">#{a.id}</span>
                    {category_badge}
                    <h3 class="ann-title">{a.title}</h3>
                </div>
                <div class="card-actions">
                    <button class="btn btn-sm btn-edit" onclick="editAnnouncement({a.id}, '{a.title}', `{a.content}`, '{a.author or ''}', '{a.category or ''}')">Edit</button>
                    <button class="btn btn-sm btn-delete" onclick="deleteAnnouncement({a.id})">Delete</button>
                </div>
            </div>
            <p class="ann-content">{a.content}</p>
            <div class="card-footer">
                <span>👤 Posted by: <strong>{a.author or "Admin"}</strong></span>
                <span>📅 Date: {a.date or "Recent"}</span>
            </div>
        </div>
        """

    if not announcements:
        cards_html = "<p style='color: #64748b; text-align: center; padding: 2rem;'>No announcements yet. Use the form to post one!</p>"

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Announcement Management - View Layer</title>
        <style>
            :root {{
                --primary: #4f46e5;
                --primary-dark: #3730a3;
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
            .container {{ max-width: 1040px; margin: 0 auto; }}
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
                background: #eef2ff;
            }}
            .nav-links a:hover {{ background: #e0e7ff; }}
            .grid {{ display: grid; grid-template-columns: 360px 1fr; gap: 2rem; }}
            @media (max-width: 860px) {{ .grid {{ grid-template-columns: 1fr; }} }}
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
            input, textarea, select {{
                width: 100%;
                padding: 0.6rem 0.8rem;
                border: 1px solid var(--border);
                border-radius: 6px;
                font-size: 0.95rem;
                font-family: inherit;
            }}
            input:focus, textarea:focus, select:focus {{
                outline: none;
                border-color: var(--primary);
                box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
            }}
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
            .btn-delete {{ background: #fee2e2; color: #b91c1c; }}
            .badge {{
                display: inline-block;
                padding: 0.2rem 0.5rem;
                font-size: 0.75rem;
                font-weight: 600;
                border-radius: 4px;
            }}
            .badge-cat {{ background: #e0e7ff; color: #4338ca; }}
            .ann-id {{ font-size: 0.8rem; font-weight: 700; color: #64748b; margin-right: 0.4rem; }}
            .announcement-card {{
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 10px;
                padding: 1.25rem;
                margin-bottom: 1rem;
                transition: box-shadow 0.2s;
            }}
            .announcement-card:hover {{ box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.06); }}
            .card-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; }}
            .ann-title {{ font-size: 1.15rem; color: #1e293b; margin-top: 0.25rem; }}
            .ann-content {{ color: #475569; margin: 0.75rem 0; white-space: pre-line; }}
            .card-footer {{
                display: flex;
                justify-content: space-between;
                font-size: 0.825rem;
                color: var(--text-muted);
                border-top: 1px solid #f1f5f9;
                padding-top: 0.5rem;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div>
                    <h1>📢 Announcement Management Interface</h1>
                    <p style="color: var(--text-muted); font-size: 0.9rem;">
                        Homework Task: In-Memory CRUD management for Announcements via <code>.../announcements/</code>
                    </p>
                </div>
                <div class="nav-links">
                    <a href="/users/">👥 Users Interface</a>
                    <a href="/api/swagger" target="_blank">📖 Swagger Docs</a>
                    <a href="/api/announcements" target="_blank">🔗 JSON API</a>
                </div>
            </div>

            <div class="grid">
                <!-- FORM: Create / Edit Announcement -->
                <div class="card">
                    <h2 id="form-title">➕ New Announcement</h2>
                    <form id="ann-form" onsubmit="handleFormSubmit(event)">
                        <input type="hidden" id="ann-id" value="">
                        <div class="form-group">
                            <label for="title">Title *</label>
                            <input type="text" id="title" required placeholder="e.g. Midterm Exam Schedule">
                        </div>
                        <div class="form-group">
                            <label for="content">Content *</label>
                            <textarea id="content" rows="4" required placeholder="Announcement details..."></textarea>
                        </div>
                        <div class="form-group">
                            <label for="author">Author</label>
                            <input type="text" id="author" placeholder="e.g. Prof. Smith / Department">
                        </div>
                        <div class="form-group">
                            <label for="category">Category</label>
                            <select id="category">
                                <option value="Academic">Academic</option>
                                <option value="General">General</option>
                                <option value="Events">Events</option>
                                <option value="Urgent">Urgent</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary" id="submit-btn">Publish Announcement</button>
                        <button type="button" class="btn" style="background:#e2e8f0; width:100%; margin-top:0.5rem; display:none;" id="cancel-btn" onclick="resetForm()">Cancel</button>
                    </form>
                </div>

                <!-- LIST: All Announcements -->
                <div>
                    <h2>📜 Live Announcements ({len(announcements)})</h2>
                    <div id="announcements-list">
                        {cards_html}
                    </div>
                </div>
            </div>
        </div>

        <script>
            async function handleFormSubmit(e) {{
                e.preventDefault();
                const id = document.getElementById('ann-id').value;
                const title = document.getElementById('title').value;
                const content = document.getElementById('content').value;
                const author = document.getElementById('author').value || 'Admin';
                const category = document.getElementById('category').value;

                const payload = {{ title, content, author, category }};

                if (id) {{
                    // Update (PUT)
                    const res = await fetch(`/announcements/${{id}}`, {{
                        method: 'PUT',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }});
                    if (res.ok) window.location.reload();
                    else alert('Update failed');
                }} else {{
                    // Create (POST)
                    const res = await fetch('/announcements/', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }});
                    if (res.ok) window.location.reload();
                    else alert('Creation failed');
                }}
            }}

            function editAnnouncement(id, title, content, author, category) {{
                document.getElementById('ann-id').value = id;
                document.getElementById('title').value = title;
                document.getElementById('content').value = content;
                document.getElementById('author').value = author || '';
                if (category) document.getElementById('category').value = category;
                document.getElementById('form-title').innerText = '✏️ Edit Announcement #' + id;
                document.getElementById('submit-btn').innerText = 'Update Announcement';
                document.getElementById('cancel-btn').style.display = 'block';
            }}

            function resetForm() {{
                document.getElementById('ann-form').reset();
                document.getElementById('ann-id').value = '';
                document.getElementById('form-title').innerText = '➕ New Announcement';
                document.getElementById('submit-btn').innerText = 'Publish Announcement';
                document.getElementById('cancel-btn').style.display = 'none';
            }}

            async function deleteAnnouncement(id) {{
                if (!confirm('Are you sure you want to delete Announcement #' + id + '?')) return;
                const res = await fetch(`/announcements/${{id}}`, {{ method: 'DELETE' }});
                if (res.ok) {{
                    document.getElementById('ann-card-' + id)?.remove();
                }} else {{
                    alert('Delete failed');
                }}
            }}
        </script>
    </body>
    </html>
    """
    return html
