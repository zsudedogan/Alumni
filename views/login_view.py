"""
Login View - UniBridge Design System (Istanbul University Theme)
Renders the responsive authentication page for student, alumni, academic, and administrative login.
Palette: Forest Green (#204729), Warm Gold (#C59B27), Sage (#F4F7F5), Crisp White.
"""

from views.components import get_base_css, render_navbar, render_footer, render_iu_logo


def render_login_page(error: str = None, next_url: str = "/admin/", email_value: str = "") -> str:
    """Renders the UniBridge Login Portal view"""

    error_html = ""
    if error:
        error_msg = error
        if error == "auth_required":
            error_msg = "Yönetim paneline erişmek için lütfen önce giriş yapınız."
        elif error == "invalid_credentials":
            error_msg = "Hatalı e-posta veya şifre girdiniz. Lütfen bilgilerinizi kontrol ediniz."
        elif error == "logged_out":
            error_msg = "Başarıyla çıkış yaptınız."

        bg_color = "#fef2f2" if error != "logged_out" else "#f0fdf4"
        text_color = "#991b1b" if error != "logged_out" else "#166534"
        border_color = "rgba(239, 68, 68, 0.3)" if error != "logged_out" else "rgba(34, 197, 94, 0.3)"

        error_html = f"""
        <div style="background: {bg_color}; border: 1px solid {border_color}; color: {text_color}; padding: 0.85rem 1.25rem; border-radius: 10px; margin-bottom: 1.5rem; font-size: 0.9rem; display: flex; align-items: center; gap: 0.6rem;">
            <span>ℹ️</span>
            <span>{error_msg}</span>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Giriş Yap • UniBridge İstanbul Üniversitesi</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        {get_base_css()}

        .login-wrapper {{
            max-width: 480px;
            margin: 2.5rem auto 4rem;
        }}
        .login-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            box-shadow: 0 10px 30px rgba(32, 71, 41, 0.08);
            padding: 2.5rem 2.25rem;
            position: relative;
        }}
        .login-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--accent-gold) 100%);
            border-top-left-radius: var(--radius-card);
            border-top-right-radius: var(--radius-card);
        }}
        .login-header {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        .login-title {{
            font-size: 1.6rem;
            font-weight: 800;
            color: var(--primary);
            letter-spacing: -0.02em;
            margin-top: 0.75rem;
            margin-bottom: 0.35rem;
        }}
        .login-subtitle {{
            font-size: 0.9rem;
            color: var(--text-muted);
        }}
        .quick-hint-box {{
            background: rgba(197, 155, 39, 0.08);
            border: 1px dashed rgba(197, 155, 39, 0.4);
            border-radius: 10px;
            padding: 0.85rem 1rem;
            margin-top: 1.5rem;
            font-size: 0.85rem;
            color: #785a08;
        }}
        .quick-hint-box strong {{
            color: #553e02;
        }}
    </style>
</head>
<body>
    {render_navbar(active_route="login")}

    <main class="container">
        <div class="login-wrapper">
            <div class="login-card">
                <div class="login-header">
                    {render_iu_logo(size=54)}
                    <h1 class="login-title">UniBridge Giriş</h1>
                    <p class="login-subtitle">İstanbul Üniversitesi Kimlik & Kariyer Kapısı</p>
                </div>

                {error_html}

                <form action="/login/" method="POST" id="loginForm">
                    <input type="hidden" name="next" value="{next_url}">

                    <div class="form-group">
                        <label class="form-label" for="email">Kurumsal / Kayıtlı E-Posta</label>
                        <input type="email" id="email" name="email" class="form-input" placeholder="ornek@example.com" value="{email_value}" required autocomplete="username">
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="password">Şifre</label>
                        <input type="password" id="password" name="password" class="form-input" placeholder="••••••••" required autocomplete="current-password">
                    </div>

                    <button type="submit" class="btn btn-primary" style="width: 100%; justify-content: center; padding: 0.85rem; font-size: 1rem; margin-top: 0.5rem;">
                        <span>🔐</span>
                        <span>Giriş Yap</span>
                    </button>
                </form>

                <div class="quick-hint-box">
                    <div style="font-weight: 700; margin-bottom: 0.25rem;">👑 Yönetici (Admin) Giriş Bilgileri:</div>
                    <div>E-posta: <strong>sude@example.com</strong></div>
                    <div>Şifre: <strong>password123</strong></div>
                    <div style="font-size: 0.78rem; margin-top: 0.35rem; color: #8c6b12;">(Rol: Sude Doğan - Admin Paneli Tam Yetkili)</div>
                </div>

                <div style="text-align: center; margin-top: 1.75rem; font-size: 0.9rem; color: var(--text-muted);">
                    Hesabınız yok mu? <a href="/register/" style="color: var(--primary); font-weight: 700; text-decoration: none;">Kayıt Olun</a>
                </div>
            </div>
        </div>
    </main>

    {render_footer()}
</body>
</html>"""
