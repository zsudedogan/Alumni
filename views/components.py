"""
Shared View Components & Styles - UniBridge Design System (Istanbul University Standard)
Implements clean light aesthetics, Istanbul University Forest Green and Warm Gold palettes,
and card-based role portal interfaces.
"""

from typing import Any, Optional



def render_iu_logo(size: int = 84) -> str:
    """Renders the official high-fidelity circular T.C. İstanbul Üniversitesi seal (1453)"""
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 4px 10px rgba(32, 71, 41, 0.15));">
        <!-- Outer Gold & Green Decorative Rings -->
        <circle cx="60" cy="60" r="58" stroke="#c59b27" stroke-width="2.5" fill="#ffffff" />
        <circle cx="60" cy="60" r="54" stroke="#204729" stroke-width="1.2" fill="#ffffff" />
        <circle cx="60" cy="60" r="39" stroke="#c59b27" stroke-width="2" fill="#204729" />

        <!-- Circular Arc Paths for Lettering -->
        <defs>
            <path id="iu-arc-top" d="M 20,60 A 40,40 0 1,1 100,60" fill="none" />
            <path id="iu-arc-bottom" d="M 100,60 A 40,40 0 0,1 20,60" fill="none" />
        </defs>

        <!-- Top Text: T.C. İSTANBUL ÜNİVERSİTESİ -->
        <text font-family="'Plus Jakarta Sans', Arial, sans-serif" font-size="6.8" font-weight="800" fill="#204729" letter-spacing="1.2px">
            <textPath href="#iu-arc-top" startOffset="50%" text-anchor="middle">
                T.C. İSTANBUL ÜNİVERSİTESİ
            </textPath>
        </text>

        <!-- Bottom Text: * 1453 * -->
        <text font-family="'Plus Jakarta Sans', Arial, sans-serif" font-size="7.5" font-weight="800" fill="#c59b27" letter-spacing="2.5px">
            <textPath href="#iu-arc-bottom" startOffset="50%" text-anchor="middle">
                ★ 1453 ★
            </textPath>
        </text>

        <!-- Central Historic Ornament / University Tree Motif -->
        <g transform="translate(60,60) scale(0.68)">
            <!-- Central Trunk & Leaf Branches -->
            <path d="M -3,-22 C -3,-26 3,-26 3,-22 L 3,-8 C 7,-6 12,-1 12,8 C 12,17 5,23 0,23 C -5,23 -12,17 -12,8 C -12,-1 -7,-6 -3,-8 Z" fill="#c59b27" stroke="#ffffff" stroke-width="0.8" />
            <circle cx="0" cy="-22" r="3" fill="#ffffff" />
            <circle cx="-10" cy="-6" r="3.2" fill="#c59b27" stroke="#ffffff" stroke-width="0.7" />
            <circle cx="10" cy="-6" r="3.2" fill="#c59b27" stroke="#ffffff" stroke-width="0.7" />
            <circle cx="-15" cy="5" r="3.2" fill="#c59b27" stroke="#ffffff" stroke-width="0.7" />
            <circle cx="15" cy="5" r="3.2" fill="#c59b27" stroke="#ffffff" stroke-width="0.7" />
            <circle cx="-8" cy="13" r="3" fill="#c59b27" stroke="#ffffff" stroke-width="0.7" />
            <circle cx="8" cy="13" r="3" fill="#c59b27" stroke="#ffffff" stroke-width="0.7" />
            <circle cx="0" cy="5" r="3.8" fill="#ffffff" />
        </g>
    </svg>
    """


def get_base_css() -> str:
    """Returns global design system CSS tokens and component styles matching UniBridge standard"""
    return """
        :root {
            /* Palette: Istanbul University Forest Green & Warm Gold */
            --bg-base: #f4f7f5;
            --bg-surface: #ffffff;
            --bg-surface-solid: #ffffff;
            --bg-elevated: #fafcfb;
            --primary: #204729;
            --primary-dark: #17351e;
            --primary-light: #2d5e36;
            --primary-glow: rgba(32, 71, 41, 0.18);
            --secondary: #52795d;
            --accent: #c59b27;
            --accent-gold: #c59b27;
            --accent-light: #fef6e7;
            --success: #15803d;
            --warning: #d97706;
            --danger: #dc2626;
            --text-main: #152418;
            --text-muted: #5e6d62;
            --text-light: #8a988d;
            --border-glass: rgba(0, 0, 0, 0.07);
            --border-card: rgba(0, 0, 0, 0.06);
            --border-glow: rgba(32, 71, 41, 0.25);
            --shadow-card: 0 10px 30px rgba(0, 0, 0, 0.04);
            --shadow-elevated: 0 20px 40px rgba(0, 0, 0, 0.06);
            --radius-card: 20px;
            --radius-btn: 12px;
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
                radial-gradient(circle at 10% 10%, rgba(32, 71, 41, 0.03) 0%, transparent 45%),
                radial-gradient(circle at 90% 20%, rgba(197, 155, 39, 0.04) 0%, transparent 45%);
            background-attachment: fixed;
        }

        /* --- STICKY CLEAN NAVBAR --- */
        .navbar {
            position: sticky;
            top: 0;
            z-index: 1000;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            background: rgba(255, 255, 255, 0.94);
            border-bottom: 1px solid var(--border-glass);
            box-shadow: 0 2px 15px rgba(0, 0, 0, 0.03);
            padding: 0.75rem 1.5rem;
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
            background: var(--primary);
            padding: 0.35rem 0.65rem;
            border-radius: 8px;
            color: white;
            font-weight: 800;
            font-size: 0.85rem;
            letter-spacing: 0.05em;
            box-shadow: 0 2px 8px var(--primary-glow);
        }
        .brand-title {
            font-weight: 800;
            font-size: 1.15rem;
            color: var(--primary);
            letter-spacing: -0.02em;
        }
        .brand-sub {
            font-size: 0.75rem;
            color: var(--accent-gold);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .nav-links {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            flex-wrap: wrap;
        }
        .nav-link {
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 600;
            padding: 0.45rem 0.85rem;
            border-radius: 8px;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }
        .nav-link:hover {
            color: var(--primary);
            background: rgba(32, 71, 41, 0.05);
        }
        .nav-link.active {
            color: var(--primary);
            background: rgba(32, 71, 41, 0.08);
            border: 1px solid rgba(32, 71, 41, 0.18);
            font-weight: 700;
        }
        .btn-swagger {
            background: rgba(197, 155, 39, 0.12) !important;
            color: #9a7210 !important;
            border: 1px solid rgba(197, 155, 39, 0.3) !important;
        }
        .btn-swagger:hover {
            background: rgba(197, 155, 39, 0.2) !important;
        }

        /* --- LAYOUT CONTAINER --- */
        .container {
            max-width: 1180px;
            margin: 2rem auto;
            padding: 0 1.5rem 3rem;
        }

        /* --- HEADERS --- */
        .page-header {
            margin-bottom: 2rem;
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1.5rem;
            flex-wrap: wrap;
        }
        .page-header h1 {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 0.4rem;
            color: var(--primary);
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
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 1.25rem 1.5rem;
            box-shadow: var(--shadow-card);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-elevated);
        }
        .stat-label {
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-muted);
            margin-bottom: 0.4rem;
        }
        .stat-value {
            font-size: 1.85rem;
            font-weight: 800;
            color: var(--primary);
            line-height: 1.1;
        }

        /* --- CARDS & PANELS --- */
        .card {
            background: var(--bg-surface);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 1.75rem;
            box-shadow: var(--shadow-card);
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
            font-size: 1.2rem;
            font-weight: 800;
            color: var(--primary);
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
            padding: 0.75rem 1.4rem;
            border-radius: var(--radius-btn);
            font-weight: 700;
            font-size: 0.92rem;
            text-decoration: none;
            cursor: pointer;
            border: none;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .btn:active { transform: scale(0.98); }
        .btn-primary {
            background: var(--primary);
            color: #ffffff !important;
            box-shadow: 0 4px 12px var(--primary-glow);
        }
        .btn-primary:hover {
            background: var(--primary-dark);
            box-shadow: 0 6px 18px var(--primary-glow);
            transform: translateY(-1px);
        }
        .btn-secondary {
            background: #ffffff;
            border: 1px solid rgba(0, 0, 0, 0.12);
            color: var(--text-main);
        }
        .btn-secondary:hover {
            background: #f8faf8;
            border-color: rgba(32, 71, 41, 0.3);
            color: var(--primary);
        }
        .btn-danger {
            background: rgba(220, 38, 38, 0.1);
            border: 1px solid rgba(220, 38, 38, 0.25);
            color: #b91c1c;
        }
        .btn-danger:hover {
            background: rgba(220, 38, 38, 0.18);
        }
        .btn-sm {
            padding: 0.4rem 0.85rem;
            font-size: 0.82rem;
            border-radius: 8px;
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
            font-weight: 700;
            color: var(--text-main);
        }
        .form-input, .form-select, .form-textarea {
            background: #ffffff;
            border: 1px solid rgba(0, 0, 0, 0.14);
            border-radius: var(--radius-input);
            padding: 0.75rem 0.95rem;
            color: var(--text-main);
            font-size: 0.95rem;
            font-family: inherit;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .form-input:focus, .form-select:focus, .form-textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(32, 71, 41, 0.12);
        }

        /* --- DATA TABLES --- */
        .table-responsive {
            overflow-x: auto;
            border-radius: 14px;
            border: 1px solid var(--border-glass);
            background: #ffffff;
        }
        table.data-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.95rem;
        }
        table.data-table th {
            background: #f7faf8;
            padding: 0.9rem 1.25rem;
            font-weight: 700;
            font-size: 0.78rem;
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
            background: rgba(32, 71, 41, 0.03);
        }

        /* --- BADGES & STATUS PILLS (UniBridge Standard) --- */
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 0.28rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.03em;
        }
        .badge-pending { background: #fef3c7; color: #b45309; border: 1px solid rgba(180, 83, 9, 0.2); }
        .badge-reviewed { background: #e0f2fe; color: #0369a1; border: 1px solid rgba(3, 105, 161, 0.2); }
        .badge-accepted { background: #dcfce7; color: #15803d; border: 1px solid rgba(21, 128, 61, 0.2); }
        .badge-rejected { background: #fee2e2; color: #b91c1c; border: 1px solid rgba(185, 28, 28, 0.2); }
        .badge-info { background: rgba(32, 71, 41, 0.08); color: var(--primary); border: 1px solid rgba(32, 71, 41, 0.18); }
        .badge-student { background: #e8f3fc; color: #1d4ed8; border: 1px solid rgba(29, 78, 216, 0.25); }
        .badge-alumni { background: #fef6e7; color: #b45309; border: 1px solid rgba(180, 83, 9, 0.25); }
        .badge-recruiter { background: #e6f4ea; color: #15803d; border: 1px solid rgba(21, 128, 61, 0.25); }
        .badge-academic { background: #ede9fe; color: #6b21a8; border: 1px solid rgba(107, 33, 168, 0.25); }
        .badge-admin { background: #fef08a; color: #854d0e; border: 1px solid rgba(133, 77, 14, 0.35); font-weight: 800; }

        /* --- FOOTER (UniBridge Standard) --- */
        footer.app-footer {
            margin-top: 4.5rem;
            padding-top: 2rem;
            padding-bottom: 2rem;
            border-top: 1px solid var(--border-glass);
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
        }
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 1.75rem;
            margin-top: 0.75rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }
        .footer-link {
            color: var(--accent-gold);
            text-decoration: none;
            font-weight: 700;
            transition: color 0.2s;
        }
        .footer-link:hover { color: #9a7210; text-decoration: underline; }
        .footer-copy {
            font-weight: 600;
            color: var(--text-muted);
            letter-spacing: 0.03em;
        }
    """


def render_navbar(active_route: str = "", current_user: Any = None) -> str:
    """Renders the UniBridge top navigation bar with Istanbul University seal and authentication links"""
    def is_active(route_prefix: str) -> str:
        return "active" if active_route == route_prefix else ""

    auth_links = ""
    if current_user:
        admin_link = ""
        if getattr(current_user, "role", "") == "Admin":
            admin_link = f'<a href="/admin/" class="nav-link {is_active("admin")}" style="background: rgba(197, 155, 39, 0.15); color: #854d0e; border: 1px solid rgba(197, 155, 39, 0.35); font-weight: 700;">👑 Admin Paneli</a>'

        auth_links = f"""
        {admin_link}
        <a href="/logout/" class="nav-link" style="color: #991b1b;" title="Oturumu Kapat">🚪 Çıkış ({getattr(current_user, 'name', 'Kullanıcı')})</a>
        """
    else:
        auth_links = f"""
        <a href="/login/" class="nav-link {is_active('login')}">🔐 Giriş</a>
        <a href="/register/" class="nav-link {is_active('register')}">✨ Kayıt Ol</a>
        """

    return f"""
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="brand">
                {render_iu_logo(size=38)}
                <div>
                    <div class="brand-title">UniBridge</div>
                    <div class="brand-sub">İstanbul Üniversitesi</div>
                </div>
            </a>
            <div class="nav-links">
                <a href="/users/" class="nav-link {is_active('users')}">👥 Users</a>
                <a href="/announcements/" class="nav-link {is_active('announcements')}">📢 Notices</a>
                <a href="/job-postings/" class="nav-link {is_active('jobs')}">💼 Careers</a>
                <a href="/applications/" class="nav-link {is_active('applications')}">📝 Applications</a>
                {auth_links}
                <a href="/api/swagger" class="nav-link btn-swagger" target="_blank">📖 Swagger</a>
            </div>
        </div>
    </nav>
    """


def render_footer() -> str:
    """Renders the official Istanbul University UniBridge footer"""
    return """
    <footer class="app-footer">
        <p class="footer-copy">© 2025 İSTANBUL ÜNİVERSİTESİ BİLGİ İŞLEM SİSTEMİ</p>
        <div class="footer-links">
            <a href="#" class="footer-link">Yardım Merkezi</a>
            <a href="#" class="footer-link">Kullanım Koşulları</a>
            <a href="/brand.md" class="footer-link">Brand Guidelines</a>
            <a href="/DESIGN.md" class="footer-link">Design System</a>
            <a href="/api/health" class="footer-link">Sistem Durumu</a>
        </div>
    </footer>
    """
