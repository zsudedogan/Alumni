"""
Admin Panel View - UniBridge Design System (Istanbul University Theme)
Provides comprehensive data administration dashboard for Users, Announcements, Job Postings, and Applications.
Color Palette: Forest Green (#204729), Warm Gold (#C59B27), Sage (#F4F7F5), Card White (#FFFFFF).
"""

from typing import List, Dict, Any
from views.components import get_base_css, render_navbar, render_footer, render_iu_logo


def render_admin_dashboard(
    current_user: Any,
    users: List[Any],
    announcements: List[Any],
    jobs: List[Any],
    applications: List[Any],
    message: str = None,
    error: str = None
) -> str:
    """Renders the comprehensive UniBridge Admin Control Dashboard"""

    # Calculate statistics
    total_users = len(users)
    admin_count = sum(1 for u in users if u.role == "Admin")
    student_count = sum(1 for u in users if u.role == "Student")
    alumni_count = sum(1 for u in users if u.role == "Alumni")
    total_announcements = len(announcements)
    total_jobs = len(jobs)
    active_jobs = sum(1 for j in jobs if getattr(j, "is_active", True))
    total_apps = len(applications)

    # Flash alert message
    alert_html = ""
    if message:
        alert_html = f"""
        <div style="background: #f0fdf4; border: 1px solid rgba(34, 197, 94, 0.3); color: #166534; padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <span style="font-size: 1.2rem;">✅</span>
                <span><strong>İşlem Başarılı:</strong> {message}</span>
            </div>
            <button onclick="this.parentElement.remove()" style="background: none; border: none; font-size: 1.1rem; cursor: pointer; color: #166534;">✕</button>
        </div>
        """
    elif error:
        alert_html = f"""
        <div style="background: #fef2f2; border: 1px solid rgba(239, 68, 68, 0.3); color: #991b1b; padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <span style="font-size: 1.2rem;">⚠️</span>
                <span><strong>Hata:</strong> {error}</span>
            </div>
            <button onclick="this.parentElement.remove()" style="background: none; border: none; font-size: 1.1rem; cursor: pointer; color: #991b1b;">✕</button>
        </div>
        """

    # Build User Rows
    user_rows_html = ""
    for u in users:
        role_badge_class = f"badge-{u.role.lower()}" if u.role.lower() in ("student", "alumni", "recruiter", "academic", "admin") else "badge-info"
        is_self = (u.id == current_user.id)
        
        user_rows_html += f"""
        <tr>
            <td style="font-weight: 700; color: var(--text-muted);">#{u.id}</td>
            <td>
                <div style="font-weight: 700; color: var(--primary);">{u.name}</div>
                <div style="font-size: 0.8rem; color: var(--text-muted);">{u.department or 'Bölüm Belirtilmemiş'}</div>
            </td>
            <td><code>{u.email or '-'}</code></td>
            <td>
                <form action="/admin/users/{u.id}/role" method="POST" style="display: inline-flex; align-items: center; gap: 0.4rem; margin: 0;">
                    <select name="role" class="form-input" style="padding: 0.25rem 0.5rem; font-size: 0.8rem; width: auto; border-radius: 6px;">
                        <option value="Admin" {'selected' if u.role == 'Admin' else ''}>👑 Admin</option>
                        <option value="Student" {'selected' if u.role == 'Student' else ''}>🎓 Öğrenci</option>
                        <option value="Alumni" {'selected' if u.role == 'Alumni' else ''}>📜 Mezun</option>
                        <option value="Academic" {'selected' if u.role == 'Academic' else ''}>🏛️ Akademik</option>
                        <option value="Recruiter" {'selected' if u.role == 'Recruiter' else ''}>💼 İşveren</option>
                    </select>
                    <button type="submit" class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;">Güncelle</button>
                </form>
            </td>
            <td>
                <div style="display: flex; gap: 0.4rem; align-items: center;">
                    <button onclick="openEditUserModal({u.id}, '{u.name}', '{u.email or ''}', '{u.department or ''}', '{u.role}')" class="btn btn-secondary" style="padding: 0.3rem 0.6rem; font-size: 0.8rem;">✏️ Düzenle</button>
                    {'' if is_self else f'''
                    <form action="/admin/users/{u.id}/delete" method="POST" onsubmit="return confirm('{u.name} kullanıcısını silmek istediğinize emin misiniz?');" style="margin: 0; display: inline;">
                        <button type="submit" class="btn btn-danger" style="padding: 0.3rem 0.6rem; font-size: 0.8rem;">🗑️ Sil</button>
                    </form>
                    '''}
                </div>
            </td>
        </tr>
        """

    # Build Announcement Rows
    announcement_rows_html = ""
    for a in announcements:
        announcement_rows_html += f"""
        <tr>
            <td style="font-weight: 700; color: var(--text-muted);">#{a.id}</td>
            <td>
                <div style="font-weight: 700; color: var(--text-main);">{a.title}</div>
                <div style="font-size: 0.82rem; color: var(--text-muted); max-width: 350px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{a.content}</div>
            </td>
            <td><span class="badge badge-info">{a.category or 'Genel'}</span></td>
            <td><span style="font-weight: 600;">{a.author or 'Admin'}</span></td>
            <td><span style="font-size: 0.85rem; color: var(--text-muted);">{a.date or '-'}</span></td>
            <td>
                <form action="/admin/announcements/{a.id}/delete" method="POST" onsubmit="return confirm('Bu duyuruyu silmek istediğinize emin misiniz?');" style="margin: 0; display: inline;">
                    <button type="submit" class="btn btn-danger" style="padding: 0.3rem 0.6rem; font-size: 0.8rem;">🗑️ Sil</button>
                </form>
            </td>
        </tr>
        """

    # Build Job Rows
    job_rows_html = ""
    for j in jobs:
        is_active = getattr(j, "is_active", True)
        status_badge = '<span class="badge badge-accepted">Aktif</span>' if is_active else '<span class="badge badge-rejected">Pasif</span>'
        toggle_label = "Pasif Yap" if is_active else "Aktif Yap"
        toggle_class = "btn-secondary" if is_active else "btn-primary"

        job_rows_html += f"""
        <tr>
            <td style="font-weight: 700; color: var(--text-muted);">#{j.id}</td>
            <td>
                <div style="font-weight: 700; color: var(--primary);">{j.title}</div>
                <div style="font-size: 0.8rem; color: var(--text-muted);">{j.job_type or 'Tam Zamanlı'}</div>
            </td>
            <td><strong>{j.company}</strong></td>
            <td>{j.location or 'Remote'}</td>
            <td>{status_badge}</td>
            <td>
                <div style="display: flex; gap: 0.4rem; align-items: center;">
                    <form action="/admin/jobs/{j.id}/toggle" method="POST" style="margin: 0; display: inline;">
                        <button type="submit" class="btn {toggle_class}" style="padding: 0.3rem 0.6rem; font-size: 0.8rem;">{toggle_label}</button>
                    </form>
                    <form action="/admin/jobs/{j.id}/delete" method="POST" onsubmit="return confirm('Bu iş ilanını silmek istediğinize emin misiniz?');" style="margin: 0; display: inline;">
                        <button type="submit" class="btn btn-danger" style="padding: 0.3rem 0.6rem; font-size: 0.8rem;">🗑️ Sil</button>
                    </form>
                </div>
            </td>
        </tr>
        """

    # Build Application Rows
    application_rows_html = ""
    for app in applications:
        status_val = app.status or "Pending"
        badge_cls = f"badge-{status_val.lower()}"
        app_rows_job_title = getattr(app, "job_title", f"İş İlanı #{app.job_id}")
        app_rows_user_name = getattr(app, "applicant_name", f"Kullanıcı #{app.user_id}")

        application_rows_html += f"""
        <tr>
            <td style="font-weight: 700; color: var(--text-muted);">#{app.id}</td>
            <td>
                <div style="font-weight: 700; color: var(--primary);">{app_rows_job_title}</div>
                <div style="font-size: 0.8rem; color: var(--text-muted);">İlan ID: #{app.job_id}</div>
            </td>
            <td>
                <div style="font-weight: 700;">{app_rows_user_name}</div>
                <div style="font-size: 0.8rem; color: var(--text-muted);">Aday ID: #{app.user_id}</div>
            </td>
            <td>
                <form action="/admin/applications/{app.id}/status" method="POST" style="display: inline-flex; align-items: center; gap: 0.4rem; margin: 0;">
                    <select name="status" class="form-input" style="padding: 0.25rem 0.5rem; font-size: 0.8rem; width: auto; border-radius: 6px;">
                        <option value="Pending" {'selected' if status_val == 'Pending' else ''}>⏳ Bekliyor</option>
                        <option value="Reviewed" {'selected' if status_val == 'Reviewed' else ''}>🔍 İncelendi</option>
                        <option value="Accepted" {'selected' if status_val == 'Accepted' else ''}>✅ Kabul Edildi</option>
                        <option value="Rejected" {'selected' if status_val == 'Rejected' else ''}>❌ Reddedildi</option>
                    </select>
                    <button type="submit" class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;">Kaydet</button>
                </form>
            </td>
            <td>
                <form action="/admin/applications/{app.id}/delete" method="POST" onsubmit="return confirm('Bu başvuruyu silmek istediğinize emin misiniz?');" style="margin: 0; display: inline;">
                    <button type="submit" class="btn btn-danger" style="padding: 0.3rem 0.6rem; font-size: 0.8rem;">🗑️ Sil</button>
                </form>
            </td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yönetim Paneli (Admin) • UniBridge İstanbul Üniversitesi</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        {get_base_css()}

        /* Admin Dashboard Styles */
        .admin-header-box {{
            background: linear-gradient(135deg, #1b3d23 0%, #204729 60%, #2f5e3a 100%);
            color: white;
            border-radius: var(--radius-card);
            padding: 2rem 2.5rem;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1.5rem;
            flex-wrap: wrap;
            box-shadow: 0 10px 25px rgba(32, 71, 41, 0.15);
        }}
        .admin-title {{
            font-size: 1.8rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 0.35rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        .admin-subtitle {{
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.95rem;
        }}
        .admin-user-pill {{
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.25);
            padding: 0.6rem 1.2rem;
            border-radius: 9999px;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            backdrop-filter: blur(8px);
        }}

        /* Tab Navigation */
        .tabs-header {{
            display: flex;
            gap: 0.5rem;
            border-bottom: 2px solid var(--border-card);
            margin-bottom: 1.75rem;
            overflow-x: auto;
        }}
        .tab-btn {{
            background: none;
            border: none;
            padding: 0.85rem 1.4rem;
            font-weight: 700;
            font-size: 0.95rem;
            color: var(--text-muted);
            cursor: pointer;
            border-bottom: 3px solid transparent;
            margin-bottom: -2px;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.2s;
            white-space: nowrap;
        }}
        .tab-btn:hover {{
            color: var(--primary);
        }}
        .tab-btn.active {{
            color: var(--primary);
            border-bottom-color: var(--primary);
        }}
        .tab-pane {{
            display: none;
        }}
        .tab-pane.active {{
            display: block;
        }}

        /* Action Modal */
        .modal-overlay {{
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            z-index: 2000;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }}
        .modal-box {{
            background: white;
            border-radius: var(--radius-card);
            max-width: 500px;
            width: 100%;
            padding: 2rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }}
    </style>
</head>
<body>
    {render_navbar(active_route="admin", current_user=current_user)}

    <main class="container">
        <!-- Top Admin Header -->
        <div class="admin-header-box">
            <div>
                <div class="admin-title">
                    <span>👑</span>
                    <span>UniBridge Yönetim Paneli</span>
                </div>
                <div class="admin-subtitle">Sistem veri manipülasyonu, kullanıcı yetkilendirme ve içerik kontrolü</div>
            </div>
            <div class="admin-user-pill">
                <span>👤</span>
                <div>
                    <div style="font-weight: 700; font-size: 0.9rem;">{current_user.name}</div>
                    <div style="font-size: 0.75rem; color: #fef08a; font-weight: 700;">YÖNETİCİ (ADMIN)</div>
                </div>
                <a href="/logout/" class="btn btn-secondary" style="padding: 0.3rem 0.7rem; font-size: 0.75rem; margin-left: 0.5rem; background: rgba(255,255,255,0.2); color: white; border: none;">Çıkış</a>
            </div>
        </div>

        {alert_html}

        <!-- Quick Stats Grid -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Toplam Kullanıcı</div>
                <div class="stat-value">{total_users}</div>
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.4rem;">
                    👑 {admin_count} Admin • 🎓 {student_count} Öğrenci • 📜 {alumni_count} Mezun
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Toplam Duyuru</div>
                <div class="stat-value">{total_announcements}</div>
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.4rem;">
                    Yayınlanmış kurumsal bildirimler
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Kariyer & İlanlar</div>
                <div class="stat-value">{total_jobs}</div>
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.4rem;">
                    🟢 {active_jobs} Aktif İlan
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Alınan Başvurular</div>
                <div class="stat-value">{total_apps}</div>
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.4rem;">
                    Aday kariyer başvuruları
                </div>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="tabs-header">
            <button class="tab-btn active" onclick="switchTab('usersTab', this)">
                <span>👥</span> Kullanıcılar ({total_users})
            </button>
            <button class="tab-btn" onclick="switchTab('announcementsTab', this)">
                <span>📢</span> Duyurular ({total_announcements})
            </button>
            <button class="tab-btn" onclick="switchTab('jobsTab', this)">
                <span>💼</span> İş İlanları ({total_jobs})
            </button>
            <button class="tab-btn" onclick="switchTab('applicationsTab', this)">
                <span>📝</span> Başvurular ({total_apps})
            </button>
        </div>

        <!-- TAB 1: USERS MANAGEMENT -->
        <div id="usersTab" class="tab-pane active">
            <div class="card" style="margin-bottom: 2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <h2 style="font-size: 1.3rem; color: var(--primary); margin-bottom: 0.2rem;">Kullanıcı Yönetimi & Rol Değiştirme</h2>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">Tüm kayıtlı kullanıcıları listeleyin, rollerini Admin / Öğrenci / Mezun olarak değiştirin veya silin.</p>
                    </div>
                    <button onclick="document.getElementById('addUserModal').style.display='flex'" class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.85rem;">
                        <span>➕</span> Yeni Kullanıcı Ekle
                    </button>
                </div>

                <div style="overflow-x: auto;">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Kullanıcı</th>
                                <th>E-posta</th>
                                <th>Yetki / Rol</th>
                                <th>İşlemler</th>
                            </tr>
                        </thead>
                        <tbody>
                            {user_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 2: ANNOUNCEMENTS MANAGEMENT -->
        <div id="announcementsTab" class="tab-pane">
            <div class="card" style="margin-bottom: 2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <h2 style="font-size: 1.3rem; color: var(--primary); margin-bottom: 0.2rem;">Duyuru & Bildirim Yönetimi</h2>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">Sistem genelindeki duyuruları yayınlayın veya silin.</p>
                    </div>
                    <button onclick="document.getElementById('addAnnouncementModal').style.display='flex'" class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.85rem;">
                        <span>📢</span> Yeni Duyuru Yayınla
                    </button>
                </div>

                <div style="overflow-x: auto;">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Başlık & İçerik</th>
                                <th>Kategori</th>
                                <th>Yazar</th>
                                <th>Tarih</th>
                                <th>İşlem</th>
                            </tr>
                        </thead>
                        <tbody>
                            {announcement_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 3: JOBS MANAGEMENT -->
        <div id="jobsTab" class="tab-pane">
            <div class="card" style="margin-bottom: 2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <h2 style="font-size: 1.3rem; color: var(--primary); margin-bottom: 0.2rem;">Kariyer & İlan Yönetimi</h2>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">İlanların durumunu Aktif/Pasif olarak değiştirin veya kaldırın.</p>
                    </div>
                </div>

                <div style="overflow-x: auto;">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>İlan Başlığı</th>
                                <th>Şirket</th>
                                <th>Konum</th>
                                <th>Durum</th>
                                <th>İşlemler</th>
                            </tr>
                        </thead>
                        <tbody>
                            {job_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 4: APPLICATIONS MANAGEMENT -->
        <div id="applicationsTab" class="tab-pane">
            <div class="card" style="margin-bottom: 2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <h2 style="font-size: 1.3rem; color: var(--primary); margin-bottom: 0.2rem;">Başvuru Yönetimi</h2>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">Aday başvurularının durumunu güncelleyin (Bekliyor, İncelendi, Kabul Edildi, Reddedildi).</p>
                    </div>
                </div>

                <div style="overflow-x: auto;">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>İlan Bilgisi</th>
                                <th>Aday Bilgisi</th>
                                <th>Durum Güncelle</th>
                                <th>İşlem</th>
                            </tr>
                        </thead>
                        <tbody>
                            {application_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- MODAL: ADD USER -->
        <div id="addUserModal" class="modal-overlay">
            <div class="modal-box">
                <h3 style="font-size: 1.25rem; color: var(--primary); margin-bottom: 1rem;">➕ Yeni Kullanıcı Oluştur</h3>
                <form action="/admin/users/create" method="POST">
                    <div class="form-group">
                        <label class="form-label">Ad Soyad</label>
                        <input type="text" name="name" class="form-input" required placeholder="Örn: Ayşe Demir">
                    </div>
                    <div class="form-group">
                        <label class="form-label">E-posta</label>
                        <input type="email" name="email" class="form-input" required placeholder="ayse@example.com">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Şifre</label>
                        <input type="password" name="password" class="form-input" required placeholder="••••••••" value="password123">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Rol</label>
                        <select name="role" class="form-input">
                            <option value="Student">🎓 Öğrenci</option>
                            <option value="Alumni">📜 Mezun</option>
                            <option value="Academic">🏛️ Akademik</option>
                            <option value="Recruiter">💼 İşveren</option>
                            <option value="Admin">👑 Admin</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Bölüm</label>
                        <input type="text" name="department" class="form-input" placeholder="Örn: Yönetim Bilişim Sistemleri">
                    </div>
                    <div style="display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 1.5rem;">
                        <button type="button" onclick="document.getElementById('addUserModal').style.display='none'" class="btn btn-secondary">İptal</button>
                        <button type="submit" class="btn btn-primary">Kaydet</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- MODAL: EDIT USER -->
        <div id="editUserModal" class="modal-overlay">
            <div class="modal-box">
                <h3 style="font-size: 1.25rem; color: var(--primary); margin-bottom: 1rem;">✏️ Kullanıcı Bilgilerini Güncelle</h3>
                <form id="editUserForm" action="" method="POST">
                    <div class="form-group">
                        <label class="form-label">Ad Soyad</label>
                        <input type="text" id="editUserName" name="name" class="form-input" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">E-posta</label>
                        <input type="email" id="editUserEmail" name="email" class="form-input" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Bölüm</label>
                        <input type="text" id="editUserDept" name="department" class="form-input">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Rol</label>
                        <select id="editUserRole" name="role" class="form-input">
                            <option value="Admin">👑 Admin</option>
                            <option value="Student">🎓 Öğrenci</option>
                            <option value="Alumni">📜 Mezun</option>
                            <option value="Academic">🏛️ Akademik</option>
                            <option value="Recruiter">💼 İşveren</option>
                        </select>
                    </div>
                    <div style="display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 1.5rem;">
                        <button type="button" onclick="document.getElementById('editUserModal').style.display='none'" class="btn btn-secondary">İptal</button>
                        <button type="submit" class="btn btn-primary">Güncelle</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- MODAL: ADD ANNOUNCEMENT -->
        <div id="addAnnouncementModal" class="modal-overlay">
            <div class="modal-box">
                <h3 style="font-size: 1.25rem; color: var(--primary); margin-bottom: 1rem;">📢 Yeni Duyuru Yayınla</h3>
                <form action="/admin/announcements/create" method="POST">
                    <div class="form-group">
                        <label class="form-label">Duyuru Başlığı</label>
                        <input type="text" name="title" class="form-input" required placeholder="Örn: 2026 Bahar Kariyer Fuarı">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Kategori</label>
                        <input type="text" name="category" class="form-input" placeholder="Örn: Kariyer, Etkinlik, Akademik" value="Genel">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Duyuru Metni</label>
                        <textarea name="content" class="form-input" rows="4" required placeholder="Duyuru detaylarını buraya yazınız..."></textarea>
                    </div>
                    <div style="display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 1.5rem;">
                        <button type="button" onclick="document.getElementById('addAnnouncementModal').style.display='none'" class="btn btn-secondary">İptal</button>
                        <button type="submit" class="btn btn-primary">Yayınla</button>
                    </div>
                </form>
            </div>
        </div>

    </main>

    <script>
        function switchTab(tabId, btn) {{
            document.querySelectorAll('.tab-pane').forEach(function(p) {{ p.classList.remove('active'); }});
            document.querySelectorAll('.tab-btn').forEach(function(b) {{ b.classList.remove('active'); }});
            document.getElementById(tabId).classList.add('active');
            btn.classList.add('active');
        }}

        function openEditUserModal(id, name, email, dept, role) {{
            document.getElementById('editUserForm').action = '/admin/users/' + id + '/edit';
            document.getElementById('editUserName').value = name;
            document.getElementById('editUserEmail').value = email;
            document.getElementById('editUserDept').value = dept;
            document.getElementById('editUserRole').value = role;
            document.getElementById('editUserModal').style.display = 'flex';
        }}
    </script>

    {render_footer()}
</body>
</html>"""
