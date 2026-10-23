"""
JobPosting View Layer
HTML Template rendering for Job Postings management interface and career portal.
"""

from typing import List, Optional
from models.job_posting import JobPosting
from models.user import User


def render_job_posting_management_page(
    jobs: List[JobPosting],
    available_users: Optional[List[User]] = None
) -> str:
    """Renders the HTML Management Interface for Job Postings"""
    total_jobs = len(jobs)
    active_jobs = sum(1 for j in jobs if j.is_active)
    internships = sum(1 for j in jobs if (j.job_type or "").lower() == "internship")
    full_times = sum(1 for j in jobs if (j.job_type or "").lower() == "full-time")

    user_options = ""
    if available_users:
        for u in available_users:
            user_options += f'<option value="{u.id}">{u.name} (ID: {u.id})</option>'
    else:
        user_options = '<option value="1">Emre Yilmaz (ID: 1)</option><option value="2">Sude Dogan (ID: 2)</option>'

    job_cards_html = ""
    for j in jobs:
        status_badge = '<span class="badge badge-active">Active</span>' if j.is_active else '<span class="badge badge-inactive">Closed</span>'
        deadline_text = f"📅 Deadline: {j.application_deadline}" if j.application_deadline else "📅 Open until filled"
        salary_text = f"💰 {j.salary_range}" if j.salary_range else "💰 Competitive"
        email_link = f'<a href="mailto:{j.contact_email}" class="meta-link">✉️ {j.contact_email}</a>' if j.contact_email else ""
        type_badge = f'<span class="badge badge-type">{j.job_type or "Full-time"}</span>'

        job_cards_html += f"""
        <div class="job-card" data-job-type="{j.job_type or ''}" data-location="{j.location or ''}">
            <div class="job-header">
                <div>
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                        <span class="job-id">#{j.id}</span>
                        <h3 class="job-title">{j.title}</h3>
                    </div>
                    <p class="company-name">🏢 <strong>{j.company}</strong> • 📍 {j.location or 'Remote'}</p>
                </div>
                <div style="display: flex; gap: 0.5rem; align-items: center;">
                    {type_badge}
                    {status_badge}
                </div>
            </div>
            <p class="job-description">{j.description}</p>
            {f'<div class="job-requirements"><strong>Requirements:</strong> {j.requirements}</div>' if j.requirements else ''}
            <div class="job-footer">
                <span class="salary-tag">{salary_text}</span>
                <span class="deadline-tag">{deadline_text}</span>
                {email_link}
                <div class="card-actions">
                    <a href="/applications/?job_id={j.id}#apply-form" class="btn-apply">📝 Apply to this Job</a>
                    <button class="btn-delete" onclick="deleteJob({j.id})">🗑️ Delete</button>
                </div>
            </div>
        </div>
        """

    if not job_cards_html:
        job_cards_html = """
        <div class="empty-state">
            <p>No job postings currently available. Be the first to publish one below!</p>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Career Portal & Job Postings</title>
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
            .container {{ max-width: 1060px; margin: 0 auto; }}
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
            .nav-links {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
            .nav-pill {{
                background: rgba(56, 189, 248, 0.1);
                color: var(--accent) !important;
                padding: 0.35rem 0.75rem;
                border-radius: 6px;
                border: 1px solid rgba(56, 189, 248, 0.2);
            }}
            .nav-pill:hover {{ background: rgba(56, 189, 248, 0.2); text-decoration: none !important; }}

            .header {{ text-align: center; margin-bottom: 2rem; }}
            .header h1 {{
                font-size: 2.2rem;
                margin-bottom: 0.5rem;
                background: linear-gradient(to right, #38bdf8, #818cf8);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .header p {{ color: var(--muted); }}

            .stats-bar {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
            .stat-box {{
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 10px;
                padding: 1.2rem;
                text-align: center;
            }}
            .stat-box .number {{ font-size: 1.8rem; font-weight: 700; color: var(--accent); }}
            .stat-box .label {{ font-size: 0.85rem; color: var(--muted); }}

            .filter-bar {{
                display: flex;
                gap: 0.5rem;
                margin-bottom: 1.5rem;
                flex-wrap: wrap;
            }}
            .filter-btn {{
                background: var(--card-bg);
                border: 1px solid var(--border);
                color: var(--muted);
                padding: 0.4rem 0.9rem;
                border-radius: 9999px;
                font-size: 0.85rem;
                cursor: pointer;
                transition: all 0.2s;
            }}
            .filter-btn:hover, .filter-btn.active {{
                background: var(--primary);
                color: #fff;
                border-color: var(--primary);
            }}

            .job-card {{
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1.25rem;
                transition: transform 0.15s, border-color 0.15s, box-shadow 0.15s;
            }}
            .job-card:hover {{
                transform: translateY(-2px);
                border-color: var(--accent);
                box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.3);
            }}
            .job-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem; }}
            .job-id {{ font-size: 0.85rem; font-weight: 700; color: var(--muted); }}
            .job-title {{ font-size: 1.25rem; color: #fff; }}
            .company-name {{ color: var(--accent); font-size: 0.9rem; margin-top: 0.2rem; }}
            .job-description {{ color: #cbd5e1; font-size: 0.95rem; line-height: 1.6; margin-bottom: 0.85rem; }}
            .job-requirements {{
                background: rgba(15, 23, 42, 0.6);
                border-left: 3px solid var(--primary);
                padding: 0.75rem 1rem;
                border-radius: 4px;
                font-size: 0.85rem;
                color: #94a3b8;
                margin-bottom: 0.85rem;
            }}
            .job-footer {{
                display: flex;
                flex-wrap: wrap;
                gap: 1rem;
                align-items: center;
                font-size: 0.85rem;
                color: var(--muted);
                padding-top: 0.85rem;
                border-top: 1px solid rgba(51, 65, 85, 0.6);
            }}
            .salary-tag {{ color: var(--success); font-weight: 600; }}
            .deadline-tag {{ color: var(--warning); }}
            .meta-link {{ color: var(--accent); text-decoration: none; }}
            .meta-link:hover {{ text-decoration: underline; }}
            .card-actions {{ margin-left: auto; display: flex; gap: 0.5rem; align-items: center; }}

            .btn-apply {{
                background: var(--primary);
                color: #fff !important;
                padding: 0.4rem 0.85rem;
                border-radius: 6px;
                font-size: 0.85rem;
                font-weight: 600;
                text-decoration: none !important;
                transition: background 0.2s;
            }}
            .btn-apply:hover {{ background: var(--primary-hover); }}
            .btn-delete {{
                background: rgba(239, 68, 68, 0.15);
                color: #f87171;
                border: 1px solid rgba(239, 68, 68, 0.3);
                padding: 0.35rem 0.75rem;
                border-radius: 6px;
                font-size: 0.8rem;
                cursor: pointer;
                transition: all 0.2s;
            }}
            .btn-delete:hover {{ background: rgba(239, 68, 68, 0.3); }}

            .badge {{ display: inline-block; padding: 0.25rem 0.6rem; font-size: 0.75rem; border-radius: 9999px; font-weight: 600; }}
            .badge-active {{ background: rgba(16, 185, 129, 0.2); color: #34d399; }}
            .badge-inactive {{ background: rgba(239, 68, 68, 0.2); color: #f87171; }}
            .badge-type {{ background: rgba(56, 189, 248, 0.15); color: var(--accent); }}

            .form-card {{
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 14px;
                padding: 2rem;
                margin-top: 3rem;
            }}
            .form-card h2 {{ font-size: 1.4rem; margin-bottom: 0.5rem; color: #fff; }}
            .form-card p.subtitle {{ font-size: 0.85rem; color: var(--muted); margin-bottom: 1.5rem; }}
            .form-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.25rem; margin-bottom: 1.25rem; }}
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
                    <a href="/applications/" class="nav-pill">📝 View Applications ({total_jobs} active)</a>
                    <a href="/users/" class="nav-pill">👥 Users Directory</a>
                    <a href="/announcements/" class="nav-pill">📢 Announcements</a>
                    <a href="/api/swagger" target="_blank" class="nav-pill">📖 Swagger UI</a>
                </div>
            </div>

            <!-- Page Header -->
            <div class="header">
                <h1>💼 Career Portal & Job Postings</h1>
                <p>Explore opportunities, submit applications, or publish new openings.</p>
            </div>

            <!-- Statistics Bar -->
            <div class="stats-bar">
                <div class="stat-box">
                    <div class="number">{total_jobs}</div>
                    <div class="label">Total Positions</div>
                </div>
                <div class="stat-box">
                    <div class="number">{active_jobs}</div>
                    <div class="label">Active Listings</div>
                </div>
                <div class="stat-box">
                    <div class="number">{internships}</div>
                    <div class="label">Internships</div>
                </div>
                <div class="stat-box">
                    <div class="number">{full_times}</div>
                    <div class="label">Full-time Roles</div>
                </div>
            </div>

            <!-- Filter Buttons -->
            <div class="filter-bar">
                <button class="filter-btn active" onclick="filterJobs('all', this)">All Positions</button>
                <button class="filter-btn" onclick="filterJobs('internship', this)">Internships</button>
                <button class="filter-btn" onclick="filterJobs('full-time', this)">Full-time</button>
                <button class="filter-btn" onclick="filterJobs('remote', this)">Remote Roles</button>
            </div>

            <!-- Job Cards Listing -->
            <div class="job-list" id="job-list-container">
                {job_cards_html}
            </div>

            <!-- Publish Form -->
            <div class="form-card" id="publish-form">
                <h2>➕ Publish a New Job Posting</h2>
                <p class="subtitle">Fill out the details below to add a position to the career portal.</p>
                <form action="/job-postings/" method="POST">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="title">Position Title *</label>
                            <input type="text" id="title" name="title" required placeholder="e.g. Junior Python / FastAPI Developer">
                        </div>
                        <div class="form-group">
                            <label for="company">Hiring Company *</label>
                            <input type="text" id="company" name="company" required placeholder="e.g. TechNova Solutions">
                        </div>
                        <div class="form-group">
                            <label for="location">Location</label>
                            <input type="text" id="location" name="location" value="Remote" placeholder="e.g. Istanbul / Remote">
                        </div>
                        <div class="form-group">
                            <label for="job_type">Employment Type</label>
                            <select id="job_type" name="job_type">
                                <option value="Full-time">Full-time</option>
                                <option value="Part-time">Part-time</option>
                                <option value="Internship">Internship</option>
                                <option value="Contract">Contract</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="user_id">Posted by (User / Recruiter)</label>
                            <select id="user_id" name="user_id">
                                {user_options}
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="salary_range">Compensation / Salary Range</label>
                            <input type="text" id="salary_range" name="salary_range" placeholder="e.g. ₺35,000 - ₺45,000 / month">
                        </div>
                        <div class="form-group">
                            <label for="contact_email">Application Email</label>
                            <input type="email" id="contact_email" name="contact_email" placeholder="jobs@company.com">
                        </div>
                        <div class="form-group">
                            <label for="application_deadline">Deadline Date</label>
                            <input type="date" id="application_deadline" name="application_deadline">
                        </div>
                    </div>
                    <div class="form-group" style="margin-bottom: 1rem;">
                        <label for="description">Job Description *</label>
                        <textarea id="description" name="description" rows="3" required placeholder="Explain role responsibilities, tech stack, team expectations..."></textarea>
                    </div>
                    <div class="form-group" style="margin-bottom: 1.5rem;">
                        <label for="requirements">Requirements & Qualifications</label>
                        <textarea id="requirements" name="requirements" rows="2" placeholder="List required skills (e.g. Python, SQL, REST APIs, Git)..."></textarea>
                    </div>
                    <button type="submit" class="btn-submit">🚀 Publish Job Opportunity</button>
                </form>
            </div>
        </div>

        <script>
            function filterJobs(filter, btn) {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const cards = document.querySelectorAll('.job-card');
                cards.forEach(card => {{
                    const type = (card.getAttribute('data-job-type') || '').toLowerCase();
                    const location = (card.getAttribute('data-location') || '').toLowerCase();
                    if (filter === 'all') {{
                        card.style.display = 'block';
                    }} else if (filter === 'remote') {{
                        card.style.display = location.includes('remote') ? 'block' : 'none';
                    }} else {{
                        card.style.display = type.includes(filter) ? 'block' : 'none';
                    }}
                }});
            }}

            async function deleteJob(id) {{
                if (!confirm(`Are you sure you want to delete Job Posting #${{id}}? This will also remove any related applications.`)) return;
                try {{
                    const res = await fetch(`/api/job-postings/${{id}}`, {{ method: 'DELETE' }});
                    if (res.ok) {{
                        window.location.reload();
                    }} else {{
                        alert('Failed to delete job posting');
                    }}
                }} catch (e) {{
                    alert('Error connecting to server');
                }}
            }}
        </script>
    </body>
    </html>
    """
