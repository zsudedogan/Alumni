"""
Portal Views - UniBridge Design System (Istanbul University Theme)
Provides dedicated, tailored web portals for Student, Alumni, Recruiter, and Academic roles.
Color Palette: Forest Green (#204729), Warm Gold (#C59B27), Sage (#F4F7F5), Crisp White.
"""

from typing import List, Any
from views.components import get_base_css, render_navbar, render_footer, render_iu_logo


def render_student_portal(
    student: Any,
    jobs: List[Any],
    applications: List[Any],
    announcements: List[Any]
) -> str:
    """Renders the dedicated Student Career & Internship Portal view"""
    student_name = getattr(student, "name", "Öğrenci")
    student_dept = getattr(student, "department", "Bölüm Belirtilmemiş") or "Bölüm Belirtilmemiş"

    # Job Cards HTML
    job_cards_html = ""
    for j in jobs[:6]:
        job_cards_html += f"""
        <div class="card" style="display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.75rem;">
                    <span class="badge badge-recruiter">{j.company}</span>
                    <span class="badge badge-info">{j.job_type or 'Tam Zamanlı'}</span>
                </div>
                <h3 style="font-size:1.15rem; color:var(--primary); margin-bottom:0.4rem;">{j.title}</h3>
                <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.85rem;">📍 {j.location or 'Remote'}</p>
                <div style="font-size:0.85rem; color:var(--text-main); line-height:1.5; margin-bottom:1rem; max-height:60px; overflow:hidden;">
                    {j.description or 'Açık staj ve iş pozisyonu.'}
                </div>
            </div>
            <a href="/job-postings/" class="btn btn-primary" style="width:100%; justify-content:center; padding:0.5rem; font-size:0.85rem;">
                İlana Başvur →
            </a>
        </div>
        """

    # Applications HTML
    app_rows_html = ""
    for app in applications:
        status_val = getattr(app, "status", "Pending") or "Pending"
        badge_cls = f"badge-{status_val.lower()}"
        job_title = getattr(app, "job_title", f"İlan #{app.job_id}")
        app_rows_html += f"""
        <tr>
            <td style="font-weight:700; color:var(--primary);">{job_title}</td>
            <td>İlan #{app.job_id}</td>
            <td><span class="badge {badge_cls}">{status_val}</span></td>
            <td><code>{getattr(app, 'created_at', '-') or '-'}</code></td>
        </tr>
        """
    if not app_rows_html:
        app_rows_html = '<tr><td colspan="4" style="text-align:center; color:var(--text-muted); padding:2rem;">Henüz bir iş veya staj başvurunuz bulunmamaktadır.</td></tr>'

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Öğrenci Portalı • UniBridge İstanbul Üniversitesi</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        {get_base_css()}
        .portal-hero {{
            background: linear-gradient(135deg, #1b3d23 0%, #204729 60%, #2a5834 100%);
            color: white;
            border-radius: var(--radius-card);
            padding: 2.25rem 2.5rem;
            margin-bottom: 2.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
            box-shadow: 0 10px 25px rgba(32, 71, 41, 0.15);
        }}
    </style>
</head>
<body>
    {render_navbar(active_route="portal_student", current_user=student)}

    <main class="container">
        <!-- Hero Header -->
        <div class="portal-hero">
            <div>
                <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
                    <span class="badge badge-student" style="background:rgba(255,255,255,0.2); color:white; border:none;">🎓 AKTİF ÖĞRENCİ</span>
                    <span style="font-size:0.85rem; color:#fef08a;">{student_dept}</span>
                </div>
                <h1 style="font-size:2rem; font-weight:800; margin:0 0 0.5rem;">Hoş Geldin, {student_name}!</h1>
                <p style="color:rgba(255,255,255,0.85); margin:0; font-size:1rem;">İstanbul Üniversitesi Kariyer & Staj Merkezi Öğrenci Arayüzü</p>
            </div>
            <div style="display:flex; gap:0.75rem;">
                <a href="/job-postings/" class="btn btn-secondary" style="background:white; color:var(--primary); font-weight:700;">💼 İlanları İncele</a>
                <a href="/users/" class="btn btn-secondary" style="background:rgba(255,255,255,0.15); color:white; border:1px solid rgba(255,255,255,0.3);">🤝 Mezun Ağı</a>
            </div>
        </div>

        <!-- Quick Stats -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Açık İş & Staj İlanları</div>
                <div class="stat-value">{len(jobs)}</div>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.4rem;">Başvuruya açık aktif pozisyonlar</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Başvurularım</div>
                <div class="stat-value">{len(applications)}</div>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.4rem;">Takipteki başvuru durumu</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Akademik Duyurular</div>
                <div class="stat-value">{len(announcements)}</div>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.4rem;">Fakülte ve bölüm ilanları</div>
            </div>
        </div>

        <!-- Section 1: Recommended Postings -->
        <div style="margin-bottom: 2.5rem;">
            <div class="page-header" style="margin-bottom: 1.25rem;">
                <div>
                    <h2>💼 Öne Çıkan Staj ve Kariyer Fırsatları</h2>
                    <p>Öğrencilerimiz için kurumsal ortaklarımız ve mezunlarımız tarafından açılan pozisyonlar.</p>
                </div>
                <a href="/job-postings/" class="btn btn-secondary">Tüm İlanları Gör →</a>
            </div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:1.25rem;">
                {job_cards_html}
            </div>
        </div>

        <!-- Section 2: My Applications -->
        <div id="my-applications" class="card" style="margin-bottom: 2.5rem;">
            <h3 style="font-size:1.3rem; color:var(--primary); margin-bottom:1rem;">📝 Başvuru Takip Çizelgesi</h3>
            <div style="overflow-x:auto;">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Pozisyon</th>
                            <th>İlan Referansı</th>
                            <th>Başvuru Durumu</th>
                            <th>Tarih</th>
                        </tr>
                    </thead>
                    <tbody>
                        {app_rows_html}
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    {render_footer()}
</body>
</html>"""


def render_alumni_portal(
    alumni: Any,
    alumni_jobs: List[Any],
    all_alumni: List[Any],
    announcements: List[Any]
) -> str:
    """Renders the dedicated Alumni Solidarity & Mentorship Portal view"""
    alumni_name = getattr(alumni, "name", "Mezun")
    alumni_dept = getattr(alumni, "department", "Bölüm Belirtilmemiş") or "Bölüm Belirtilmemiş"

    alumni_cards = ""
    for a in all_alumni[:6]:
        alumni_cards += f"""
        <div class="card" style="padding:1.25rem;">
            <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.75rem;">
                <div style="width:40px; height:40px; border-radius:50%; background:var(--accent-gold); color:white; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.9rem;">
                    {a.name[:2].upper()}
                </div>
                <div>
                    <div style="font-weight:700; color:var(--text-main);">{a.name}</div>
                    <div style="font-size:0.8rem; color:var(--text-muted);">{a.department or 'Mezun'}</div>
                </div>
            </div>
            <div style="font-size:0.85rem; color:var(--text-muted); line-height:1.4;">
                {getattr(a, 'bio', '') or 'İstanbul Üniversitesi Mezunlar Ağı Üyesi'}
            </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mezun Portalı • UniBridge İstanbul Üniversitesi</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        {get_base_css()}
        .portal-hero {{
            background: linear-gradient(135deg, #785a08 0%, #a1780d 50%, #c59b27 100%);
            color: white;
            border-radius: var(--radius-card);
            padding: 2.25rem 2.5rem;
            margin-bottom: 2.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
            box-shadow: 0 10px 25px rgba(197, 155, 39, 0.2);
        }}
    </style>
</head>
<body>
    {render_navbar(active_route="portal_alumni", current_user=alumni)}

    <main class="container">
        <!-- Hero Header -->
        <div class="portal-hero">
            <div>
                <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
                    <span class="badge badge-alumni" style="background:rgba(255,255,255,0.25); color:white; border:none;">📜 DEĞERLİ MEZUNUMUZ</span>
                    <span style="font-size:0.85rem; color:#fef9c3;">{alumni_dept}</span>
                </div>
                <h1 style="font-size:2rem; font-weight:800; margin:0 0 0.5rem;">Hoş Geldin, {alumni_name}!</h1>
                <p style="color:rgba(255,255,255,0.9); margin:0; font-size:1rem;">İstanbul Üniversitesi Mezunlar Dayanışma & Mentorluk Portalı</p>
            </div>
            <div style="display:flex; gap:0.75rem;">
                <a href="/job-postings/" class="btn btn-primary" style="background:#204729; border:none;">➕ İlan Yayınla</a>
                <a href="/users/" class="btn btn-secondary" style="background:white; color:#785a08; font-weight:700;">🤝 Mezun Rehberi</a>
            </div>
        </div>

        <!-- Quick Stats -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Kayıtlı Mezun Sayısı</div>
                <div class="stat-value">{len(all_alumni)}</div>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.4rem;">Mezun topluluk üyeleri</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Yayınlanan İlanlar</div>
                <div class="stat-value">{len(alumni_jobs)}</div>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.4rem;">Öğrencilere sunulan fırsatlar</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Bölüm Duyuruları</div>
                <div class="stat-value">{len(announcements)}</div>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.4rem;">Akademik & mezun bültenleri</div>
            </div>
        </div>

        <!-- Section: Alumni Network Grid -->
        <div style="margin-bottom:2.5rem;">
            <div class="page-header" style="margin-bottom:1.25rem;">
                <div>
                    <h2>🤝 Mezun Mentorluk ve Ağ Paylaşımı</h2>
                    <p>Farklı dönem ve sektörlerdeki İÜ mezunlarıyla iletişime geçin, iş birlikleri kurun.</p>
                </div>
                <a href="/users/" class="btn btn-secondary">Tüm Mezunları Gör →</a>
            </div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:1.25rem;">
                {alumni_cards}
            </div>
        </div>
    </main>

    {render_footer()}
</body>
</html>"""


def render_recruiter_portal(
    recruiter: Any,
    posted_jobs: List[Any],
    applications: List[Any],
    talent_pool: List[Any]
) -> str:
    """Renders the dedicated Corporate Recruiter & Talent Portal view"""
    recruiter_name = getattr(recruiter, "name", "İşveren")
    recruiter_comp = getattr(recruiter, "department", "Kurumsal Firma") or "Kurumsal Firma"

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>İşveren Portalı • UniBridge İstanbul Üniversitesi</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        {get_base_css()}
        .portal-hero {{
            background: linear-gradient(135deg, #14532d 0%, #15803d 60%, #16a34a 100%);
            color: white;
            border-radius: var(--radius-card);
            padding: 2.25rem 2.5rem;
            margin-bottom: 2.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
            box-shadow: 0 10px 25px rgba(22, 163, 74, 0.15);
        }}
    </style>
</head>
<body>
    {render_navbar(active_route="portal_recruiter", current_user=recruiter)}

    <main class="container">
        <!-- Hero Header -->
        <div class="portal-hero">
            <div>
                <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
                    <span class="badge badge-recruiter" style="background:rgba(255,255,255,0.25); color:white; border:none;">💼 KURUMSAL İŞVEREN</span>
                    <span style="font-size:0.85rem; color:#dcfce7;">{recruiter_comp}</span>
                </div>
                <h1 style="font-size:2rem; font-weight:800; margin:0 0 0.5rem;">Hoş Geldiniz, {recruiter_name}!</h1>
                <p style="color:rgba(255,255,255,0.9); margin:0; font-size:1rem;">İstanbul Üniversitesi Genç Yetenek İşe Alım & Staj Yönetim Portalı</p>
            </div>
            <div style="display:flex; gap:0.75rem;">
                <a href="/job-postings/" class="btn btn-primary" style="background:white; color:#15803d; font-weight:700;">➕ Yeni İlan Oluştur</a>
                <a href="/applications/" class="btn btn-secondary" style="background:rgba(255,255,255,0.15); color:white; border:1px solid rgba(255,255,255,0.3);">📋 Başvuruları İncele</a>
            </div>
        </div>

        <!-- Quick Stats -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Toplam İlanlar</div>
                <div class="stat-value">{len(posted_jobs)}</div>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.4rem;">Yayındaki açık kariyer pozisyonları</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Alınan Aday Başvuruları</div>
                <div class="stat-value">{len(applications)}</div>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.4rem;">İncelenmeyi bekleyen özgeçmişler</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Yetenek Havuzu (Öğrenci & Mezun)</div>
                <div class="stat-value">{len(talent_pool)}</div>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.4rem;">İletişime açık nitelikli adaylar</div>
            </div>
        </div>

        <!-- Actions Row -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1.5rem; margin-bottom:2.5rem;">
            <div class="card">
                <h3 style="font-size:1.2rem; color:var(--primary); margin-bottom:0.75rem;">🎯 İlan Yönetim Merkezi</h3>
                <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1.25rem;">Şirketinizin açık staj, yarı zamanlı veya tam zamanlı iş ilanlarını yönetin.</p>
                <a href="/job-postings/" class="btn btn-primary">İlanları Yönet →</a>
            </div>
            <div class="card">
                <h3 style="font-size:1.2rem; color:var(--primary); margin-bottom:0.75rem;">📋 Aday Başvuru Havuzu</h3>
                <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1.25rem;">Başvuruları onaylayın, inceleyin ve adaylara geri bildirim iletin.</p>
                <a href="/applications/" class="btn btn-secondary">Başvuruları Aç →</a>
            </div>
        </div>
    </main>

    {render_footer()}
</body>
</html>"""


def render_academic_portal(
    academic: Any,
    department_users: List[Any],
    announcements: List[Any]
) -> str:
    """Renders the dedicated Academic Faculty & Departmental Portal view"""
    academic_name = getattr(academic, "name", "Akademisyen")
    academic_dept = getattr(academic, "department", "Fakülte / Bölüm") or "Fakülte / Bölüm"

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Akademik Portal • UniBridge İstanbul Üniversitesi</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        {get_base_css()}
        .portal-hero {{
            background: linear-gradient(135deg, #4c1d95 0%, #6b21a8 60%, #7e22ce 100%);
            color: white;
            border-radius: var(--radius-card);
            padding: 2.25rem 2.5rem;
            margin-bottom: 2.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
            box-shadow: 0 10px 25px rgba(107, 33, 168, 0.15);
        }}
    </style>
</head>
<body>
    {render_navbar(active_route="portal_academic", current_user=academic)}

    <main class="container">
        <!-- Hero Header -->
        <div class="portal-hero">
            <div>
                <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
                    <span class="badge badge-academic" style="background:rgba(255,255,255,0.25); color:white; border:none;">🏛️ AKADEMİK PERSONEL</span>
                    <span style="font-size:0.85rem; color:#f3e8ff;">{academic_dept}</span>
                </div>
                <h1 style="font-size:2rem; font-weight:800; margin:0 0 0.5rem;">Sayın {academic_name}, Hoş Geldiniz!</h1>
                <p style="color:rgba(255,255,255,0.9); margin:0; font-size:1rem;">İstanbul Üniversitesi Akademik Yönetim ve Bölüm Bilgi Portalı</p>
            </div>
            <div style="display:flex; gap:0.75rem;">
                <a href="/announcements/" class="btn btn-primary" style="background:white; color:#6b21a8; font-weight:700;">📢 Duyuru Yayınla</a>
                <a href="/users/" class="btn btn-secondary" style="background:rgba(255,255,255,0.15); color:white; border:1px solid rgba(255,255,255,0.3);">👥 Öğrenci Listesi</a>
            </div>
        </div>

        <!-- Quick Stats -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Bölüm Öğrenci & Mezunları</div>
                <div class="stat-value">{len(department_users)}</div>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.4rem;">Kayıtlı bölüm öğrencileri ve mezunları</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Yayınlanmış Duyurular</div>
                <div class="stat-value">{len(announcements)}</div>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.4rem;">Aktif akademik duyuru ve bültenler</div>
            </div>
        </div>

        <!-- Section: Actions -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1.5rem; margin-bottom:2.5rem;">
            <div class="card">
                <h3 style="font-size:1.2rem; color:var(--primary); margin-bottom:0.75rem;">📢 Bölüm Duyurusu Yayınla</h3>
                <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1.25rem;">Sınav tarihleri, staj yönergeleri ve akademik etkinlikleri duyurun.</p>
                <a href="/announcements/" class="btn btn-primary">Duyurulara Git →</a>
            </div>
            <div class="card">
                <h3 style="font-size:1.2rem; color:var(--primary); margin-bottom:0.75rem;">👥 Öğrenci & Mezun Rehberi</h3>
                <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1.25rem;">Bölümünüzdeki aktif öğrencileri ve mezun kariyer yollarını inceleyin.</p>
                <a href="/users/" class="btn btn-secondary">Rehberi Aç →</a>
            </div>
        </div>
    </main>

    {render_footer()}
</body>
</html>"""
