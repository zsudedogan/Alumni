"""
Application View Layer
HTML Template rendering for Applications management interface.
"""

from typing import List
from models.application import ApplicationWithDetails


def render_application_management_page(applications: List[ApplicationWithDetails]) -> str:
    """Renders the HTML Management Interface for Job Applications"""
    total_apps = len(applications)
    pending_apps = sum(1 for a in applications if (a.status or "").lower() == "pending")
    accepted_apps = sum(1 for a in applications if (a.status or "").lower() in ["accepted", "shortlisted"])

    app_cards_html = ""
    for a in applications:
        status_lower = (a.status or "Pending").lower()
        if status_lower in ["accepted", "shortlisted"]:
            badge_class = "badge-success"
        elif status_lower == "rejected":
            badge_class = "badge-danger"
        else:
            badge_class = "badge-warning"

        applicant_name = a.applicant_name or f"User #{a.user_id}"
        applicant_email = a.applicant_email or "No email provided"
        job_info = f"💼 {a.job_title} @ {a.company}" if a.job_title and a.company else f"Job Posting #{a.job_id}"
        resume_link = f'<a href="{a.resume_url}" target="_blank" class="link-btn">📄 View Resume / Portfolio</a>' if a.resume_url else '<span class="no-link">No resume attached</span>'

        app_cards_html += f"""
        <div class="app-card">
            <div class="app-header">
                <div>
                    <h3 class="app-title">{applicant_name}</h3>
                    <p class="app-sub">{job_info} • ✉️ {applicant_email}</p>
                </div>
                <div>
                    <span class="badge {badge_class}">{a.status}</span>
                </div>
            </div>
            {f'<p class="cover-note">"{a.cover_note}"</p>' if a.cover_note else ''}
            <div class="app-footer">
                <span class="date-tag">📅 Submitted: {a.created_at or 'Recently'}</span>
                {resume_link}
                <span class="meta-tag">Application ID: #{a.id}</span>
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
            .header h1 {{ font-size: 2.2rem; margin-bottom: 0.5rem; background: linear-gradient(to right, #38bdf8, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .header p {{ color: var(--muted); }}
            
            .stats-bar {{ display: flex; gap: 1rem; justify-content: center; margin-bottom: 2rem; }}
            .stat-box {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 10px; padding: 1rem 1.5rem; text-align: center; min-width: 160px; }}
            .stat-box .number {{ font-size: 1.8rem; font-weight: 700; color: var(--accent); }}
            .stat-box .label {{ font-size: 0.85rem; color: var(--muted); }}
            
            .app-card {{
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1.25rem;
                transition: transform 0.15s, border-color 0.15s;
            }}
            .app-card:hover {{ transform: translateY(-2px); border-color: var(--accent); }}
            .app-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem; }}
            .app-title {{ font-size: 1.3rem; color: #fff; margin-bottom: 0.25rem; }}
            .app-sub {{ color: var(--accent); font-size: 0.9rem; }}
            .cover-note {{ color: #cbd5e1; font-size: 0.95rem; line-height: 1.5; margin-bottom: 0.75rem; font-style: italic; background: rgba(15, 23, 42, 0.4); padding: 0.75rem; border-radius: 6px; }}
            .app-footer {{ display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; font-size: 0.85rem; color: var(--muted); padding-top: 0.75rem; border-top: 1px solid rgba(51, 65, 85, 0.5); }}
            .link-btn {{ color: var(--accent); text-decoration: none; font-weight: 500; }}
            .link-btn:hover {{ text-decoration: underline; }}
            .no-link {{ color: var(--muted); }}
            .meta-tag {{ margin-left: auto; color: #64748b; }}
            
            .badge {{ display: inline-block; padding: 0.25rem 0.6rem; font-size: 0.75rem; border-radius: 9999px; font-weight: 600; }}
            .badge-success {{ background: rgba(16, 185, 129, 0.2); color: #34d399; }}
            .badge-danger {{ background: rgba(239, 68, 68, 0.2); color: #f87171; }}
            .badge-warning {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; }}
            
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
                    <a href="/users/" style="margin-right: 1.25rem;">👥 Users</a>
                    <a href="/announcements/" style="margin-right: 1.25rem;">📢 Announcements</a>
                    <a href="/job-postings/" style="margin-right: 1.25rem;">💼 Job Postings</a>
                    <a href="/api/swagger" target="_blank">📖 Swagger UI</a>
                </div>
            </div>

            <div class="header">
                <h1>📝 Student Job Applications</h1>
                <p>MVC Direct & Nested REST Architecture • Track Candidate Applications</p>
            </div>

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
                    <div class="number">{accepted_apps}</div>
                    <div class="label">Accepted / Shortlisted</div>
                </div>
            </div>

            <div class="app-list">
                {app_cards_html}
            </div>

            <div class="form-card">
                <h2>➕ Submit New Job Application (View Layer)</h2>
                <form action="/applications/" method="POST">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="job_id">Job Posting ID *</label>
                            <input type="number" id="job_id" name="job_id" required value="1" placeholder="e.g. 1">
                        </div>
                        <div class="form-group">
                            <label for="user_id">Applicant User ID *</label>
                            <input type="number" id="user_id" name="user_id" required value="2" placeholder="e.g. 2">
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
                        <label for="resume_url">Resume / Portfolio URL</label>
                        <input type="url" id="resume_url" name="resume_url" placeholder="https://linkedin.com/in/... or https://github.com/...">
                    </div>
                    <div class="form-group" style="margin-bottom: 1.5rem;">
                        <label for="cover_note">Cover Note / Candidate Statement</label>
                        <textarea id="cover_note" name="cover_note" rows="3" placeholder="Explain why you are a great fit for this role..."></textarea>
                    </div>
                    <button type="submit" class="btn-submit">Submit Application</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """
