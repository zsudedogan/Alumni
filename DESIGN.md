# 📐 Design System Specification (DESIGN.md)

> Conforming to the **[VoltAgent/design-md](https://github.com/VoltAgent/design-md)** framework standard for AI agents and developer-driven UI consistency.

---

## 1. System Foundations & Aesthetic Principles

This design system establishes strict visual tokens, layout contracts, component behaviors, and micro-interactions across every page of the Alumni web application.

* **Reference Standard:** [VoltAgent/design-md](https://github.com/VoltAgent/design-md)
* **Aesthetic Category:** Modern Developer-First Dark Theme with Glassmorphic Elements (Linear / Vercel style).
* **Target Audience:** University students, alumni, faculty, and corporate talent recruiters.
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
* **Desktop (> 1024px):** Max container width `1140px`, 3-column feature grids, floating sticky navigation.

---

## 3. Unified Navigation Bar (`.navbar`)

Every page in the application MUST include the identical, sticky glassmorphic navigation bar ensuring instant zero-latency routing across modules:

```html
<nav class="navbar">
  <div class="nav-container">
    <a href="/" class="brand">
      <span class="brand-badge">ALUMNI</span>
      <span class="brand-title">Ecosystem</span>
    </a>
    <div class="nav-links">
      <a href="/users/" class="nav-link {active}">👥 Users</a>
      <a href="/announcements/" class="nav-link {active}">📢 Notices</a>
      <a href="/job-postings/" class="nav-link {active}">💼 Careers</a>
      <a href="/applications/" class="nav-link {active}">📝 Applications</a>
      <a href="/api/swagger" class="nav-link btn-swagger" target="_blank">📖 Swagger</a>
    </div>
  </div>
</nav>
```

---

## 4. Component Primitives & Styling Contracts

### 4.1. Glassmorphic Card Container (`.card`)
* Background: `rgba(15, 23, 42, 0.75)`
* Border: `1px solid rgba(255, 255, 255, 0.08)`
* Backdrop Filter: `blur(16px)`
* Border Radius: `16px`
* Shadow: `0 10px 25px -5px rgba(0, 0, 0, 0.5)`
* Hover Effect: `transform: translateY(-4px); border-color: rgba(99, 102, 241, 0.4);`

### 4.2. Buttons (`.btn`)
* **Primary (`.btn-primary`):** Background `linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)`, color white, bold font, subtle drop-shadow `0 4px 14px rgba(99, 102, 241, 0.35)`.
* **Secondary (`.btn-secondary`):** Background `rgba(255, 255, 255, 0.06)`, border `1px solid rgba(255, 255, 255, 0.12)`, color `#f8fafc`.
* **Danger (`.btn-danger`):** Background `rgba(244, 63, 94, 0.15)`, border `1px solid rgba(244, 63, 94, 0.3)`, color `#f43f5e`.
* **Small (`.btn-sm`):** Padding `0.35rem 0.75rem`, font-size `0.8rem`, border-radius `6px`.

### 4.3. Stat Widgets (`.stat-card`)
Stat cards highlight key operational metrics:
* Structure: Top micro-label (`.stat-label`), large bold numeric value (`.stat-value`), bottom context pill (`.stat-badge`).
* Metric highlights:
  * Total counts: Indigo highlight
  * Active listings: Emerald highlight
  * Pending reviews: Amber highlight

### 4.4. Status Badges & Pills (`.badge`)
* Common styling: `display: inline-flex; align-items: center; padding: 0.25rem 0.65rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;`
* **Pending:** Background `rgba(245, 158, 11, 0.15)`, color `#f59e0b`.
* **Reviewed:** Background `rgba(56, 189, 248, 0.15)`, color `#38bdf8`.
* **Shortlisted / Accepted:** Background `rgba(16, 185, 129, 0.15)`, color `#10b981`.
* **Rejected:** Background `rgba(244, 63, 94, 0.15)`, color `#f43f5e`.
* **Full-Time / Internship:** Background `rgba(99, 102, 241, 0.15)`, color `#818cf8`.

### 4.5. Data Tables (`.data-table`)
* Container: Rounded corners (`border-radius: 12px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.08);`).
* Headers: Uppercase muted font, sticky background `rgba(30, 41, 59, 0.95)`, bottom border.
* Row States: Zebra subtle background, hover highlight `rgba(99, 102, 241, 0.08)`.

### 4.6. Form Controls
* Inputs, Textareas, Selects:
  * Background: `rgba(15, 23, 42, 0.8)`
  * Border: `1px solid rgba(255, 255, 255, 0.12)`
  * Focus State: Border color `#6366f1`, glow: `box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25); outline: none;`
  * Text: Color `#f8fafc`, font size `0.95rem`

---

## 5. Page-by-Page Implementation Guide

1. **Hub / Landing (`/` in `main.py`):**
   - Brand hero headline with gradient text.
   - 4-card interactive feature grid linking to all management interfaces.
   - Live architectural stat badges (MVC, SQLite/PostgreSQL, Middleware Pipeline, Pytest 21/21).

2. **User Management (`/users/` in `views/user_view.py`):**
   - Stat overview: Total registered users, candidate counts.
   - Interactive data table with avatar initial badges, email pills, and action buttons.
   - Smooth inline creation card and modal editor.

3. **Announcements Feed (`/announcements/` in `views/announcement_view.py`):**
   - Feed cards with author tags, category badges (Academic, Career, Event, Urgent).
   - Instant search and category filter pills.
   - Inline creation form and delete buttons.

4. **Career & Job Postings (`/job-postings/` in `views/job_posting_view.py`):**
   - Career banner with metric counters (Active, Internships, Full-time).
   - Filter pills (All, Remote, Full-time, Internship).
   - Opportunity cards displaying `title` (enforced max 120), `company`, `city`/location, salary chip, deadline.
   - "Apply Now" button directly deep-linking to `/applications/?job_id=X#apply-form`.

5. **Job Applications Portal (`/applications/` in `views/application_view.py`):**
   - Stat widgets for candidate application pipeline (Pending, Reviewed, Accepted, Rejected).
   - Filterable candidate review cards with dynamic status update dropdown calling `PATCH /api/applications/{id}` via AJAX.
   - Pre-populated submission form linking candidates to postings.

6. **Error Guardians (`middlewares/handlers.py`):**
   - 404 Guardian page displaying reason, path, and recovery buttons.
   - 500 Guardian page with incident tracking notice.

---

> 🔗 **Related System Documents:**
> * Brand Strategy & Tokens: **[brand.md](./brand.md)**
> * Data Architecture: **[ddd.md](./ddd.md)**
> * Root Documentation: **[README.md](./README.md)**
