"""
Register View - UniBridge Design System (Istanbul University Standard)
Renders the HTML View Layer for User Registration matching UniBridge aesthetics.
"""

from views.components import get_base_css, render_navbar, render_footer, render_iu_logo


def render_register_page() -> str:
    """
    Renders the UniBridge registration page allowing users to register
    with their designated role (Student, Alumni, Recruiter, Academic), credentials, and profile details.
    """
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hesap Oluştur • UniBridge İstanbul Üniversitesi</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
        <style>
            {get_base_css()}

            .register-container {{
                max-width: 760px;
                margin: 2rem auto 4rem;
            }}

            .register-card {{
                background: #ffffff;
                border: 1px solid var(--border-card);
                border-radius: var(--radius-card);
                padding: 2.5rem;
                box-shadow: var(--shadow-elevated);
                position: relative;
            }}

            .unibridge-header {{
                text-align: center;
                margin-bottom: 2rem;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0.75rem;
            }}

            .unibridge-header h1 {{
                font-size: 2.2rem;
                font-weight: 800;
                color: var(--primary);
                letter-spacing: -0.02em;
                margin: 0;
            }}

            .unibridge-header p {{
                color: var(--text-muted);
                font-size: 1rem;
                margin: 0;
                max-width: 520px;
            }}

            .role-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 1rem;
                margin-top: 0.5rem;
            }}

            @media (max-width: 640px) {{
                .role-grid {{
                    grid-template-columns: 1fr;
                }}
                .register-card {{
                    padding: 1.5rem;
                }}
            }}

            .role-option {{
                position: relative;
                border: 1.5px solid rgba(0, 0, 0, 0.08);
                background: #fafcfb;
                border-radius: 16px;
                padding: 1.15rem 1.25rem;
                cursor: pointer;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                display: flex;
                flex-direction: column;
                gap: 0.4rem;
            }}

            .role-option:hover {{
                border-color: rgba(32, 71, 41, 0.35);
                background: #ffffff;
                transform: translateY(-2px);
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.04);
            }}

            .role-option.selected {{
                border-color: var(--primary);
                background: #ffffff;
                box-shadow: 0 0 0 2px rgba(32, 71, 41, 0.2), 0 8px 20px rgba(32, 71, 41, 0.08);
            }}

            .role-header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
            }}

            .role-title {{
                font-weight: 800;
                font-size: 1.05rem;
                color: var(--primary);
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }}

            .role-desc {{
                font-size: 0.82rem;
                color: var(--text-muted);
                line-height: 1.45;
            }}

            .form-row {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1.25rem;
            }}

            @media (max-width: 600px) {{
                .form-row {{
                    grid-template-columns: 1fr;
                }}
            }}

            .password-hint {{
                font-size: 0.76rem;
                color: var(--text-muted);
                margin-top: 0.35rem;
            }}

            .alert-banner {{
                display: none;
                padding: 1rem 1.25rem;
                border-radius: 12px;
                margin-bottom: 1.5rem;
                font-size: 0.92rem;
                font-weight: 600;
            }}

            .alert-banner.success {{
                display: flex;
                align-items: center;
                gap: 0.75rem;
                background: #dcfce7;
                border: 1px solid rgba(21, 128, 61, 0.3);
                color: #15803d;
            }}

            .alert-banner.error {{
                display: flex;
                align-items: center;
                gap: 0.75rem;
                background: #fee2e2;
                border: 1px solid rgba(185, 28, 28, 0.3);
                color: #b91c1c;
            }}
        </style>
    </head>
    <body>
        {render_navbar(active_route="register")}

        <div class="container">
            <div class="register-container">
                <div class="unibridge-header">
                    {render_iu_logo(size=84)}
                    <h1>UniBridge Kayıt Portalı • Join Alumni Ecosystem</h1>
                    <p>İstanbul Üniversitesi mezunlar ağı, staj ve kariyer ekosistemine hemen katılın.</p>
                </div>

                <div class="register-card">
                    <div id="alert-box" class="alert-banner"></div>

                    <form id="register-form" onsubmit="handleRegister(event)">
                        <!-- Role Selection (UniBridge Style) -->
                        <div class="form-group" style="margin-bottom: 1.75rem;">
                            <label class="form-label">Select Your Role / Kullanıcı Tipinizi Seçin *</label>
                            <input type="hidden" id="selected-role" value="Student">
                            
                            <div class="role-grid">
                                <div class="role-option selected" id="opt-Student" onclick="selectRole('Student')">
                                    <div class="role-header">
                                        <div class="role-title">🎓 Öğrenci <span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">(Student)</span></div>
                                        <span class="badge badge-student">Varsayılan</span>
                                    </div>
                                    <div class="role-desc">Aktif öğrenciler için staj arama, kariyer etkinlikleri ve mentorluk erişimi.</div>
                                </div>

                                <div class="role-option" id="opt-Alumni" onclick="selectRole('Alumni')">
                                    <div class="role-header">
                                        <div class="role-title">🎖️ Mezun <span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">(Alumni)</span></div>
                                        <span class="badge badge-alumni">Mezunlar Ağı</span>
                                    </div>
                                    <div class="role-desc">Mezunlar ağı, sektör tecrübesi paylaşımı ve kariyer fırsatları portalı.</div>
                                </div>

                                <div class="role-option" id="opt-Recruiter" onclick="selectRole('Recruiter')">
                                    <div class="role-header">
                                        <div class="role-title">🏢 İşveren / İK <span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">(Recruiter)</span></div>
                                        <span class="badge badge-recruiter">Sektör</span>
                                    </div>
                                    <div class="role-desc">Kurumsal şirketler ve yetenek avcıları için iş/staj ilanı ve aday değerlendirme.</div>
                                </div>

                                <div class="role-option" id="opt-Academic" onclick="selectRole('Academic')">
                                    <div class="role-header">
                                        <div class="role-title">🖥️ Akademik <span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">(Academic)</span></div>
                                        <span class="badge badge-academic">Fakülte</span>
                                    </div>
                                    <div class="role-desc">Öğretim üyeleri ve bölüm danışmanları için akademik koordinasyon paneli.</div>
                                </div>
                            </div>
                        </div>

                        <!-- Personal Info -->
                        <div class="form-row" style="margin-bottom: 1.25rem;">
                            <div class="form-group">
                                <label class="form-label" for="reg-name">Ad Soyad *</label>
                                <input class="form-input" type="text" id="reg-name" required placeholder="Örn: Sude Doğan">
                            </div>
                            <div class="form-group">
                                <label class="form-label" for="reg-email">E-posta Adresi *</label>
                                <input class="form-input" type="email" id="reg-email" required placeholder="Örn: sude@istanbul.edu.tr">
                            </div>
                        </div>

                        <!-- Credentials & Age -->
                        <div class="form-row" style="margin-bottom: 1.25rem;">
                            <div class="form-group">
                                <label class="form-label" for="reg-password">Şifre *</label>
                                <input class="form-input" type="password" id="reg-password" required minlength="6" placeholder="En az 6 karakter">
                                <div class="password-hint">🔒 Minimum 6 karakterli güvenli şifre</div>
                            </div>
                            <div class="form-group">
                                <label class="form-label" for="reg-age">Yaş (Opsiyonel)</label>
                                <input class="form-input" type="number" id="reg-age" min="16" max="100" placeholder="Örn: 22">
                            </div>
                        </div>

                        <!-- Department / Company -->
                        <div class="form-group" style="margin-bottom: 1.25rem;">
                            <label class="form-label" for="reg-department" id="dept-label">Bölüm / Program</label>
                            <input class="form-input" type="text" id="reg-department" placeholder="Örn: Yönetim Bilişim Sistemleri">
                        </div>

                        <!-- Bio -->
                        <div class="form-group" style="margin-bottom: 2rem;">
                            <label class="form-label" for="reg-bio">Hakkınızda / Biyografi (Opsiyonel)</label>
                            <textarea class="form-textarea" id="reg-bio" rows="3" placeholder="İlgi alanlarınız, kariyer hedefleriniz veya uzmanlıklarınız hakkında kısa bilgi..."></textarea>
                        </div>

                        <button type="submit" class="btn btn-primary" id="reg-submit-btn" style="width: 100%; padding: 0.95rem; font-size: 1.05rem;">
                            Giriş Yap / Kaydı Tamamla
                        </button>
                    </form>

                    <div style="margin-top: 1.5rem; text-align: center; color: var(--text-muted); font-size: 0.9rem;">
                        Zaten bir hesabınız var mı? <a href="/users/" style="color: var(--accent-gold); text-decoration: none; font-weight: 700;">Kullanıcı Rehberini İnceleyin &rarr;</a>
                    </div>
                </div>
            </div>

            {render_footer()}
        </div>

        <script>
            function selectRole(role) {{
                document.getElementById('selected-role').value = role;
                ['Student', 'Alumni', 'Recruiter', 'Academic'].forEach(r => {{
                    const el = document.getElementById('opt-' + r);
                    if (el) {{
                        if (r === role) el.classList.add('selected');
                        else el.classList.remove('selected');
                    }}
                }});

                const deptLabel = document.getElementById('dept-label');
                const deptInput = document.getElementById('reg-department');
                if (role === 'Recruiter') {{
                    deptLabel.innerText = 'Şirket / Kurum Adı *';
                    deptInput.placeholder = 'Örn: Google / SoftTech A.Ş.';
                }} else if (role === 'Academic') {{
                    deptLabel.innerText = 'Fakülte / Akademik Bölüm *';
                    deptInput.placeholder = 'Örn: İktisat Fakültesi / YBS Bölümü';
                }} else if (role === 'Alumni') {{
                    deptLabel.innerText = 'Mezun Olunan Bölüm / Çalışılan Kurum';
                    deptInput.placeholder = 'Örn: Bilgisayar Mühendisliği (2023 Mezunu)';
                }} else {{
                    deptLabel.innerText = 'Bölüm / Program';
                    deptInput.placeholder = 'Örn: Yönetim Bilişim Sistemleri';
                }}
            }}

            async function handleRegister(e) {{
                e.preventDefault();
                const alertBox = document.getElementById('alert-box');
                const submitBtn = document.getElementById('reg-submit-btn');

                alertBox.className = 'alert-banner';
                alertBox.style.display = 'none';

                const name = document.getElementById('reg-name').value.trim();
                const email = document.getElementById('reg-email').value.trim();
                const password = document.getElementById('reg-password').value;
                const role = document.getElementById('selected-role').value;
                const department = document.getElementById('reg-department').value.trim() || null;
                const ageVal = document.getElementById('reg-age').value;
                const age = ageVal ? parseInt(ageVal) : null;
                const bio = document.getElementById('reg-bio').value.trim() || null;

                if (!name || !email || !password) {{
                    showAlert('Lütfen tüm zorunlu alanları doldurunuz.', 'error');
                    return;
                }}

                if (password.length < 6) {{
                    showAlert('Şifre en az 6 karakter uzunluğunda olmalıdır.', 'error');
                    return;
                }}

                submitBtn.disabled = true;
                submitBtn.innerText = '⏳ Kayıt İşleniyor...';

                try {{
                    const response = await fetch('/api/auth/register', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            name,
                            email,
                            password,
                            role,
                            department,
                            age,
                            bio
                        }})
                    }});

                    const data = await response.json();

                    if (response.ok) {{
                        showAlert('🎉 Hoş geldiniz, ' + name + '! (' + role + ') rolüyle kaydınız başarıyla oluşturuldu. Kullanıcı rehberine yönlendiriliyorsunuz...', 'success');
                        document.getElementById('register-form').reset();
                        setTimeout(() => {{
                            window.location.href = '/users/';
                        }}, 1800);
                    }} else {{
                        const detail = data.detail || data.reason || 'Kayıt gerçekleştirilemedi. Lütfen bilgilerinizi kontrol ediniz.';
                        showAlert(typeof detail === 'string' ? detail : JSON.stringify(detail), 'error');
                        submitBtn.disabled = false;
                        submitBtn.innerText = 'Giriş Yap / Kaydı Tamamla';
                    }}
                }} catch (err) {{
                    showAlert('Bağlantı hatası: ' + err.message, 'error');
                    submitBtn.disabled = false;
                    submitBtn.innerText = 'Giriş Yap / Kaydı Tamamla';
                }}
            }}

            function showAlert(msg, type) {{
                const alertBox = document.getElementById('alert-box');
                alertBox.className = 'alert-banner ' + type;
                alertBox.innerHTML = msg;
                alertBox.style.display = 'flex';
                window.scrollTo({{ top: alertBox.offsetTop - 20, behavior: 'smooth' }});
            }}
        </script>
    </body>
    </html>
    """
