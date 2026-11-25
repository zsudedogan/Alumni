"""
Application View Layer
HTML Template rendering for Applications management interface (VoltAgent DESIGN.md Standard).
"""

from typing import List, Optional
from models.application import ApplicationWithDetails
from models.job_posting import JobPosting
from models.user import User
from views.components import get_base_css, render_navbar, render_footer


def render_application_management_page(
    applications: List[ApplicationWithDetails],
    available_jobs: Optional[List[JobPosting]] = None,
    available_users: Optional[List[User]] = None,
    preselected_job_id: Optional[int] = None,
) -> str:
    """Renders the HTML Management Interface for Job Applications"""
    total_apps = len(applications)
    pending_apps = sum(1 for a in applications if (a.status or "").lower() == "pending")
    reviewed_apps = sum(1 for a in applications if (a.status or "").lower() == "reviewed")
    accepted_apps = sum(1 for a in applications if (a.status or "").lower() in ["accepted", "shortlisted"])
    rejected_apps = sum(1 for a in applications if (a.status or "").lower() == "rejected")

    # Generate Job Options for Form Select
    job_options = ""
    if available_jobs:
        for j in available_jobs:
            selected = ' selected="selected"' if preselected_job_id and j.id == preselected_job_id else ""
            job_options += f'<option value="{j.id}"{selected}>#{j.id} - {j.title} @ {j.company} ({j.job_type or "Full-time"})</option>\n'
    else:
        job_options = '<option value="1">#1 - Software Engineering Intern @ TechNova</option>'

    # Generate User Options for Form Select
    user_options = ""
    if available_users:
        for u in available_users:
            user_options += f'<option value="{u.id}">#{u.id} - {u.name} ({u.email or "No email"})</option>\n'
    else:
        user_options = '<option value="1">#1 - Emre Yilmaz (emre@example.com)</option><option value="2">#2 - Sude Dogan (sude@example.com)</option>'

    # Generate Application Cards HTML
    app_cards_html = ""
    for a in applications:
        status_raw = a.status or "Pending"
        status_lower = status_raw.lower()
        if status_lower == "accepted":
            badge_class = "badge-accepted"
        elif status_lower == "shortlisted":
            badge_class = "badge-accepted"
        elif status_lower == "reviewed":
            badge_class = "badge-reviewed"
        elif status_lower == "rejected":
            badge_class = "badge-rejected"
        else:
            badge_class = "badge-pending"

        applicant_name = a.applicant_name or f"User #{a.user_id}"
        applicant_email = a.applicant_email or "No email on record"
        job_info = f"💼 {a.job_title} @ {a.company}" if a.job_title and a.company else f"Job Posting #{a.job_id}"
        resume_link = (
            f'<a href="{a.resume_url}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-sm" style="color:#38bdf8;">📄 View Portfolio / Resume</a>'
            if a.resume_url
            else '<span style="color:var(--text-muted); font-size:0.85rem;">No resume attached</span>'
        )

        status_choices = ["Pending", "Reviewed", "Shortlisted", "Accepted", "Rejected"]
        status_options = "".join(
            f'<option value="{s}"{" selected" if s.lower() == status_lower else ""}>{s}</option>'
            for s in status_choices
        )

        initials = "".join([p[0].upper() for p in applicant_name.split()[:2]]) if applicant_name else "A"

        app_cards_html += f"""
        <div class="card app-card-item" data-status="{status_lower}" id="app-card-{a.id}">
            <div class="card-header" style="align-items: flex-start; padding-bottom: 0.85rem;">
                <div style="display: flex; gap: 0.85rem; align-items: center;">
                    <div style="width: 42px; height: 42px; border-radius: 50%; background: #204729; display: flex; align-items: center; justify-content: center; font-weight: 700; color: white; box-shadow: 0 3px 8px rgba(32, 71, 41, 0.2);">
                        {initials}
                    </div>
                    <div>
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.2rem;">
                            <span style="font-family: monospace; color: var(--text-muted); font-size: 0.8rem; font-weight: 700;">#{a.id}</span>
                            <h3 style="font-size: 1.2rem; font-weight: 800; color: var(--text-main); margin: 0;">{applicant_name}</h3>
                        </div>
                        <p style="color: var(--text-muted); font-size: 0.88rem; margin: 0;">
                            {job_info} • <span style="color: var(--primary); font-family: monospace;">{applicant_email}</span>
                        </p>
                    </div>
                </div>
                <div>
                    <span class="badge {badge_class}" id="badge-{a.id}">{status_raw}</span>
                </div>
            </div>

            {f'<div style="background: #fafcfb; border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 8px; padding: 0.75rem 1rem; font-size: 0.9rem; color: var(--text-main); margin-bottom: 1rem;"><strong style="color: var(--primary);">Candidate Statement:</strong> "{a.cover_note}"</div>' if a.cover_note else ''}

            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem; border-top: 1px solid var(--border-glass); padding-top: 0.85rem;">
                <div style="display: flex; gap: 1rem; align-items: center; font-size: 0.825rem; color: var(--text-muted); flex-wrap: wrap;">
                    <span>📅 Submitted: <strong style="color: var(--text-main);">{a.created_at or "Recently"}</strong></span>
                    {resume_link}
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <label for="status-select-{a.id}" style="font-size: 0.8rem; color: var(--text-muted); font-weight: 600;">Status:</label>
                    <select id="status-select-{a.id}" class="form-select" style="padding: 0.3rem 0.6rem; font-size: 0.825rem;" onchange="updateApplicationStatus({a.id}, this.value)">
                        {status_options}
                    </select>
                    <button class="btn btn-danger btn-sm" onclick="deleteApplication({a.id})">🗑️ Delete</button>
                </div>
            </div>
        </div>
        """

    if not app_cards_html:
        app_cards_html = """
        <div class="card" style="text-align: center; padding: 3rem 1.5rem;">
            <p style="color: var(--text-muted); font-size: 1.1rem; margin-bottom: 0.5rem;">No job applications submitted yet.</p>
            <p style="color: var(--text-muted); font-size: 0.9rem;">Submit candidate credentials below to start review workflows!</p>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Job Applications - Alumni OS</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
        <style>
            {get_base_css()}
            .filter-bar {{
                display: flex;
                gap: 0.5rem;
                flex-wrap: wrap;
                margin-bottom: 1.5rem;
            }}
            .filter-btn {{
                padding: 0.4rem 0.9rem;
                border-radius: 9999px;
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid var(--border-glass);
                color: var(--text-muted);
                font-size: 0.825rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
            }}
            .filter-btn:hover, .filter-btn.active {{
                background: rgba(99, 102, 241, 0.25);
                border-color: var(--primary);
                color: #ffffff;
            }}
        </style>
    </head>
    <body>
        {render_navbar(active_route="applications")}

        <div class="container">
            <div class="page-header">
                <div>
                    <h1>📝 Student Job Applications</h1>
                    <p>Track, evaluate, and transition candidate applications across recruitment stages with interactive workflows.</p>
                </div>
                <div style="display:flex; gap:0.75rem;">
                    <a href="#apply-form" class="btn btn-primary btn-sm">➕ Submit Application</a>
                    <a href="/api/applications" target="_blank" class="btn btn-secondary btn-sm">🔗 JSON API</a>
                </div>
            </div>

            <!-- STATS WIDGETS -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Total Submissions</div>
                    <div class="stat-value">{total_apps}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Pending Review</div>
                    <div class="stat-value" style="color: #f59e0b;">{pending_apps}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Reviewed</div>
                    <div class="stat-value" style="color: #38bdf8;">{reviewed_apps}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Accepted / Shortlist</div>
                    <div class="stat-value" style="color: #10b981;">{accepted_apps}</div>
                </div>
            </div>

            <!-- FILTER PILLS -->
            <div class="filter-bar">
                <button class="filter-btn active" onclick="filterApps('all', this)">All Submissions</button>
                <button class="filter-btn" onclick="filterApps('pending', this)">Pending Only</button>
                <button class="filter-btn" onclick="filterApps('reviewed', this)">Reviewed</button>
                <button class="filter-btn" onclick="filterApps('accepted', this)">Accepted</button>
                <button class="filter-btn" onclick="filterApps('rejected', this)">Rejected</button>
            </div>

            <!-- APPLICATION CARDS FEED -->
            <div id="apps-feed" style="margin-bottom: 3rem;">
                {app_cards_html}
            </div>

            <!-- FORM: Submit Application -->
            <div class="card" id="apply-form">
                <div class="card-header">
                    <div>
                        <span class="card-title">📝 Submit New Job Application</span>
                        <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 0.25rem;">
                            Connect a registered candidate to an open career position with optional resume link and cover statement.
                        </p>
                    </div>
                    <span class="badge badge-info">Candidate Form</span>
                </div>

                <form action="/applications/" method="POST">
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label" for="job_id">Target Career Opening *</label>
                            <select class="form-select" id="job_id" name="job_id" required>
                                {job_options}
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="user_id">Candidate / Applicant User *</label>
                            <select class="form-select" id="user_id" name="user_id" required>
                                {user_options}
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="status">Initial Status</label>
                            <select class="form-select" id="status" name="status">
                                <option value="Pending">Pending</option>
                                <option value="Reviewed">Reviewed</option>
                                <option value="Shortlisted">Shortlisted</option>
                                <option value="Accepted">Accepted</option>
                                <option value="Rejected">Rejected</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group" style="margin-bottom: 1.25rem;">
                        <label class="form-label" for="resume_url">Resume / Portfolio URL (Optional)</label>
                        <input class="form-input" type="url" id="resume_url" name="resume_url" placeholder="https://linkedin.com/in/... or https://github.com/...">
                    </div>

                    <div class="form-group" style="margin-bottom: 1.5rem;">
                        <label class="form-label" for="cover_note">Cover Note / Candidate Statement (Optional)</label>
                        <textarea class="form-textarea" id="cover_note" name="cover_note" rows="3" placeholder="Brief statement highlighting relevant courses, projects, or interests..."></textarea>
                    </div>

                    <button type="submit" class="btn btn-primary" style="width: 100%; padding: 0.85rem;">🚀 Submit Candidate Application</button>
                </form>
            </div>

            {render_footer()}
        </div>

        <script>
            function filterApps(filter, btn) {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const cards = document.querySelectorAll('.app-card-item');
                cards.forEach(card => {{
                    const status = (card.getAttribute('data-status') || '').toLowerCase();
                    if (filter === 'all' || status === filter) {{
                        card.style.display = '';
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});
            }}

            async function updateApplicationStatus(id, newStatus) {{
                try {{
                    const res = await fetch(`/api/applications/${{id}}`, {{
                        method: 'PATCH',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ status: newStatus }})
                    }});
                    if (res.ok) {{
                        const badge = document.getElementById(`badge-${{id}}`);
                        if (badge) {{
                            badge.textContent = newStatus;
                            badge.className = 'badge';
                            const lower = newStatus.toLowerCase();
                            if (lower === 'accepted' || lower === 'shortlisted') badge.classList.add('badge-accepted');
                            else if (lower === 'reviewed') badge.classList.add('badge-reviewed');
                            else if (lower === 'rejected') badge.classList.add('badge-rejected');
                            else badge.classList.add('badge-pending');
                        }}
                        const selectEl = document.getElementById(`status-select-${{id}}`);
                        if (selectEl) {{
                            const parentCard = selectEl.closest('.app-card-item');
                            if (parentCard) parentCard.setAttribute('data-status', newStatus.toLowerCase());
                        }}
                    }} else {{
                        alert('Failed to update application status.');
                    }}
                }} catch (e) {{
                    alert('Error connecting to server.');
                }}
            }}

            async function deleteApplication(id) {{
                if (!confirm(`Are you sure you want to delete Application #${{id}}?`)) return;
                try {{
                    const res = await fetch(`/api/applications/${{id}}`, {{ method: 'DELETE' }});
                    if (res.ok) {{
                        const el = document.getElementById('app-card-' + id);
                        if (el) el.remove();
                    }} else {{
                        alert('Failed to delete application.');
                    }}
                }} catch (e) {{
                    alert('Error connecting to server.');
                }}
            }}

            window.addEventListener('DOMContentLoaded', () => {{
                if (window.location.hash === '#apply-form' || window.location.search.includes('job_id=')) {{
                    const formCard = document.getElementById('apply-form');
                    if (formCard) {{
                        formCard.scrollIntoView({{ behavior: 'smooth' }});
                        formCard.style.border = '2px solid var(--accent)';
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """
