# 🎨 Brand Identity & Style Guidelines (brand.md)

> **UniBridge Giriş Sistemi • İstanbul Üniversitesi**  
> *Bridging Academic Excellence with Professional Opportunity.*

---

## 1. Brand Mission & Story

**UniBridge (İstanbul Üniversitesi)** is the official career and academic portal designed for students, alumni, faculty members, and corporate recruiters to interact within a unified, high-performance ecosystem.

Whether announcing university milestones, discovering internships, managing applications, or onboarding new talent across departments, UniBridge delivers an authoritative, modern, and accessible experience rooted in Istanbul University's historic heritage (1453).

---

## 2. Brand Tone of Voice & Personality

The brand embodies four core personality pillars:

| Pillar | Description | Execution in UI & Copy |
| :--- | :--- | :--- |
| **Academic Credibility & Heritage** | Grounded in Istanbul University's historic excellence (1453). | Official circular emblem seal, deep forest green and gold hues, dignified tone. |
| **Trustworthy & Transparent** | Emphasizes data integrity, persistence, and auditability. | Explicit role badges, readable timestamps, clear error reasoning. |
| **Developer-First & High Performance** | Celebrates clean RESTful MVC architecture and containerized robustness. | Monospace indicators for routes and IDs, instant responses, responsive feedback. |
| **Empowering & Action-Oriented** | Focuses on moving candidate workflows and opportunities forward. | Clear call-to-action buttons, intuitive navigation, high-contrast interactive states. |

---

## 3. Brand Color Palette & Semantic Tokens (UniBridge Standard)

Our color tokens utilize an accessible light aesthetic matching the official Istanbul University UniBridge portal:

```
  IU Forest Green      Warm Gold           Light Sage Base       Crisp White
     #204729             #C59B27             #F4F7F5             #FFFFFF
  [   Primary   ]     [   Accent  ]       [ Canvas Base ]     [ Card Surface]
```

### Palette Specification:

| Token Name | Hex Code | RGB | Purpose & Usage |
| :--- | :--- | :--- | :--- |
| `--bg-base` | `#F4F7F5` | `rgb(244, 247, 245)` | Soft airy light sage, canvas background |
| `--bg-surface` | `#FFFFFF` | `rgb(255, 255, 255)` | Pure white card bodies, panels, table containers |
| `--primary` | `#204729` | `rgb(32, 71, 41)` | Istanbul University Forest Green, primary brand color |
| `--primary-dark` | `#17351E` | `rgb(23, 53, 30)` | Hover state for buttons and active navigations |
| `--accent` / `--accent-gold` | `#C59B27` | `rgb(197, 155, 39)` | University Warm Gold, seal detailing and link accents |
| `--text-main` | `#152418` | `rgb(21, 36, 24)` | Deep forest charcoal for high-contrast headings & labels |
| `--text-muted` | `#5E6D62` | `rgb(94, 109, 98)` | Medium slate for secondary text, descriptions, table headers |
| `--border-card` | `rgba(0, 0, 0, 0.06)` | `rgba(0, 0, 0, 0.06)` | Clean 1px boundary border for cards |
| `--border-glow` | `rgba(32, 71, 41, 0.25)` | `rgba(32, 71, 41, 0.25)` | Focus outline and active card highlight |
| `--success` | `#15803D` | `rgb(21, 128, 61)` | Accepted status, healthy indicators |
| `--warning` | `#D97706` | `rgb(217, 119, 6)` | Pending review, cautionary states |
| `--danger` | `#DC2626` | `rgb(220, 38, 38)` | Rejected status, delete buttons, 404 alert |

### Role Pastel Badges:
- **Öğrenci (Student)**: `#E8F3FC` background with `#1D4ED8` icon (graduation cap 🎓)
- **Mezun (Alumni)**: `#FEF6E7` background with `#C59B27` icon (medal / ribbon 🎖️)
- **Akademik (Academic)**: `#EDE9FE` background with `#6B21A8` icon (screen / faculty 🖥️)
- **İşveren / İK (Recruiter)**: `#E6F4EA` background with `#15803D` icon (briefcase 🏢)

---

## 4. Typography Hierarchy

- **Primary Font Family:** `Plus Jakarta Sans`, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif.
- **Code & Identifier Font:** `JetBrains Mono`, 'Fira Code', monospace.

| Scale Level | Weight | Size | Usage |
| :--- | :--- | :--- | :--- |
| **Hero Title (H1)** | 800 (ExtraBold) | 2.25rem - 2.5rem | UniBridge Portal Entrance, Page Titles |
| **Section Header (H2/H3)**| 800 (ExtraBold) | 1.25rem - 1.4rem | Role card titles, Module titles |
| **Card Header (H4)** | 700 (Bold) | 1.1rem | Quick access cards, modal titles |
| **Body Text** | 400 - 500 | 0.95rem - 1.05rem | Descriptions, notice contents, job overviews |
| **Labels & Badges** | 700 (Bold) | 0.75rem - 0.85rem | Status pills, role tags, form labels |

---

## 5. Logo & Seals

1. **Circular Official Seal (`render_iu_logo`):**
   High-fidelity SVG depicting T.C. İstanbul Üniversitesi with golden borders, "★ 1453 ★", and central university historic gate/tree motif.
2. **Top Navigation Logotype:**
   Includes the seal alongside "UniBridge" in forest green with "İstanbul Üniversitesi" in warm gold uppercase.

---

## 6. Official Footer

- `© 2025 İSTANBUL ÜNİVERSİTESİ BİLGİ İŞLEM SİSTEMİ`
- Standard Gold Navigation Links: `Yardım Merkezi` `Kullanım Koşulları` `Brand Guidelines` `Design System` `Sistem Durumu`.
