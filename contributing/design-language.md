# Reusable editorial interface prompt

Use this prompt to reproduce the visual language of the GDAC v2.0 reading
experience for another serious technical, governance, research, or standards
publication. Replace the bracketed content brief; preserve the design rules.

```text
Act as a senior editorial designer and front-end engineer. Design and implement
a high-trust reading interface for [PRODUCT / STANDARD / RESEARCH BRIEF]. The
audience is [AUDIENCE]. The page should feel like a carefully edited technical
manual or independent journal, not a SaaS landing-page template and not an
AI-generated dashboard.

Editorial direction
- Lead with one plain-language proposition. A reader should understand what the
  work is, when to use it, and what it changes within 30 seconds.
- Use natural, concise language. Keep technical terms only when they control a
  real object, decision, state, permission, or evidence requirement.
- Put the practical mechanism before caveats. State limits once, near the claim
  they qualify; do not fill every section with defensive disclaimers.
- Use tables for exact mappings, ordered lists for actual sequences, and small
  diagrams only when they explain a real architecture or state transition.
- Do not add decorative images, abstract node art, fake charts, arbitrary
  metrics, testimonials, gradients, glass effects, or empty cards.

Visual language
- Warm paper background: #f5f4f0. Main ink: #14130f. Body ink: #26241d.
  Secondary ink: #3a382f. Rules: #dcd8d0 and #cdc8bd.
- One restrained brown accent: #8f4f1d. Reserve it for limits, active states,
  focus, evidence boundaries, and important semantic markers. Never scatter it
  as decoration. Do not substitute generic AI green, neon blue, or alert red.
- Serif display type for titles and major section headings; neutral sans serif
  for body text; monospace only for actual fields, statuses, IDs, commands, or
  metadata. Use system fonts and no third-party font request.
- Thin rules, square corners, generous but purposeful whitespace. No shadows,
  pill-heavy interfaces, floating glass panels, or rounded-card grids.
- Establish a strict shared content baseline. Do not leave an unexplained empty
  column. Keep reading width around 60-70 characters and use a 12-column or
  equivalent editorial grid.
- Visual variance: 4/10. Motion: 2/10. Information density: 6/10.

Page architecture
1. Quiet sticky masthead with one brand and a consistent six-item navigation.
2. Hero with one status eyebrow, one concrete title, one short proposition, at
   most two actions, and one semantic system model if it materially helps.
3. A concise contents disclosure after the hero for long pages.
4. Sections ordered as: purpose and adoption trigger; system or method; one
   end-to-end example; exact rules or mappings; tools or implementation;
   boundaries and provenance.
5. Subpages use one natural-language eyebrow, title, summary, and compact
   contents. Remove three-line metadata rails, repeated decorative section
   numbers, and duplicated status notices.
6. Developer commands belong inside a native collapsed details section, not in
   the main narrative. Source Markdown or JSON is secondary, clearly labelled
   as source or download rather than presented as the public reading page.

Interaction and accessibility
- Static HTML and CSS first. Use native details/summary for disclosures. No
  JavaScript unless a real interaction cannot be expressed accessibly without
  it.
- Preserve semantic heading order, table captions, th scope, skip link,
  visible keyboard focus, reduced-motion support, and WCAG AA contrast.
- All navigation and disclosure targets should be at least 44px high on mobile.
- Long tables scroll inside a labelled region on small screens, show a visible
  horizontal-swipe hint, and keep the first column readable when practical.
- Avoid page-level horizontal overflow at 1440px, 1024px, and 390px. At 390px,
  the proposition and first action should appear before the page becomes a long
  technical document.
- Print CSS expands disclosure content, wraps code safely, removes navigation,
  and prevents important table rows or records from splitting badly.

Implementation constraints
- Reuse the existing architecture and semantic markup. Make the smallest
  coherent change; do not introduce a framework or speculative design system.
- Centralize color, type, spacing, measure, and grid as CSS custom properties.
- Create responsive behavior from layout rules before adding breakpoints.
- Before delivery, inspect every page at 1440px, 1024px, and 390px; test
  keyboard navigation, disclosures, anchor links, table scrolling, print, and
  reduced motion. Remove any component that looks polished but carries no
  information.

Deliver production-ready files and a short rationale that names the content
hierarchy, design tokens, interaction rules, and any deliberate limitations.
```
