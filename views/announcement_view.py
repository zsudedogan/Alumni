"""
Announcement View - MVC Architecture
Renders the HTML View Layer for Announcement Management Interface (VoltAgent DESIGN.md Standard).
"""

from views.components import get_base_css, render_navbar, render_footer


def render_announcement_management_page(announcements: list) -> str:
    """
    Renders an interactive HTML view for managing announcements (listing, creating, editing, deleting).
    """
    cards_html = ""
    for a in announcements:
        cat = a.category or "General"
        badge_class = "badge-info"
        if cat.lower() == "urgent":
            badge_class = "badge-rejected"
        elif cat.lower() == "academic":
            badge_class = "badge-reviewed"
        elif cat.lower() == "events":
            badge_class = "badge-accepted"

        cards_html += f"""
        <div class="card ann-card-item" id="ann-card-{a.id}" data-category="{cat.lower()}">
            <div class="card-header" style="margin-bottom:0.75rem; padding-bottom:0.5rem;">
                <div style="display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                    <span style="font-family:monospace; color:var(--text-muted); font-size:0.8rem; font-weight:700;">#{a.id}</span>
                    <span class="badge {badge_class}">{cat}</span>
                    <h3 style="color:var(--text-main); font-size:1.15rem; font-weight:800; margin:0;">{a.title}</h3>
                </div>
                <div style="display:flex; gap:0.4rem;">
                    <button class="btn btn-sm btn-secondary" onclick="editAnnouncement({a.id}, `{a.title}`, `{a.content}`, `{a.author or ''}`, `{a.category or ''}`)">✏️ Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteAnnouncement({a.id})">🗑️ Delete</button>
                </div>
            </div>
            <p style="color:var(--text-main); font-size:0.95rem; line-height:1.6; white-space:pre-line; margin-bottom:1rem;">{a.content}</p>
            <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.8rem; color:var(--text-muted); border-top:1px solid var(--border-glass); padding-top:0.6rem;">
                <span>👤 Author: <strong style="color:var(--primary);">{a.author or "Admin"}</strong></span>
                <span>📅 Date: <strong style="color:var(--text-main);">{a.date or "Recent"}</strong></span>
            </div>
        </div>
        """

    if not announcements:
        cards_html = """
        <div class="card" style="text-align: center; padding: 3rem 1.5rem;">
            <p style="color: var(--text-muted); font-size: 1.1rem; margin-bottom: 1rem;">No department notices published yet.</p>
            <p style="font-size: 0.9rem; color: var(--text-muted);">Use the sidebar form to post an announcement!</p>
        </div>
        """

    total_ann = len(announcements)

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Department Notices - Alumni OS</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
        <style>
            {get_base_css()}
            .ann-layout {{
                display: grid;
                grid-template-columns: 360px 1fr;
                gap: 1.75rem;
                align-items: start;
            }}
            @media (max-width: 900px) {{
                .ann-layout {{ grid-template-columns: 1fr; }}
            }}
            .filter-pills {{
                display: flex;
                gap: 0.5rem;
                flex-wrap: wrap;
                margin-bottom: 1.25rem;
            }}
            .filter-pill {{
                padding: 0.35rem 0.85rem;
                border-radius: 9999px;
                background: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.12);
                color: var(--text-muted);
                font-size: 0.82rem;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.2s;
            }}
            .filter-pill:hover, .filter-pill.active {{
                background: var(--primary);
                border-color: var(--primary);
                color: #ffffff;
            }}
        </style>
    </head>
    <body>
        {render_navbar(active_route="announcements")}

        <div class="container">
            <div class="page-header">
                <div>
                    <h1>📢 Department Notices & Announcements</h1>
                    <p>Official academic bulletins, campus events, and administrative circulars for students and alumni.</p>
                </div>
                <div style="display:flex; gap:0.75rem;">
                    <a href="/api/announcements" target="_blank" class="btn btn-secondary btn-sm">🔗 JSON API</a>
                    <a href="/api/swagger" target="_blank" class="btn btn-secondary btn-sm">📖 Swagger Docs</a>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Total Notices</div>
                    <div class="stat-value">{total_ann}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Storage Backend</div>
                    <div class="stat-value" style="color: #38bdf8;">SQLAlchemy ORM</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Filter Support</div>
                    <div class="stat-value" style="color: #34d399;">Categories & Search</div>
                </div>
            </div>

            <div class="ann-layout">
                <!-- FORM: Create / Edit Announcement -->
                <div class="card" style="position: sticky; top: 5rem;">
                    <div class="card-header">
                        <span class="card-title" id="form-title">➕ New Notice</span>
                        <span class="badge badge-info">Publish</span>
                    </div>
                    <form id="ann-form" onsubmit="handleFormSubmit(event)">
                        <input type="hidden" id="ann-id" value="">
                        <div class="form-group" style="margin-bottom: 1rem;">
                            <label class="form-label" for="title">Notice Title *</label>
                            <input class="form-input" type="text" id="title" required placeholder="e.g. Midterm Examination Schedule">
                        </div>
                        <div class="form-group" style="margin-bottom: 1rem;">
                            <label class="form-label" for="category">Category</label>
                            <select class="form-select" id="category">
                                <option value="Academic">Academic</option>
                                <option value="General">General</option>
                                <option value="Events">Events</option>
                                <option value="Urgent">Urgent</option>
                            </select>
                        </div>
                        <div class="form-group" style="margin-bottom: 1rem;">
                            <label class="form-label" for="author">Author / Department</label>
                            <input class="form-input" type="text" id="author" placeholder="e.g. MIS Department Chair">
                        </div>
                        <div class="form-group" style="margin-bottom: 1.5rem;">
                            <label class="form-label" for="content">Notice Content *</label>
                            <textarea class="form-textarea" id="content" rows="4" required placeholder="Write detailed notice text here..."></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary" style="width: 100%;" id="submit-btn">Publish Notice</button>
                        <button type="button" class="btn btn-secondary" style="width: 100%; margin-top: 0.5rem; display: none;" id="cancel-btn" onclick="resetForm()">Cancel Edit</button>
                    </form>
                </div>

                <!-- FEED: Announcements List -->
                <div>
                    <div class="filter-pills">
                        <button class="filter-pill active" onclick="filterCategory('all', this)">All Notices</button>
                        <button class="filter-pill" onclick="filterCategory('academic', this)">Academic</button>
                        <button class="filter-pill" onclick="filterCategory('general', this)">General</button>
                        <button class="filter-pill" onclick="filterCategory('events', this)">Events</button>
                        <button class="filter-pill" onclick="filterCategory('urgent', this)">Urgent</button>
                    </div>

                    <div id="ann-feed">
                        {cards_html}
                    </div>
                </div>
            </div>

            {render_footer()}
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
                    const res = await fetch(`/announcements/${{id}}`, {{
                        method: 'PUT',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }});
                    if (res.ok) window.location.reload();
                    else alert('Update failed');
                }} else {{
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
                document.getElementById('category').value = category || 'General';
                document.getElementById('form-title').innerText = '✏️ Edit Notice #' + id;
                document.getElementById('submit-btn').innerText = 'Update Notice';
                document.getElementById('cancel-btn').style.display = 'block';
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }}

            function resetForm() {{
                document.getElementById('ann-form').reset();
                document.getElementById('ann-id').value = '';
                document.getElementById('form-title').innerText = '➕ New Notice';
                document.getElementById('submit-btn').innerText = 'Publish Notice';
                document.getElementById('cancel-btn').style.display = 'none';
            }}

            async function deleteAnnouncement(id) {{
                if (!confirm('Are you sure you want to delete Notice #' + id + '?')) return;
                const res = await fetch(`/announcements/${{id}}`, {{ method: 'DELETE' }});
                if (res.ok) {{
                    const el = document.getElementById('ann-card-' + id);
                    if (el) el.remove();
                }} else {{
                    alert('Delete failed');
                }}
            }}

            function filterCategory(cat, btn) {{
                document.querySelectorAll('.filter-pill').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const cards = document.querySelectorAll('.ann-card-item');
                cards.forEach(c => {{
                    if (cat === 'all' || c.getAttribute('data-category') === cat) {{
                        c.style.display = '';
                    }} else {{
                        c.style.display = 'none';
                    }}
                }});
            }}
        </script>
    </body>
    </html>
    """
    return html
