"""
JobPosting View Layer
HTML Template rendering for Career Portal and Job Postings (VoltAgent DESIGN.md Standard).
"""

from typing import List, Optional
from models.job_posting import JobPosting
from models.user import User
from views.components import get_base_css, render_navbar, render_footer


def render_job_posting_management_page(
    jobs: List[JobPosting],
    available_users: Optional[List[User]] = None
) -> str:
    """Renders the modernized HTML Management Interface for Job Postings"""
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
        status_badge = '<span class="badge badge-accepted">Active</span>' if j.is_active else '<span class="badge badge-rejected">Closed</span>'
        deadline_text = f"📅 Deadline: {j.application_deadline}" if j.application_deadline else "📅 Open until filled"
        salary_text = f"💰 {j.salary_range}" if j.salary_range else "💰 Competitive Compensation"
        email_link = f'<span style="color:#38bdf8;">✉️ {j.contact_email}</span>' if j.contact_email else ""
        type_badge = f'<span class="badge badge-info">{j.job_type or "Full-time"}</span>'
        city_display = j.city or j.location or "Remote"

        # Company initial
        company_initial = j.company[0].upper() if j.company else "C"

        job_cards_html += f"""
        <div class="card job-card-item" data-job-type="{j.job_type or ''}" data-location="{city_display}">
            <div class="card-header" style="align-items: flex-start; padding-bottom: 0.85rem;">
                <div style="display: flex; gap: 1rem; align-items: flex-start;">
                    <div style="width: 44px; height: 44px; border-radius: 12px; background: #204729; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; font-weight: 800; color: white; box-shadow: 0 4px 10px rgba(32, 71, 41, 0.2);">
                        {company_initial}
                    </div>
                    <div>
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem; flex-wrap: wrap;">
                            <span style="font-family: monospace; font-size: 0.8rem; color: var(--text-muted); font-weight: 700;">#{j.id}</span>
                            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--text-main); margin: 0;">{j.title}</h3>
                        </div>
                        <p style="color: var(--text-muted); font-size: 0.9rem; margin: 0;">
                            🏢 <strong style="color: var(--primary);">{j.company}</strong> • 📍 {city_display}
                        </p>
                    </div>
                </div>
                <div style="display: flex; gap: 0.4rem; align-items: center;">
                    {type_badge}
                    {status_badge}
                </div>
            </div>

            {f'<p style="color: var(--text-main); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1rem;">{j.description}</p>' if j.description else ''}

            {f'<div style="background: #fafcfb; border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 8px; padding: 0.65rem 0.9rem; font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;"><strong style="color: var(--text-main);">Requirements:</strong> {j.requirements}</div>' if j.requirements else ''}

            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem; border-top: 1px solid var(--border-glass); padding-top: 0.85rem;">
                <div style="display: flex; gap: 1rem; align-items: center; font-size: 0.85rem; color: var(--text-muted); flex-wrap: wrap;">
                    <span>{salary_text}</span>
                    <span>{deadline_text}</span>
                    {email_link}
                </div>
                <div style="display: flex; gap: 0.5rem;">
                    <a href="/applications/?job_id={j.id}#apply-form" class="btn btn-primary btn-sm">📝 Apply Now</a>
                    <button class="btn btn-danger btn-sm" onclick="deleteJob({j.id})">🗑️ Delete</button>
                </div>
            </div>
        </div>
        """

    if not job_cards_html:
        job_cards_html = """
        <div class="card" style="text-align: center; padding: 3rem 1.5rem;">
            <p style="color: var(--text-muted); font-size: 1.1rem; margin-bottom: 0.5rem;">No job postings published yet.</p>
            <p style="color: var(--text-muted); font-size: 0.9rem;">Publish the first career opportunity using the form below!</p>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Career Portal & Job Postings - Alumni OS</title>
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
        {render_navbar(active_route="jobs")}

        <div class="container">
            <div class="page-header">
                <div>
                    <h1>💼 Career Portal & Job Postings</h1>
                    <p>Discover internships and full-time employment opportunities published by alumni and partner companies.</p>
                </div>
                <div style="display:flex; gap:0.75rem;">
                    <a href="#publish-form" class="btn btn-primary btn-sm">➕ Post an Opening</a>
                    <a href="/api/job-postings" target="_blank" class="btn btn-secondary btn-sm">🔗 JSON API</a>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Total Positions</div>
                    <div class="stat-value">{total_jobs}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Active Listings</div>
                    <div class="stat-value" style="color: #34d399;">{active_jobs}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Internship Roles</div>
                    <div class="stat-value" style="color: #38bdf8;">{internships}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Full-Time Roles</div>
                    <div class="stat-value" style="color: #a5b4fc;">{full_times}</div>
                </div>
            </div>

            <!-- FILTER PILLS -->
            <div class="filter-bar">
                <button class="filter-btn active" onclick="filterJobs('all', this)">All Positions</button>
                <button class="filter-btn" onclick="filterJobs('internship', this)">Internships Only</button>
                <button class="filter-btn" onclick="filterJobs('full-time', this)">Full-time Roles</button>
                <button class="filter-btn" onclick="filterJobs('remote', this)">Remote Positions</button>
            </div>

            <!-- JOB CARDS LIST -->
            <div id="job-feed" style="margin-bottom: 3rem;">
                {job_cards_html}
            </div>

            <!-- FORM: Publish Opportunity -->
            <div class="card" id="publish-form">
                <div class="card-header">
                    <div>
                        <span class="card-title">🚀 Publish New Career Opportunity</span>
                        <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 0.25rem;">
                            Rule enforcement: Title (max 120 chars, required), Company (required), City & Description (optional).
                        </p>
                    </div>
                    <span class="badge badge-info">Recruiter Portal</span>
                </div>

                <form action="/job-postings/" method="POST">
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label" for="title">Position Title * (Max 120 chars)</label>
                            <input class="form-input" type="text" id="title" name="title" required maxlength="120" placeholder="e.g. Junior Backend Engineer">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="company">Hiring Company *</label>
                            <input class="form-input" type="text" id="company" name="company" required placeholder="e.g. TechCorp Istanbul">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="city">City / Location (Optional)</label>
                            <input class="form-input" type="text" id="city" name="city" placeholder="e.g. Istanbul / Remote">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="job_type">Employment Type</label>
                            <select class="form-select" id="job_type" name="job_type">
                                <option value="Full-time">Full-time</option>
                                <option value="Part-time">Part-time</option>
                                <option value="Internship">Internship</option>
                                <option value="Contract">Contract</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label" for="user_id">Posted by (Recruiter / User)</label>
                            <select class="form-select" id="user_id" name="user_id">
                                {user_options}
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="salary_range">Compensation Range (Optional)</label>
                            <input class="form-input" type="text" id="salary_range" name="salary_range" placeholder="e.g. ₺35,000 - ₺45,000 / month">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="contact_email">Application Email (Optional)</label>
                            <input class="form-input" type="email" id="contact_email" name="contact_email" placeholder="careers@company.com">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="application_deadline">Deadline Date</label>
                            <input class="form-input" type="date" id="application_deadline" name="application_deadline">
                        </div>
                    </div>

                    <div class="form-group" style="margin-bottom: 1rem;">
                        <label class="form-label" for="description">Job Description (Optional)</label>
                        <textarea class="form-textarea" id="description" name="description" rows="3" placeholder="Overview of team, role responsibilities, tech stack..."></textarea>
                    </div>

                    <div class="form-group" style="margin-bottom: 1.5rem;">
                        <label class="form-label" for="requirements">Requirements & Qualifications (Optional)</label>
                        <textarea class="form-textarea" id="requirements" name="requirements" rows="2" placeholder="Required technical skills, university year, languages..."></textarea>
                    </div>

                    <button type="submit" class="btn btn-primary" style="width: 100%; padding: 0.85rem;">🚀 Publish Opportunity to Portal</button>
                </form>
            </div>

            {render_footer()}
        </div>

        <script>
            function filterJobs(filter, btn) {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const cards = document.querySelectorAll('.job-card-item');
                cards.forEach(card => {{
                    const type = (card.getAttribute('data-job-type') || '').toLowerCase();
                    const location = (card.getAttribute('data-location') || '').toLowerCase();
                    if (filter === 'all') {{
                        card.style.display = '';
                    }} else if (filter === 'remote') {{
                        card.style.display = location.includes('remote') ? '' : 'none';
                    }} else {{
                        card.style.display = type.includes(filter) ? '' : 'none';
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
