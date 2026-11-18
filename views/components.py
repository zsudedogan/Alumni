"""
Shared View Components & Styles
Implements DESIGN.md and brand.md specifications (VoltAgent standard).
"""

def get_base_css() -> str:
    """Returns global design system CSS tokens and component styles"""
    return """
        :root {
            --bg-base: #090d16;
            --bg-surface: rgba(15, 23, 42, 0.75);
            --bg-surface-solid: #0f172a;
            --bg-elevated: #1e293b;
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --primary-glow: rgba(99, 102, 241, 0.35);
            --secondary: #06b6d4;
            --accent: #38bdf8;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #f43f5e;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-glass: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(99, 102, 241, 0.4);
            --gradient-brand: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
            --radius-card: 16px;
            --radius-btn: 8px;
            --radius-input: 10px;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-base);
            color: var(--text-main);
            min-height: 100vh;
            line-height: 1.6;
            background-image: 
                radial-gradient(circle at 10% 15%, rgba(99, 102, 241, 0.10) 0%, transparent 40%),
                radial-gradient(circle at 90% 25%, rgba(6, 182, 212, 0.08) 0%, transparent 40%);
            background-attachment: fixed;
        }

        /* --- STICKY GLASS NAVBAR --- */
        .navbar {
            position: sticky;
            top: 0;
            z-index: 1000;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            background: rgba(9, 13, 22, 0.85);
            border-bottom: 1px solid var(--border-glass);
            padding: 0.85rem 1.5rem;
        }
        .nav-container {
            max-width: 1180px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
            color: var(--text-main);
        }
        .brand-badge {
            background: var(--gradient-brand);
            padding: 0.35rem 0.65rem;
            border-radius: 8px;
            color: white;
            font-weight: 800;
            font-size: 0.9rem;
            letter-spacing: 0.05em;
            box-shadow: 0 4px 15px var(--primary-glow);
        }
        .brand-title {
            font-weight: 700;
            font-size: 1.15rem;
            letter-spacing: -0.02em;
        }
        .nav-links {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        .nav-link {
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 600;
            padding: 0.45rem 0.9rem;
            border-radius: var(--radius-btn);
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }
        .nav-link:hover {
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
        }
        .nav-link.active {
            color: #ffffff;
            background: rgba(99, 102, 241, 0.2);
            border: 1px solid rgba(99, 102, 241, 0.4);
        }
        .btn-swagger {
            background: rgba(16, 185, 129, 0.15) !important;
            color: #34d399 !important;
            border: 1px solid rgba(16, 185, 129, 0.3) !important;
        }
        .btn-swagger:hover {
            background: rgba(16, 185, 129, 0.25) !important;
        }

        /* --- LAYOUT CONTAINER --- */
        .container {
            max-width: 1180px;
            margin: 2rem auto;
            padding: 0 1.5rem 3rem;
        }

        /* --- HERO & PAGE HEADERS --- */
        .page-header {
            margin-bottom: 2rem;
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1.5rem;
            flex-wrap: wrap;
        }
        .page-header h1 {
            font-size: 2.25rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .page-header p {
            color: var(--text-muted);
            font-size: 1.05rem;
            max-width: 650px;
        }

        /* --- STAT WIDGETS --- */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-card);
            padding: 1.25rem 1.5rem;
            backdrop-filter: blur(16px);
            transition: transform 0.2s, border-color 0.2s;
        }
        .stat-card:hover {
            transform: translateY(-2px);
            border-color: var(--border-glow);
        }
        .stat-label {
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-muted);
            margin-bottom: 0.4rem;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.1;
        }

        /* --- CARDS & PANELS --- */
        .card {
            background: var(--bg-surface);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-card);
            padding: 1.75rem;
            backdrop-filter: blur(16px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
            margin-bottom: 1.75rem;
        }
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.25rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--border-glass);
        }
        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* --- BUTTONS --- */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            padding: 0.65rem 1.25rem;
            border-radius: var(--radius-btn);
            font-weight: 600;
            font-size: 0.9rem;
            text-decoration: none;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
        }
        .btn:active { transform: scale(0.98); }
        .btn-primary {
            background: var(--gradient-brand);
            color: white;
            box-shadow: 0 4px 14px var(--primary-glow);
        }
        .btn-primary:hover {
            opacity: 0.92;
            box-shadow: 0 6px 18px var(--primary-glow);
        }
        .btn-secondary {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid var(--border-glass);
            color: var(--text-main);
        }
        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.12);
        }
        .btn-danger {
            background: rgba(244, 63, 94, 0.15);
            border: 1px solid rgba(244, 63, 94, 0.35);
            color: #fb7185;
        }
        .btn-danger:hover {
            background: rgba(244, 63, 94, 0.25);
        }
        .btn-sm {
            padding: 0.35rem 0.75rem;
            font-size: 0.8rem;
            border-radius: 6px;
        }

        /* --- FORMS & INPUTS --- */
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.25rem;
            margin-bottom: 1.25rem;
        }
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }
        .form-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
        }
        .form-input, .form-select, .form-textarea {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-input);
            padding: 0.7rem 0.9rem;
            color: var(--text-main);
            font-size: 0.95rem;
            font-family: inherit;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .form-input:focus, .form-select:focus, .form-textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25);
        }

        /* --- DATA TABLES --- */
        .table-responsive {
            overflow-x: auto;
            border-radius: 12px;
            border: 1px solid var(--border-glass);
        }
        table.data-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.95rem;
        }
        table.data-table th {
            background: rgba(30, 41, 59, 0.85);
            padding: 0.9rem 1.25rem;
            font-weight: 700;
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 1px solid var(--border-glass);
        }
        table.data-table td {
            padding: 1rem 1.25rem;
            border-bottom: 1px solid var(--border-glass);
            color: var(--text-main);
        }
        table.data-table tbody tr:hover {
            background: rgba(99, 102, 241, 0.06);
        }

        /* --- BADGES & STATUS PILLS --- */
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.65rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.04em;
        }
        .badge-pending { background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }
        .badge-reviewed { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
        .badge-accepted { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
        .badge-rejected { background: rgba(244, 63, 94, 0.15); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.3); }
        .badge-info { background: rgba(99, 102, 241, 0.15); color: #a5b4fc; border: 1px solid rgba(99, 102, 241, 0.3); }

        /* --- FOOTER --- */
        footer.app-footer {
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border-glass);
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
        }
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin-bottom: 0.75rem;
            flex-wrap: wrap;
        }
        .footer-link {
            color: var(--text-muted);
            text-decoration: none;
            transition: color 0.2s;
        }
        .footer-link:hover { color: var(--accent); }
    """


def render_navbar(active_route: str = "") -> str:
    """Renders the unified glassmorphic top navigation bar"""
    def is_active(route_prefix: str) -> str:
        return "active" if active_route == route_prefix else ""

    return f"""
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="brand">
                <span class="brand-badge">ALUMNI</span>
                <span class="brand-title">Ecosystem</span>
            </a>
            <div class="nav-links">
                <a href="/users/" class="nav-link {is_active('users')}">👥 Users</a>
                <a href="/announcements/" class="nav-link {is_active('announcements')}">📢 Notices</a>
                <a href="/job-postings/" class="nav-link {is_active('jobs')}">💼 Careers</a>
                <a href="/applications/" class="nav-link {is_active('applications')}">📝 Applications</a>
                <a href="/api/swagger" class="nav-link btn-swagger" target="_blank">📖 Swagger</a>
            </div>
        </div>
    </nav>
    """


def render_footer() -> str:
    """Renders the unified brand footer"""
    return """
    <footer class="app-footer">
        <div class="footer-links">
            <a href="/brand.md" class="footer-link">🎨 Brand Guidelines</a>
            <a href="/DESIGN.md" class="footer-link">📐 Design System</a>
            <a href="/ddd.md" class="footer-link">📊 Data Design</a>
            <a href="/api/health" class="footer-link">⚡ System Health</a>
        </div>
        <p>Department of Management Information Systems • Istanbul University of Economics • MVC Lab</p>
    </footer>
    """
