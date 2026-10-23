"""
Application View Layer
HTML Template rendering for Applications management interface.
Provides modern, responsive UI with interactive status management, job/applicant dropdowns, and filters.
"""

from typing import List, Optional
from models.application import ApplicationWithDetails
from models.job_posting import JobPosting
from models.user import User


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
            user_options += f'<option value="{u.id}">#{u.id} - {u.name} ({u.email})</option>\n'
    else:
        user_options = '<option value="1">#1 - Emre Yilmaz (emre@example.com)</option><option value="2">#2 - Sude Dogan (sude@example.com)</option>'

    # Generate Application Cards HTML
    app_cards_html = ""
    for a in applications:
        status_raw = a.status or "Pending"
        status_lower = status_raw.lower()
        if status_lower == "accepted":
            badge_class = "badge-success"
        elif status_lower == "shortlisted":
            badge_class = "badge-purple"
        elif status_lower == "reviewed":
            badge_class = "badge-info"
        elif status_lower == "rejected":
            badge_class = "badge-danger"
        else:
            badge_class = "badge-warning"

        applicant_name = a.applicant_name or f"User #{a.user_id}"
        applicant_email = a.applicant_email or "No email on record"
        job_info = f"💼 {a.job_title} @ {a.company}" if a.job_title and a.company else f"Job Posting #{a.job_id}"
        resume_link = (
            f'<a href="{a.resume_url}" target="_blank" rel="noopener noreferrer" class="link-btn">📄 View Portfolio / Resume</a>'
            if a.resume_url
            else '<span class="no-link">No resume attached</span>'
        )

        # Status selection options with current status pre-selected
        status_choices = ["Pending", "Reviewed", "Shortlisted", "Accepted", "Rejected"]
        status_options = "".join(
            f'<option value="{s}"{" selected" if s.lower() == status_lower else ""}>{s}</option>'
            for s in status_choices
        )

        app_cards_html += f"""
        <div class="app-card" data-status="{status_lower}">
            <div class="app-header">
                <div>
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                        <span class="app-id">#{a.id}</span>
                        <h3 class="app-title">{applicant_name}</h3>
                    </div>
                    <p class="app-sub">{job_info} • ✉️ {applicant_email}</p>
                </div>
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <span class="badge {badge_class}" id="badge-{a.id}">{status_raw}</span>
                </div>
            </div>
            {f'<div class="cover-note"><strong>Candidate Statement:</strong> "{a.cover_note}"</div>' if a.cover_note else ''}
            <div class="app-footer">
                <span class="date-tag">📅 Submitted: {a.created_at or 'Recently'}</span>
                {resume_link}
                <div class="card-actions">
                    <label for="status-select-{a.id}" class="action-label">Status:</label>
                    <select id="status-select-{a.id}" class="status-select" onchange="updateApplicationStatus({a.id}, this.value)">
                        {status_options}
                    </select>
                    <button class="btn-delete" onclick="deleteApplication({a.id})">🗑️ Delete</button>
                </div>
                <span class="meta-tag">App ID: #{a.id} • User #{a.user_id}</span>
            </div>
        </div>
        """

    if not app_cards_html:
        app_cards_html = """
        <div class="empty-state">
            <p>No job applications submitted yet. Use the form below to submit an application!</p>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Job Applications</title>
        <style>
            :root {{
                --primary: #4f46e5;
                --primary-hover: #4338ca;
                --bg: #0f172a;
                --card-bg: #1e293b;
                --text: #f8fafc;
                --muted: #94a3b8;
                --border: #334155;
                --success: #10b981;
                --danger: #ef4444;
                --warning: #f59e0b;
                --accent: #38bdf8;
                --purple: #a855f7;
            }}
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: var(--bg);
                color: var(--text);
                padding: 2rem 1rem;
                min-height: 100vh;
                line-height: 1.5;
            }}
            .container {{ max-width: 1000px; margin: 0 auto; }}

            /* Navigation */
            .nav-bar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 2rem;
                border-bottom: 1px solid var(--border);
                padding-bottom: 1rem;
                flex-wrap: wrap;
                gap: 1rem;
            }}
            .nav-bar a {{ color: var(--accent); text-decoration: none; font-size: 0.95rem; font-weight: 500; }}
            .nav-bar a:hover {{ text-decoration: underline; }}
            .nav-links {{ display: flex; gap: 0.75rem; flex-wrap: wrap; }}
            .nav-pill {{
                background: rgba(51, 65, 85, 0.4);
                border: 1px solid var(--border);
                padding: 0.4rem 0.85rem;
                border-radius: 9999px;
                color: var(--muted) !important;
                font-size: 0.85rem !important;
                text-decoration: none !important;
                transition: all 0.2s;
            }}
            .nav-pill:hover {{
                background: rgba(56, 189, 248, 0.15);
                border-color: var(--accent);
                color: var(--accent) !important;
            }}

            /* Header */
            .header {{ text-align: center; margin-bottom: 2rem; }}
            .header h1 {{
                font-size: 2.2rem;
                margin-bottom: 0.5rem;
                background: linear-gradient(to right, #38bdf8, #a855f7);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .header p {{ color: var(--muted); font-size: 1rem; }}

            /* Statistics Bar */
            .stats-bar {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 1rem;
                margin-bottom: 2rem;
            }}
            .stat-box {{
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 1.25rem 1rem;
                text-align: center;
            }}
            .stat-box .number {{ font-size: 1.8rem; font-weight: 700; color: var(--accent); }}
            .stat-box .label {{ font-size: 0.85rem; color: var(--muted); margin-top: 0.25rem; }}

            /* Filter Bar */
            .filter-bar {{
                display: flex;
                gap: 0.5rem;
                flex-wrap: wrap;
                margin-bottom: 1.5rem;
                background: var(--card-bg);
                padding: 0.5rem;
                border-radius: 10px;
                border: 1px solid var(--border);
            }}
            .filter-btn {{
                background: transparent;
                border: none;
                color: var(--muted);
                padding: 0.5rem 1rem;
                border-radius: 6px;
                font-size: 0.85rem;
                cursor: pointer;
                font-weight: 500;
                transition: all 0.2s;
            }}
            .filter-btn:hover {{ color: var(--text); background: rgba(255, 255, 255, 0.05); }}
            .filter-btn.active {{
                background: var(--primary);
                color: #fff;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }}

            /* Application Cards */
            .app-card {{
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1.25rem;
                transition: transform 0.15s, border-color 0.15s;
            }}
            .app-card:hover {{
                transform: translateY(-2px);
                border-color: var(--accent);
            }}
            .app-header {{
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 0.75rem;
                flex-wrap: wrap;
                gap: 0.5rem;
            }}
            .app-id {{
                background: rgba(56, 189, 248, 0.15);
                color: var(--accent);
                font-size: 0.75rem;
                font-weight: 700;
                padding: 0.2rem 0.5rem;
                border-radius: 4px;
            }}
            .app-title {{ font-size: 1.25rem; color: #fff; }}
            .app-sub {{ color: var(--accent); font-size: 0.9rem; margin-top: 0.25rem; }}
            .cover-note {{
                color: #cbd5e1;
                font-size: 0.92rem;
                line-height: 1.5;
                margin-bottom: 0.85rem;
                background: rgba(15, 23, 42, 0.5);
                border-left: 3px solid var(--accent);
                padding: 0.75rem 1rem;
                border-radius: 0 6px 6px 0;
            }}
            .app-footer {{
                display: flex;
                flex-wrap: wrap;
                gap: 1rem;
                align-items: center;
                font-size: 0.85rem;
                color: var(--muted);
                padding-top: 0.85rem;
                border-top: 1px solid rgba(51, 65, 85, 0.6);
            }}
            .link-btn {{
                color: var(--accent);
                text-decoration: none;
                font-weight: 500;
            }}
            .link-btn:hover {{ text-decoration: underline; }}
            .no-link {{ color: #64748b; font-style: italic; }}
            .meta-tag {{ margin-left: auto; color: #64748b; font-size: 0.8rem; }}

            /* Card Actions */
            .card-actions {{
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }}
            .action-label {{
                font-size: 0.8rem;
                color: var(--muted);
            }}
            .status-select {{
                background: #0f172a;
                border: 1px solid var(--border);
                color: #fff;
                padding: 0.3rem 0.6rem;
                border-radius: 6px;
                font-size: 0.8rem;
                cursor: pointer;
            }}
            .status-select:focus {{
                outline: none;
                border-color: var(--accent);
            }}
            .btn-delete {{
                background: rgba(239, 68, 68, 0.15);
                color: #f87171;
                border: 1px solid rgba(239, 68, 68, 0.3);
                padding: 0.3rem 0.65rem;
                border-radius: 6px;
                font-size: 0.8rem;
                cursor: pointer;
                transition: all 0.2s;
            }}
            .btn-delete:hover {{ background: rgba(239, 68, 68, 0.3); }}

            /* Badges */
            .badge {{
                display: inline-block;
                padding: 0.25rem 0.65rem;
                font-size: 0.75rem;
                border-radius: 9999px;
                font-weight: 600;
            }}
            .badge-success {{ background: rgba(16, 185, 129, 0.2); color: #34d399; }}
            .badge-purple {{ background: rgba(168, 85, 247, 0.2); color: #c084fc; }}
            .badge-info {{ background: rgba(56, 189, 248, 0.2); color: #38bdf8; }}
            .badge-danger {{ background: rgba(239, 68, 68, 0.2); color: #f87171; }}
            .badge-warning {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; }}

            /* Form Card */
            .form-card {{
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 14px;
                padding: 2rem;
                margin-top: 3rem;
            }}
            .form-card h2 {{ font-size: 1.4rem; margin-bottom: 0.4rem; color: #fff; }}
            .form-card p.subtitle {{ font-size: 0.85rem; color: var(--muted); margin-bottom: 1.5rem; }}
            .form-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 1.25rem;
                margin-bottom: 1.25rem;
            }}
            .form-group {{ display: flex; flex-direction: column; gap: 0.4rem; }}
            .form-group label {{ font-size: 0.85rem; font-weight: 500; color: #cbd5e1; }}
            .form-group input, .form-group select, .form-group textarea {{
                background: #0f172a;
                border: 1px solid var(--border);
                color: #fff;
                padding: 0.7rem 0.9rem;
                border-radius: 8px;
                font-size: 0.9rem;
            }}
            .form-group input:focus, .form-group select:focus, .form-group textarea:focus {{
                outline: none;
                border-color: var(--accent);
                box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
            }}
            .btn-submit {{
                background: var(--primary);
                color: white;
                border: none;
                padding: 0.85rem 1.75rem;
                border-radius: 8px;
                font-weight: 600;
                font-size: 0.95rem;
                cursor: pointer;
                transition: background 0.2s;
            }}
            .btn-submit:hover {{ background: var(--primary-hover); }}
            .empty-state {{ text-align: center; padding: 3rem 1rem; color: var(--muted); background: var(--card-bg); border-radius: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Navigation -->
            <div class="nav-bar">
                <a href="/">← Return to Application Hub</a>
                <div class="nav-links">
                    <a href="/job-postings/" class="nav-pill">💼 Job Postings Directory</a>
                    <a href="/users/" class="nav-pill">👥 Users Directory</a>
                    <a href="/announcements/" class="nav-pill">📢 Announcements</a>
                    <a href="/api/swagger" target="_blank" class="nav-pill">📖 Swagger UI</a>
                </div>
            </div>

            <!-- Page Header -->
            <div class="header">
                <h1>📝 Student Job Applications</h1>
                <p>MVC Direct & Nested REST Architecture • Track Candidate Pipeline & Review Submissions</p>
            </div>

            <!-- Statistics Bar -->
            <div class="stats-bar">
                <div class="stat-box">
                    <div class="number">{total_apps}</div>
                    <div class="label">Total Applications</div>
                </div>
                <div class="stat-box">
                    <div class="number">{pending_apps}</div>
                    <div class="label">Pending Review</div>
                </div>
                <div class="stat-box">
                    <div class="number">{reviewed_apps}</div>
                    <div class="label">Reviewed</div>
                </div>
                <div class="stat-box">
                    <div class="number">{accepted_apps}</div>
                    <div class="label">Accepted / Shortlisted</div>
                </div>
                <div class="stat-box">
                    <div class="number">{rejected_apps}</div>
                    <div class="label">Rejected</div>
                </div>
            </div>

            <!-- Filter Buttons -->
            <div class="filter-bar">
                <button class="filter-btn active" onclick="filterApps('all', this)">All ({total_apps})</button>
                <button class="filter-btn" onclick="filterApps('pending', this)">Pending ({pending_apps})</button>
                <button class="filter-btn" onclick="filterApps('reviewed', this)">Reviewed ({reviewed_apps})</button>
                <button class="filter-btn" onclick="filterApps('shortlisted', this)">Shortlisted</button>
                <button class="filter-btn" onclick="filterApps('accepted', this)">Accepted</button>
                <button class="filter-btn" onclick="filterApps('rejected', this)">Rejected ({rejected_apps})</button>
            </div>

            <!-- Application Cards Listing -->
            <div class="app-list" id="app-list-container">
                {app_cards_html}
            </div>

            <!-- Application Form -->
            <div class="form-card" id="apply-form">
                <h2>➕ Submit New Job Application (View Layer)</h2>
                <p class="subtitle">Submit candidate credentials, resume URL, and statement for an active job posting.</p>
                <form action="/applications/" method="POST">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="job_id">Select Open Position *</label>
                            <select id="job_id" name="job_id" required>
                                {job_options}
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="user_id">Candidate / Applicant User *</label>
                            <select id="user_id" name="user_id" required>
                                {user_options}
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="status">Initial Status</label>
                            <select id="status" name="status">
                                <option value="Pending">Pending</option>
                                <option value="Reviewed">Reviewed</option>
                                <option value="Shortlisted">Shortlisted</option>
                                <option value="Accepted">Accepted</option>
                                <option value="Rejected">Rejected</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group" style="margin-bottom: 1rem;">
                        <label for="resume_url">Resume / Portfolio / LinkedIn URL</label>
                        <input type="url" id="resume_url" name="resume_url" placeholder="https://linkedin.com/in/... or https://github.com/...">
                    </div>
                    <div class="form-group" style="margin-bottom: 1.5rem;">
                        <label for="cover_note">Cover Note / Candidate Statement</label>
                        <textarea id="cover_note" name="cover_note" rows="3" placeholder="Explain why you are an ideal fit for this role, relevant projects, technical background..."></textarea>
                    </div>
                    <button type="submit" class="btn-submit">🚀 Submit Job Application</button>
                </form>
            </div>
        </div>

        <script>
            function filterApps(filter, btn) {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const cards = document.querySelectorAll('.app-card');
                cards.forEach(card => {{
                    const status = (card.getAttribute('data-status') || '').toLowerCase();
                    if (filter === 'all' || status === filter) {{
                        card.style.display = 'block';
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
                            if (lower === 'accepted') badge.classList.add('badge-success');
                            else if (lower === 'shortlisted') badge.classList.add('badge-purple');
                            else if (lower === 'reviewed') badge.classList.add('badge-info');
                            else if (lower === 'rejected') badge.classList.add('badge-danger');
                            else badge.classList.add('badge-warning');
                        }}
                        const card = document.querySelector(`.app-card[data-status]`);
                        // Update data-status on the parent card
                        const selectEl = document.getElementById(`status-select-${{id}}`);
                        if (selectEl) {{
                            const parentCard = selectEl.closest('.app-card');
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
                        window.location.reload();
                    }} else {{
                        alert('Failed to delete application.');
                    }}
                }} catch (e) {{
                    alert('Error connecting to server.');
                }}
            }}

            // Highlight preselected form if navigated with #apply-form
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
