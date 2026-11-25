# 📐 Design System Specification (DESIGN.md)

> Conforming to the **[VoltAgent/design-md](https://github.com/VoltAgent/design-md)** framework standard for AI agents and developer-driven UI consistency.

---

## 1. System Foundations & Aesthetic Principles

This design system establishes strict visual tokens, layout contracts, component behaviors, and micro-interactions across every page of the UniBridge (İstanbul Üniversitesi) web application.

* **Reference Standard:** [VoltAgent/design-md](https://github.com/VoltAgent/design-md)
* **Aesthetic Category:** Official Academic & Career Portal (UniBridge Standard) with Istanbul University Forest Green (`#204729`), University Warm Gold (`#C59B27`), Soft Sage Canvas (`#F4F7F5`), and Pure White Cards.
* **Target Audience:** University students, alumni, faculty members, and corporate talent recruiters.
* **Accessibility Target:** WCAG 2.1 AA (contrast ratio $\ge 4.5:1$ for normal text, keyboard navigable).

---

## 2. Layout & Spatial System

### 2.1. Spatial Grid
All margins, paddings, and gap distances follow an 8-point spatial grid:
* `4px`: Micro spacing (pill padding, border thickness)
* `8px`: Small spacing (button icon gaps, badge padding)
* `12px`: Form input internal padding
* `16px`: Standard card padding, grid gaps
* `24px`: Section gaps, modal padding
* `32px`: Hero vertical spacing
* `48px`: Page header margin

### 2.2. Responsive Breakpoints
* **Mobile (< 640px):** Single-column stack, full-width buttons, scrollable table wrappers.
* **Tablet (640px - 1024px):** 2-column card grids, condensed navigation.
* **Desktop (> 1024px):** Max container width `1180px`, role card stack, floating sticky navigation.

---

## 3. Unified Navigation Bar (`.navbar`)

Every page in the application includes the sticky navigation bar featuring the official Istanbul University seal and UniBridge brand identity:

```html
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
      <a href="/users/" class="nav-link {active}">👥 Users</a>
      <a href="/announcements/" class="nav-link {active}">📢 Notices</a>
      <a href="/job-postings/" class="nav-link {active}">💼 Careers</a>
      <a href="/applications/" class="nav-link {active}">📝 Applications</a>
      <a href="/register/" class="nav-link {active}">✨ Register</a>
      <a href="/api/swagger" class="nav-link btn-swagger" target="_blank">📖 Swagger</a>
    </div>
  </div>
</nav>
```

---

## 4. Component Primitives & Styling Contracts

### 4.1. Clean Card Container (`.card`)
* Background: `#ffffff`
* Border: `1px solid rgba(0, 0, 0, 0.06)`
* Border Radius: `20px`
* Shadow: `0 10px 30px rgba(0, 0, 0, 0.04)`
* Hover Effect: `transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0, 0, 0, 0.06);`

### 4.2. Buttons (`.btn`)
* **Primary (`.btn-primary`, `.btn-unibridge`):** Background `#204729` (Istanbul University Forest Green), color white, bold font, drop-shadow `0 4px 12px rgba(32, 71, 41, 0.18)`.
* **Secondary (`.btn-secondary`):** Background `#ffffff`, border `1px solid rgba(0, 0, 0, 0.12)`, color `#152418`.
* **Danger (`.btn-danger`):** Background `rgba(220, 38, 38, 0.1)`, border `1px solid rgba(220, 38, 38, 0.25)`, color `#b91c1c`.
* **Small (`.btn-sm`):** Padding `0.4rem 0.85rem`, font-size `0.82rem`, border-radius `8px`.

### 4.3. Stat Widgets (`.stat-card`)
Stat cards highlight key operational metrics:
* Structure: Top micro-label (`.stat-label`), large bold numeric value (`.stat-value`).
* Accent Colors:
  * Total counts: Forest Green (`#204729`)
  * Role counts: University Warm Gold (`#C59B27`)
  * Database Engine: Primary Green (`#204729`)

### 4.4. Status Badges & Pills (`.badge`)
* Common styling: `display: inline-flex; align-items: center; padding: 0.28rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700;`
* **Student:** Background `#e8f3fc`, color `#1d4ed8`, border `rgba(29, 78, 216, 0.25)`.
* **Alumni:** Background `#fef6e7`, color `#b45309`, border `rgba(180, 83, 9, 0.25)`.
* **Recruiter:** Background `#e6f4ea`, color `#15803d`, border `rgba(21, 128, 61, 0.25)`.
* **Academic:** Background `#ede9fe`, color `#6b21a8`, border `rgba(107, 33, 168, 0.25)`.
* **Pending:** Background `#fef3c7`, color `#b45309`.
* **Reviewed:** Background `#e0f2fe`, color `#0369a1`.
* **Accepted:** Background `#dcfce7`, color `#15803d`.
* **Rejected:** Background `#fee2e2`, color `#b91c1c`.

### 4.5. Data Tables (`.data-table`)
* Container: Rounded corners (`border-radius: 14px; overflow: hidden; border: 1px solid rgba(0, 0, 0, 0.07); background: #ffffff;`).
* Headers: Uppercase muted font, background `#f7faf8`, bottom border.
* Row States: Crisp white, hover highlight `rgba(32, 71, 41, 0.03)`.

### 4.6. Form Controls
* Inputs, Textareas, Selects:
  * Background: `#ffffff`
  * Border: `1px solid rgba(0, 0, 0, 0.14)`
  * Focus State: Border color `#204729`, glow: `box-shadow: 0 0 0 3px rgba(32, 71, 41, 0.12); outline: none;`
  * Text: Color `#152418`, font size `0.95rem`

---

## 5. Page-by-Page Implementation Guide

1. **Hub / Entrance Portal (`/` in `main.py`):**
   - Official T.C. İstanbul Üniversitesi circular seal (1453).
   - UniBridge Giriş Sistemi header and subtitle ("Lütfen devam etmek için kullanıcı tipinizi seçin").
   - 4 prominent role entry cards: Öğrenci, Mezun, Akademik, İşveren.
   - Quick Access module grid (Users, Notices, Careers, Applications, Swagger UI).

2. **User Management (`/users/` in `views/user_view.py`):**
   - Stat overview: Total registered users, roles supported, SQLAlchemy database.
   - Interactive data table with avatar initials, role pills, email text, and edit/delete actions.

3. **Announcements Feed (`/announcements/` in `views/announcement_view.py`):**
   - Feed cards with author tags, category badges (Academic, Career, Event, Urgent).
   - Category filter pills with active green highlight.

4. **Career & Job Postings (`/job-postings/` in `views/job_posting_view.py`):**
   - Career cards with company initial badges, 120-char validated title, location, requirements box.
   - Direct "Apply Now" button linking to `/applications/?job_id=X#apply-form`.

5. **Job Applications Portal (`/applications/` in `views/application_view.py`):**
   - Recruitment pipeline stat counters.
   - Candidate review cards with live status dropdown calling `PATCH /api/applications/{id}` via AJAX.

6. **Error Guardians (`middlewares/handlers.py`):**
   - Clean 404 Guardian page displaying reason and UniBridge return buttons.
   - 500 Guardian page with incident tracking notice.

---

> 🔗 **Related System Documents:**
> * Brand Strategy & Tokens: **[brand.md](./brand.md)**
> * Data Architecture: **[ddd.md](./ddd.md)**
> * Root Documentation: **[README.md](./README.md)**
