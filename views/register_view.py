"""
Register View - MVC Architecture
Renders the HTML View Layer for User Registration (VoltAgent DESIGN.md & brand.md Standard).
"""

from views.components import get_base_css, render_navbar, render_footer


def render_register_page() -> str:
    """
    Renders the modern, glassmorphic registration page allowing users to register
    with their designated role (Student, Alumni, Recruiter, Academic), credentials, and profile details.
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Create Your Account - Alumni Ecosystem</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
        <style>
            {get_base_css()}

            .register-container {{
                max-width: 760px;
                margin: 2rem auto;
            }}

            .register-card {{
                background: var(--bg-surface);
                border: 1px solid var(--border-glass);
                border-radius: var(--radius-card);
                padding: 2.5rem;
                backdrop-filter: blur(20px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45);
                position: relative;
                overflow: hidden;
            }}

            .register-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: var(--gradient-brand);
            }}

            .role-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 1rem;
                margin-top: 0.5rem;
            }}

            @media (max-width: 600px) {{
                .role-grid {{
                    grid-template-columns: 1fr;
                }}
                .register-card {{
                    padding: 1.5rem;
                }}
            }}

            .role-option {{
                position: relative;
                border: 1px solid var(--border-glass);
                background: rgba(15, 23, 42, 0.6);
                border-radius: var(--radius-card);
                padding: 1rem 1.25rem;
                cursor: pointer;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                display: flex;
                flex-direction: column;
                gap: 0.35rem;
            }}

            .role-option:hover {{
                border-color: rgba(99, 102, 241, 0.5);
                background: rgba(30, 41, 59, 0.7);
                transform: translateY(-2px);
            }}

            .role-option.selected {{
                border-color: var(--primary);
                background: rgba(99, 102, 241, 0.12);
                box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.35);
            }}

            .role-header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
            }}

            .role-title {{
                font-weight: 700;
                font-size: 1rem;
                color: #ffffff;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }}

            .role-desc {{
                font-size: 0.8rem;
                color: var(--text-muted);
                line-height: 1.4;
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
                font-size: 0.75rem;
                color: var(--text-muted);
                margin-top: 0.35rem;
            }}

            .alert-banner {{
                display: none;
                padding: 1rem 1.25rem;
                border-radius: var(--radius-card);
                margin-bottom: 1.5rem;
                font-size: 0.9rem;
            }}

            .alert-banner.success {{
                display: flex;
                align-items: center;
                gap: 0.75rem;
                background: rgba(16, 185, 129, 0.15);
                border: 1px solid rgba(16, 185, 129, 0.4);
                color: #34d399;
            }}

            .alert-banner.error {{
                display: flex;
                align-items: center;
                gap: 0.75rem;
                background: rgba(244, 63, 94, 0.15);
                border: 1px solid rgba(244, 63, 94, 0.4);
                color: #fb7185;
            }}
        </style>
    </head>
    <body>
        {render_navbar(active_route="register")}

        <div class="container">
            <div class="register-container">
                <div class="page-header" style="text-align: center; justify-content: center; margin-bottom: 1.5rem;">
                    <div>
                        <span class="badge badge-info" style="margin-bottom: 0.75rem;">Account Setup</span>
                        <h1>Join Alumni Ecosystem</h1>
                        <p style="margin: 0 auto;">Connect with graduates, explore exclusive career openings, or recruit top university talent.</p>
                    </div>
                </div>

                <div class="register-card">
                    <div id="alert-box" class="alert-banner"></div>

                    <form id="register-form" onsubmit="handleRegister(event)">
                        <!-- Role Selection -->
                        <div class="form-group" style="margin-bottom: 1.75rem;">
                            <label class="form-label">Select Your Role in the Ecosystem *</label>
                            <input type="hidden" id="selected-role" value="Student">
                            
                            <div class="role-grid">
                                <div class="role-option selected" id="opt-Student" onclick="selectRole('Student')">
                                    <div class="role-header">
                                        <div class="role-title">🎓 Student</div>
                                        <span class="badge badge-student">Default</span>
                                    </div>
                                    <div class="role-desc">Undergraduate or graduate seeking mentorship, internships, and opportunities.</div>
                                </div>

                                <div class="role-option" id="opt-Alumni" onclick="selectRole('Alumni')">
                                    <div class="role-header">
                                        <div class="role-title">💼 Alumni</div>
                                        <span class="badge badge-alumni">Graduate</span>
                                    </div>
                                    <div class="role-desc">Graduated professional offering mentorship, industry insights, and career guidance.</div>
                                </div>

                                <div class="role-option" id="opt-Recruiter" onclick="selectRole('Recruiter')">
                                    <div class="role-header">
                                        <div class="role-title">🏢 Recruiter</div>
                                        <span class="badge badge-recruiter">Hiring</span>
                                    </div>
                                    <div class="role-desc">Company HR or talent partner seeking qualified alumni & students for full-time/intern roles.</div>
                                </div>

                                <div class="role-option" id="opt-Academic" onclick="selectRole('Academic')">
                                    <div class="role-header">
                                        <div class="role-title">🏛️ Academic</div>
                                        <span class="badge badge-academic">Faculty</span>
                                    </div>
                                    <div class="role-desc">University professors and department staff coordinating student career advancement.</div>
                                </div>
                            </div>
                        </div>

                        <!-- Personal Info -->
                        <div class="form-row" style="margin-bottom: 1.25rem;">
                            <div class="form-group">
                                <label class="form-label" for="reg-name">Full Name *</label>
                                <input class="form-input" type="text" id="reg-name" required placeholder="e.g. Sude Dogan">
                            </div>
                            <div class="form-group">
                                <label class="form-label" for="reg-email">Email Address *</label>
                                <input class="form-input" type="email" id="reg-email" required placeholder="e.g. sude@alumni.edu">
                            </div>
                        </div>

                        <!-- Credentials & Age -->
                        <div class="form-row" style="margin-bottom: 1.25rem;">
                            <div class="form-group">
                                <label class="form-label" for="reg-password">Password *</label>
                                <input class="form-input" type="password" id="reg-password" required minlength="6" placeholder="Min 6 characters">
                                <div class="password-hint">🔒 Securely stored with minimum 6 characters</div>
                            </div>
                            <div class="form-group">
                                <label class="form-label" for="reg-age">Age (Optional)</label>
                                <input class="form-input" type="number" id="reg-age" min="16" max="100" placeholder="e.g. 23">
                            </div>
                        </div>

                        <!-- Department / Company -->
                        <div class="form-group" style="margin-bottom: 1.25rem;">
                            <label class="form-label" for="reg-department" id="dept-label">Department / Major</label>
                            <input class="form-input" type="text" id="reg-department" placeholder="e.g. Computer Science, Google, or Information Systems">
                        </div>

                        <!-- Bio -->
                        <div class="form-group" style="margin-bottom: 2rem;">
                            <label class="form-label" for="reg-bio">Short Bio / Professional Summary (Optional)</label>
                            <textarea class="form-input" id="reg-bio" rows="3" placeholder="Tell the community about your interests, current work, or aspirations..."></textarea>
                        </div>

                        <button type="submit" class="btn btn-primary" id="reg-submit-btn" style="width: 100%; padding: 0.9rem; font-size: 1rem; font-weight: 700;">
                            ✨ Complete Registration
                        </button>
                    </form>

                    <div style="margin-top: 1.5rem; text-align: center; color: var(--text-muted); font-size: 0.85rem;">
                        Already registered? <a href="/users/" style="color: var(--accent); text-decoration: none; font-weight: 600;">Browse User Directory &rarr;</a>
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

                // Dynamic label update
                const deptLabel = document.getElementById('dept-label');
                const deptInput = document.getElementById('reg-department');
                if (role === 'Recruiter') {{
                    deptLabel.innerText = 'Company / Organization Name *';
                    deptInput.placeholder = 'e.g. TechCorp Solutions';
                }} else if (role === 'Academic') {{
                    deptLabel.innerText = 'Faculty / Academic Department *';
                    deptInput.placeholder = 'e.g. Department of Software Engineering';
                }} else if (role === 'Alumni') {{
                    deptLabel.innerText = 'Graduated Major / Current Company';
                    deptInput.placeholder = 'e.g. Management Information Systems (2024)';
                }} else {{
                    deptLabel.innerText = 'Department / Major';
                    deptInput.placeholder = 'e.g. Computer Engineering';
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
                    showAlert('Please fill in all required fields.', 'error');
                    return;
                }}

                if (password.length < 6) {{
                    showAlert('Password must be at least 6 characters long.', 'error');
                    return;
                }}

                submitBtn.disabled = true;
                submitBtn.innerText = '⏳ Registering Account...';

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
                        showAlert('🎉 Welcome aboard, ' + name + '! Your account as a <strong>' + role + '</strong> was successfully created. Redirecting to directory...', 'success');
                        document.getElementById('register-form').reset();
                        setTimeout(() => {{
                            window.location.href = '/users/';
                        }}, 1800);
                    }} else {{
                        const detail = data.detail || 'Registration failed. Please verify your details.';
                        showAlert(typeof detail === 'string' ? detail : JSON.stringify(detail), 'error');
                        submitBtn.disabled = false;
                        submitBtn.innerText = '✨ Complete Registration';
                    }}
                }} catch (err) {{
                    showAlert('Network error: ' + err.message, 'error');
                    submitBtn.disabled = false;
                    submitBtn.innerText = '✨ Complete Registration';
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
