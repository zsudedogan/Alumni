"""
JobPosting View Layer
HTML Template rendering for Job Postings management interface.
"""

from typing import List
from models.job_posting import JobPosting


def render_job_posting_management_page(jobs: List[JobPosting]) -> str:
    """Renders the HTML Management Interface for Job Postings"""
    total_jobs = len(jobs)
    active_jobs = sum(1 for j in jobs if j.is_active)

    job_cards_html = ""
    for j in jobs:
        status_badge = '<span class="badge badge-active">Active</span>' if j.is_active else '<span class="badge badge-inactive">Closed</span>'
        deadline_text = f"Deadline: {j.application_deadline}" if j.application_deadline else "Open until filled"
        salary_text = f"💰 {j.salary_range}" if j.salary_range else "Competitive"
        email_link = f'<a href="mailto:{j.contact_email}" class="email-link">📧 {j.contact_email}</a>' if j.contact_email else ""

        job_cards_html += f"""
        <div class="job-card">
            <div class="job-header">
                <div>
                    <h3 class="job-title">{j.title}</h3>
                    <p class="company-name">🏢 {j.company} • 📍 {j.location} • 💼 {j.job_type}</p>
                </div>
                <div>{status_badge}</div>
            </div>
            <p class="job-description">{j.description}</p>
            {f'<div class="job-requirements"><strong>Requirements:</strong> {j.requirements}</div>' if j.requirements else ''}
            <div class="job-footer">
                <span class="salary-tag">{salary_text}</span>
                <span class="deadline-tag">{deadline_text}</span>
                {email_link}
            </div>
        </div>
        """

    if not job_cards_html:
        job_cards_html = """
        <div class="empty-state">
            <p>No job postings currently available. Be the first to create one below!</p>
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
                --accent: #38bdf8;
            }}
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: var(--bg);
                color: var(--text);
                padding: 2rem 1rem;
                min-height: 100vh;
            }}
            .container {{ max-width: 1000px; margin: 0 auto; }}
            .nav-bar {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 1rem; }}
            .nav-bar a {{ color: var(--accent); text-decoration: none; font-size: 0.95rem; font-weight: 500; }}
            .nav-bar a:hover {{ text-decoration: underline; }}
            .header {{ text-align: center; margin-bottom: 2rem; }}
            .header h1 {{ font-size: 2.2rem; margin-bottom: 0.5rem; background: linear-gradient(to right, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .header p {{ color: var(--muted); }}
            
            .stats-bar {{ display: flex; gap: 1rem; justify-content: center; margin-bottom: 2rem; }}
            .stat-box {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 10px; padding: 1rem 1.5rem; text-align: center; min-width: 160px; }}
            .stat-box .number {{ font-size: 1.8rem; font-weight: 700; color: var(--accent); }}
            .stat-box .label {{ font-size: 0.85rem; color: var(--muted); }}
            
            .job-card {{
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1.25rem;
                transition: transform 0.15s, border-color 0.15s;
            }}
            .job-card:hover {{ transform: translateY(-2px); border-color: var(--accent); }}
            .job-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem; }}
            .job-title {{ font-size: 1.3rem; color: #fff; margin-bottom: 0.25rem; }}
            .company-name {{ color: var(--accent); font-size: 0.9rem; }}
            .job-description {{ color: #cbd5e1; font-size: 0.95rem; line-height: 1.5; margin-bottom: 0.75rem; }}
            .job-requirements {{ background: rgba(15, 23, 42, 0.5); padding: 0.75rem; border-radius: 6px; font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.75rem; }}
            .job-footer {{ display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; font-size: 0.85rem; color: var(--muted); padding-top: 0.75rem; border-top: 1px solid rgba(51, 65, 85, 0.5); }}
            .salary-tag {{ color: var(--success); font-weight: 600; }}
            .email-link {{ color: var(--accent); text-decoration: none; }}
            .email-link:hover {{ text-decoration: underline; }}
            
            .badge {{ display: inline-block; padding: 0.25rem 0.6rem; font-size: 0.75rem; border-radius: 9999px; font-weight: 600; }}
            .badge-active {{ background: rgba(16, 185, 129, 0.2); color: #34d399; }}
            .badge-inactive {{ background: rgba(239, 68, 68, 0.2); color: #f87171; }}
            
            .form-card {{
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 1.75rem;
                margin-top: 3rem;
            }}
            .form-card h2 {{ font-size: 1.4rem; margin-bottom: 1.25rem; color: #fff; }}
            .form-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-bottom: 1rem; }}
            .form-group {{ display: flex; flex-direction: column; gap: 0.4rem; }}
            .form-group label {{ font-size: 0.85rem; color: var(--muted); }}
            .form-group input, .form-group select, .form-group textarea {{
                background: #0f172a;
                border: 1px solid var(--border);
                color: #fff;
                padding: 0.65rem 0.85rem;
                border-radius: 6px;
                font-size: 0.9rem;
            }}
            .form-group input:focus, .form-group textarea:focus {{ outline: none; border-color: var(--accent); }}
            .btn-submit {{
                background: var(--primary);
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 6px;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
            }}
            .btn-submit:hover {{ background: var(--primary-hover); }}
            .empty-state {{ text-align: center; padding: 3rem 1rem; color: var(--muted); background: var(--card-bg); border-radius: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav-bar">
                <a href="/">← Return to Main Application Hub</a>
                <div>
                    <a href="/users/" style="margin-right: 1.25rem;">👥 Users View</a>
                    <a href="/announcements/" style="margin-right: 1.25rem;">📢 Announcements View</a>
                    <a href="/api/swagger" target="_blank">📖 Swagger UI</a>
                </div>
            </div>

            <div class="header">
                <h1>💼 Career Portal & Job Postings</h1>
                <p>MVC Direct & Nested REST Architecture • Student & Alumni Opportunities</p>
            </div>

            <div class="stats-bar">
                <div class="stat-box">
                    <div class="number">{total_jobs}</div>
                    <div class="label">Total Positions</div>
                </div>
                <div class="stat-box">
                    <div class="number">{active_jobs}</div>
                    <div class="label">Active Listings</div>
                </div>
            </div>

            <div class="job-list">
                {job_cards_html}
            </div>

            <div class="form-card">
                <h2>➕ Publish New Job Posting (View Layer)</h2>
                <form action="/job-postings/" method="POST">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="title">Position Title *</label>
                            <input type="text" id="title" name="title" required placeholder="e.g. Junior Backend Developer">
                        </div>
                        <div class="form-group">
                            <label for="company">Company Name *</label>
                            <input type="text" id="company" name="company" required placeholder="e.g. TechCorp">
                        </div>
                        <div class="form-group">
                            <label for="location">Location</label>
                            <input type="text" id="location" name="location" value="Remote" placeholder="e.g. Istanbul / Remote">
                        </div>
                        <div class="form-group">
                            <label for="job_type">Job Type</label>
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
                            <label for="salary_range">Salary Range</label>
                            <input type="text" id="salary_range" name="salary_range" placeholder="e.g. $2,000 - $3,000">
                        </div>
                        <div class="form-group">
                            <label for="contact_email">Contact / Application Email</label>
                            <input type="email" id="contact_email" name="contact_email" placeholder="hr@company.com">
                        </div>
                        <div class="form-group">
                            <label for="application_deadline">Application Deadline</label>
                            <input type="date" id="application_deadline" name="application_deadline">
                        </div>
                    </div>
                    <div class="form-group" style="margin-bottom: 1rem;">
                        <label for="description">Job Description *</label>
                        <textarea id="description" name="description" rows="3" required placeholder="Describe responsibilities and project scope..."></textarea>
                    </div>
                    <div class="form-group" style="margin-bottom: 1.5rem;">
                        <label for="requirements">Requirements & Qualifications</label>
                        <textarea id="requirements" name="requirements" rows="2" placeholder="List required technologies, degrees, skills..."></textarea>
                    </div>
                    <button type="submit" class="btn-submit">Publish Job Opportunity</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """
