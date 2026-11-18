# 🎨 Brand Identity & Style Guidelines (brand.md)

> **Alumni & Career Portal (Alumni OS)**  
> *Bridging Academic Excellence with Professional Opportunity.*

---

## 1. Brand Mission & Story

**Alumni OS** is the official career and academic networking platform designed for the Department of Management Information Systems. It empowers students, alumni, faculty members, and corporate recruiters to interact within a unified, high-performance ecosystem. 

Whether announcing university milestones, discovering internships, managing applications, or evaluating talent, Alumni OS delivers a seamless experience guided by clarity, speed, and modern aesthetics.

---

## 2. Brand Tone of Voice & Personality

The brand embodies four core personality pillars:

| Pillar | Description | Execution in UI & Copy |
| :--- | :--- | :--- |
| **Academic yet Modern** | Grounded in university credibility while adopting cutting-edge engineering standards. | Clean typography, authoritative yet welcoming copy, zero unnecessary jargon. |
| **Trustworthy & Transparent** | Emphasizes data integrity, persistence, and auditability. | Explicit status badges, readable timestamps, clear error reasoning. |
| **Developer-First & High Performance** | Celebrates clean RESTful MVC architecture and containerized robustness. | Monospace indicators for routes and IDs, instant responses, responsive feedback. |
| **Empowering & Action-Oriented** | Focuses on moving candidate workflows and opportunities forward. | Clear call-to-action buttons, intuitive navigation, high-contrast interactive states. |

---

## 3. Brand Color Palette & Semantic Tokens

Our color tokens utilize an accessible dark-mode first scheme inspired by modern developer ecosystems (Linear, Stripe, Vercel).

```
  Primary Indigo      Royal Violet        Neon Cyan           Deep Obsidian
     #6366F1             #8B5CF6             #06B6D4             #090D16
  [   Brand   ]       [   Accent  ]       [ Highlight ]       [ Background]
```

### Palette Specification:

| Token Name | Hex Code | RGB | Purpose & Usage |
| :--- | :--- | :--- | :--- |
| `--bg-base` | `#090D16` | `rgb(9, 13, 22)` | Deep space obsidian, canvas background |
| `--bg-surface` | `#0F172A` | `rgb(15, 23, 42)` | Glassmorphic card bodies, panels, table containers |
| `--bg-surface-elevated`| `#1E293B` | `rgb(30, 41, 59)` | Modals, active states, hovered cards |
| `--primary` | `#6366F1` | `rgb(99, 102, 241)` | Electric Indigo, main primary brand color |
| `--primary-gradient` | `linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #06B6D4 100%)` | Brand badges, hero titles, primary buttons |
| `--secondary` | `#06B6D4` | `rgb(6, 182, 212)` | Electric Cyan, secondary highlights & links |
| `--accent` | `#38BDF8` | `rgb(56, 189, 248)` | Sky blue accent for badges and active route indicators |
| `--text-main` | `#F8FAFC` | `rgb(248, 250, 252)` | Crisp white for headings and high-priority labels |
| `--text-muted` | `#94A3B8` | `rgb(148, 163, 184)` | Slate for secondary text, descriptions, table headers |
| `--border-glass` | `rgba(255, 255, 255, 0.08)` | Glassmorphism 1px boundary border |
| `--border-glow` | `rgba(99, 102, 241, 0.45)` | Glowing focus outline and active card highlight |
| `--success` | `#10B981` | `rgb(16, 185, 129)` | Accepted status, healthy indicators |
| `--warning` | `#F59E0B` | `rgb(245, 158, 11)` | Pending review, cautionary states |
| `--danger` | `#F43F5E` | `rgb(244, 63, 94)` | Rejected status, delete buttons, 404 alert |

---

## 4. Typography Hierarchy

We prioritize clean readability, high contrast, and proportional optical sizing:

* **Primary Sans-Serif:** `'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
* **Code / Technical Monospace:** `'JetBrains Mono', 'Fira Code', Menlo, Consolas, monospace`

### Scale:
* **Display / Hero H1:** `2.5rem – 3.25rem` (800 ExtraBold, letter-spacing: `-0.03em`)
* **Section Title H2:** `1.5rem – 1.85rem` (700 Bold, letter-spacing: `-0.02em`)
* **Card Title H3:** `1.15rem – 1.25rem` (600 SemiBold)
* **Body Text:** `0.95rem – 1.05rem` (400 Regular / 500 Medium, line-height: `1.6`)
* **Captions & Metadata:** `0.75rem – 0.85rem` (500 Medium / 600 SemiBold uppercase)

---

## 5. Visual Identity: Logo & Badges

### The Logo Mark:
* Textual Logotype: **ALUMNI**
* Styling: Displayed inside a gradient rounded container (`border-radius: 10px`, `background: var(--primary-gradient)`), coupled with crisp bold white lettering and a subtle outer glow: `box-shadow: 0 4px 20px rgba(99, 102, 241, 0.35)`.
* Sub-tag: `Career & Academic Ecosystem` in muted uppercase.

---

## 6. Micro-Interactions & Motion

* **Card Elevation:** Hovered cards lift smoothly (`transform: translateY(-4px);`) with transition `0.2s cubic-bezier(0.16, 1, 0.3, 1)`.
* **Focus States:** Inputs illuminate with an indigo glow ring: `box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25)`.
* **Button Feedback:** Active buttons scale slightly (`transform: scale(0.98);`) providing tactile visual confirmation.

---

> 🔗 **Related System Documents:**
> * Design System Specifications: **[DESIGN.md](./DESIGN.md)**
> * Data Architecture & Domain Model: **[ddd.md](./ddd.md)**
> * Project Overview & Quickstart: **[README.md](./README.md)**
