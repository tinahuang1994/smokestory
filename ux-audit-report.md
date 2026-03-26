# SmokeStory — UX/UI Audit Report
**Date:** March 20, 2026
**Auditor:** Senior UX/UI Design Review
**File audited:** `frontend/index.html` (v1.0.1)
**Audience:** Editorial product for journalists, researchers, and affected communities

---

## Executive Summary

SmokeStory has genuine editorial ambition. The typographic pairing, amber accent, grain texture, and glassmorphism panels create a premium dark-theme aesthetic that positions this well above a standard data dashboard. The core mechanics — date selection, county click, narrative generation — work logically.

However, several critical issues block the product from being usable by its stated non-technical audience: mobile is effectively broken, contrast ratios fail WCAG AA at multiple points, the map provides no hover feedback before clicking, and error messages surface raw HTTP codes to readers who don't know what they mean.

**Overall score: 6.5 / 10.** Excellent aesthetic foundation, incomplete execution for the target audience.

---

## 1. ONBOARDING & FIRST IMPRESSION

### Issue 1.1 — Default date is not today, with no explanation
**Severity: Critical**

The date picker initializes to `2025-01-09` (Palisades Fire day). A first-time visitor sees data from months ago with no explanation of why. The hint text below the date input — *"Select any date since 2005 to explore historical smoke events"* — is 0.6rem, monospace, faint gray (`--text-muted`), and is barely legible. Most users will not read it.

**Recommendation:** Default to today's date. If today has no data, fall back to the most recent available date and show a prominent notice: *"Showing most recent available data: January 9, 2025"*. If you intentionally want to default to Palisades, put an amber banner in the welcome panel: *"Loaded: Palisades & Eaton Fires — Jan 9, 2025."* The user deserves to know why the map looks the way it does.

**Effort: Small** — change the `defaultDate` in flatpickr init and add a conditional notice in the welcome panel.

---

### Issue 1.2 — No primary CTA; the welcome panel reads as passive editorial
**Severity: Important**

The welcome panel has good copy — "What is this" and "How to explore" — but no button or strong visual affordance to begin. The experience is: user reads steps, looks at the map, doesn't know what to do first because the onboarding tooltip hasn't fired yet. There is no first action to take *inside the panel itself*.

**Recommendation:** Add a single high-contrast CTA below the steps — a large amber `EXPLORE THE MAP →` button or an arrow nudge pointing left toward the map. Alternatively, make the "Most Affected Today" county rows more obviously clickable with a `→ Read story` affordance on each row rather than just a left-border hover. The top stories list is the most actionable element on the welcome screen; it should feel like links, not data rows.

**Effort: Small**

---

### Issue 1.3 — Welcome panel wordmark is duplicate
**Severity: Nice to have**

"Smoke Story" appears in both the fixed header (amber, 1rem, tracked) and as the large welcome panel wordmark (amber, 2.8rem serif). This redundancy reduces the wordmark's impact and makes the page feel unfinished.

**Recommendation:** Replace the welcome panel wordmark with a large ambient tagline — e.g., *"Every county. Every fire. Every day."* — or a hero data statement like *"58 counties. 20 years of smoke."* This frees the serif for editorial use while letting the header logo own the brand.

**Effort: Small**

---

## 2. MAP INTERACTION

### Issue 2.1 — No hover tooltip shows county name before clicking
**Severity: Critical**

The hover state changes the county border from 0.6px dark to 1.5px amber — this IS visible, but the user cannot see the county name on hover. On a California map, many inland counties are unfamiliar to non-Californians. The user has no way to know what they're about to click without clicking it.

**Recommendation:** Add a Leaflet tooltip on `mouseover` that shows `{county_name} County` and the PM2.5 value (e.g., `42.3 µg/m³ · Unhealthy for Sensitive Groups`). Use `lyr.bindTooltip(...)` with `{permanent: false, direction: 'top'}` and style it with the existing dark glass aesthetic. This single change dramatically reduces friction for exploration.

**Effort: Small**

---

### Issue 2.2 — Onboarding tip disappears after 5 seconds, only fires once
**Severity: Important**

The "👆 Click any county to read its smoke story" tooltip appears after map load, pulsing in amber, but auto-dismisses after 5 seconds. If the user is watching the map load or reading the welcome panel, they'll miss it entirely. It also only fires once per session, so a confused user has no way to see it again.

**Recommendation:** Extend the tip to 10–12 seconds. Add a subtle persistent "hint" state (non-pulsing, lower opacity) that stays until the first county click. Consider also adding a micro-animation on the map itself — a ripple effect on the highest-severity county on load — to draw the eye and communicate clickability.

**Effort: Small**

---

### Issue 2.3 — No cursor feedback on county polygons
**Severity: Important**

Leaflet doesn't automatically set `cursor: pointer` on GeoJSON layers with click handlers. Most browsers will default to the standard cursor over map tiles. Users may not realize counties are interactive.

**Recommendation:** Add `cursor: 'pointer'` to the Leaflet style object, or use CSS: `.leaflet-interactive { cursor: pointer; }`. This is a standard Leaflet pattern and the fix is one line.

**Effort: Small** (one CSS rule)

---

### Issue 2.4 — Smoke and PM2.5 layers use nearly identical colors, creating visual noise
**Severity: Important**

The PM2.5 county fill uses `#f97316` (amber-orange), and the smoke plumes use `fillColor: '#f97316'` with a stroke of `#fb923c`. These two layers are visually indistinguishable except for opacity and shape type. When both are active, the map looks uniformly orange with no clear signal about which is which.

**Recommendation:** Differentiate smoke plumes clearly from PM2.5 county fills. Options: (a) use a different hue for smoke — a desaturated steel-blue or gray (`#64748b`) better represents atmospheric haze vs. ground-level air quality; (b) use a hatched/striped fill pattern for smoke polygons; (c) give smoke a yellow-white tint. The three layers should have three distinct visual languages.

**Effort: Medium** — requires design decision + updating smoke polygon style + updating the layer legend dot.

---

## 3. SIDE PANEL

### Issue 3.1 — "Generate Story" requires a second click after county selection
**Severity: Important**

The flow after clicking a county is: (1) panel opens with PM2.5 card, (2) user must manually click "Generate Story" to see the narrative. This two-step flow adds friction. For a journalism product where storytelling is the core value, the story should be the first thing the user sees, not something they have to request.

**Recommendation:** Auto-trigger narrative generation immediately on county click. Remove the explicit "Generate Story" button. Show a loading state in-panel as soon as the county opens. If API cost is a concern, consider auto-generating only for counties with data (`pm25_mean != null`). Add a regenerate/refresh icon for subsequent requests.

**Effort: Medium** — requires removing the button, moving `generateStory()` to be called inside `openPanel()`, and ensuring the loading state is immediate and visible.

---

### Issue 3.2 — "USG*" label is cryptic
**Severity: Important**

In the PM2.5 card, the `pm25Label()` function returns `'USG*'` for the "Unhealthy for Sensitive Groups" category. This abbreviation is not defined anywhere visible in the panel at point of use. The asterisk implies a footnote that doesn't exist inline.

**Recommendation:** Use the full label "Unhealthy for Sensitive Groups" or a shorter but self-explanatory form: "Sensitive Groups." If screen space requires abbreviation, add a tooltip on the severity text itself explaining who "sensitive groups" means. The legend footnote exists at panel bottom but is not linked to the card.

**Effort: Small**

---

### Issue 3.3 — Panel label "Particulate Matter PM2.5" is redundant
**Severity: Nice to have**

The PM2.5 card label reads "Particulate Matter PM2.5" — PM stands for Particulate Matter, making this "Particulate Matter Particulate Matter 2.5."

**Recommendation:** Use "Fine Particle Pollution (PM2.5)" which is the plain-language EPA term, or simply "Air Quality Index · PM2.5".

**Effort: Small** (one string change)

---

### Issue 3.4 — "In the News" section has no visual separation or header hierarchy
**Severity: Nice to have**

The news headlines section below the narrative is injected as raw inline HTML with a left border and small label. It lacks the same card/section treatment that the rest of the panel uses. After reading the AI narrative, the transition to news headlines is abrupt.

**Recommendation:** Wrap the news section in a defined component with consistent padding, a visible section label at the same weight as "Ask About This County", and a thin divider. Give each headline a source badge with favicon or colored source tag for scannability.

**Effort: Medium**

---

## 4. TYPOGRAPHY & READABILITY

### Issue 4.1 — Multiple color values fail WCAG AA contrast minimum
**Severity: Critical**

Against the near-black `#04040a` background:

| Element | Color | Estimated Contrast | WCAG AA (4.5:1) |
|---|---|---|---|
| `--text-muted` labels (#40405a) | #40405a | ~1.7:1 | **FAILS** |
| `--text-dim` (#7a7a92) | #7a7a92 | ~3.9:1 | **FAILS** (< 4.5:1) |
| `welcome-section-label` (amber at opacity 0.55) | ~rgba(249,115,22,0.55) | ~2.1:1 | **FAILS** |
| `.step-num` (amber at opacity 0.38) | ~rgba(249,115,22,0.38) | ~1.5:1 | **FAILS** |
| `.tagline` (#40405a) | #40405a | ~1.7:1 | **FAILS** |

These aren't decorative elements — `--text-muted` is used for section labels, step numbers, card labels, and the legend footnote. The `--text-dim` color is used for most body copy in the welcome panel steps.

**Recommendation:**
- Raise `--text-dim` to at least `#9a9ab4` (≈4.6:1)
- Raise `--text-muted` to at least `#6a6a8a` for body copy, or restrict it to purely decorative/large elements only
- Replace opacity-based amber dimming (`rgba(249,115,22,0.38)`) with a fixed accessible value — `#c2651a` achieves ~4.6:1
- Use WCAG-compliant contrast for all interactive text elements and readable labels

**Effort: Medium** — requires updating CSS variables and testing each instance.

---

### Issue 4.2 — Narrative text italic serif at 1.15rem is good, but line-height 1.95 may feel bloated on long passages
**Severity: Nice to have**

`line-height: 1.95` is unusually generous for 1.15rem body text. While it creates breathing room for short AI narratives, on longer passages it will make the text feel disconnected and hard to follow as a continuous read.

**Recommendation:** Use `line-height: 1.7` for narrative text — still generous for readability, but tighter enough to maintain narrative flow. Reserve 1.95 for blockquotes or pull quotes.

**Effort: Small** (one CSS value)

---

### Issue 4.3 — Font size below 0.7rem used for critical interactive labels
**Severity: Important**

Numerous interactive elements have font sizes of 0.55rem–0.62rem:
- `welcome-section-label`: 0.55rem
- `.ctrl-title`, `.legend-title`: 0.58rem
- `.events-dropdown-title`: 0.58rem
- `.pm25-card-label`: 0.56rem
- `.layer-row label`: 0.62rem

At 96dpi, 0.55rem ≈ 8.8px. This is below the 9px practical floor for desktop legibility and will be essentially invisible on lower-resolution or non-Retina displays.

**Recommendation:** Set a minimum font size floor of 0.7rem (11.2px) for all interactive labels and section headers. The mono typeface DM Mono has slightly narrower letterforms that help, but 0.58rem remains too small for general audiences.

**Effort: Small** — update CSS font-size values on identified elements.

---

## 5. COLOR & VISUAL HIERARCHY

### Issue 5.1 — The amber accent is overused, reducing its ability to signal importance
**Severity: Important**

Amber (#f97316) appears on: the logo, header top border, the logo accent bar, section label text, active states, borders, the county name hover in events, the PM2.5 number, the bar fill, the spinner border, scroll thumbs, and map hover borders. When everything is amber, nothing is amber. The accent has lost its ability to communicate "this is important" or "this is interactive."

**Recommendation:** Reserve amber exclusively for: (a) interactive affordances (hover states, active selections, CTA buttons), and (b) the highest severity air quality readings (the "USG" tier and above). Use the existing `--text-dim` (#7a7a92) for structural chrome like section headers, labels, and decorative dividers. Let amber mean "pay attention here."

**Effort: Medium** — requires a systematic pass through all amber usages to categorize and reassign.

---

### Issue 5.2 — Layer control dots (16x2px) are too small to distinguish layers
**Severity: Important**

Each layer row in the controls has a `layer-dot` that is 16px wide × 2px tall — essentially a thin line. The three dots are:
- PM2.5: `#f97316` at opacity 0.85
- Smoke: `#fb923c` at opacity 0.65
- Fires: `#ef4444` at full opacity

At 2px height, the difference between #f97316 and #fb923c is virtually imperceptible. The red for fires is distinguishable, but the first two look identical.

**Recommendation:** Use 8×8px circles (matching the top-story-dot pattern already used in the welcome panel). This is large enough to clearly show color differences. Better still, use a small icon per layer: a gradient square for PM2.5, a cloud shape or wavy line for smoke, and a flame for fires.

**Effort: Small**

---

### Issue 5.3 — Dark theme is premium — but the lowest-contrast elements undermine it
**Severity: Important**

The grain texture overlay, glassmorphism panels, amber gradient header line, and subtle `box-shadow` glows all contribute to a genuinely premium aesthetic. This is the product's biggest visual strength. However, when text fails contrast ratios (Issue 4.1), the "premium" feeling is contradicted by content that users cannot actually read.

**Recommendation:** Fix contrast issues (Issue 4.1) and the design will be consistently premium. Additionally, consider a very subtle ambient glow behind the side panel on dark nights — a `box-shadow: -8px 0 60px rgba(249,115,22,0.04)` on the panel left edge — to make the panel feel alive without being distracting.

**Effort: Small** (after contrast fixes are in)

---

## 6. MOBILE RESPONSIVENESS

### Issue 6.1 — Mobile layout is effectively broken
**Severity: Critical**

The only mobile breakpoint (at 640px) sets `--panel: 100vw`, making the side panel full-width. This means:
1. When a user clicks a county, the panel opens full-width and completely covers the map
2. There is no way to return to the map to select a different county without using the close button (which is tiny: 24×24px)
3. The layer control (`#layer-ctrl`) and legend (`#legend`) remain at their desktop positions and will overlap map content and each other on small screens
4. The date picker has `disableMobile: true`, forcing flatpickr's own calendar — which may display poorly on a phone
5. The footer bar (centered at bottom) will collide with the zoom controls on narrow screens

**Recommendation — mobile priorities in order:**

1. **Bottom sheet pattern for county panel:** On mobile, the panel should slide up from the bottom (60% of viewport height) with a drag handle, leaving the top 40% of map visible. Users can scroll the bottom sheet to read, or pull it down to dismiss and return to the map.

2. **Collapsible layer/legend controls:** On mobile, replace the always-visible float panels with a single FAB (floating action button) in the bottom-right that expands to show layer toggles. The legend can be hidden by default with a "show legend" link.

3. **Larger touch targets:** The close button (24×24px), checkboxes (12×12px), and the ⓘ info button (15×15px) all fall below the 44×44px minimum recommended touch target size.

4. **Header simplification:** On mobile, the date picker area should be collapsible or moved to a bottom bar, as it takes significant header width.

**Effort: Large** — the bottom sheet pattern requires restructuring the side panel's positioning logic. Touch targets can be fixed separately (Medium).

---

## 7. LOADING STATES & ERROR HANDLING

### Issue 7.1 — Multiple simultaneous loading states overwrite each other
**Severity: Important**

All three layers (PM2.5, smoke, fires) call `showLoading()` in parallel. The loading indicator shows one text string, so whichever `showLoading()` call runs last wins — the display flickers between "Loading PM2.5 data…", "Loading smoke data…", and "Loading fire data…" before settling. This is disorienting.

**Recommendation:** Instead of one text string, show a progress indicator with three named states, e.g.:
```
⟳ PM2.5  ✓ Smoke  ⟳ Fires
```
Or simplify: just show "Loading map data…" with a determinate-ish bar that fills as each layer resolves. The current `loadingCount` counter is already tracking parallel loads — use it to show `N of 3 loaded` or similar.

**Effort: Medium**

---

### Issue 7.2 — Error messages show raw HTTP status codes and are not user-friendly
**Severity: Important**

When `generateStory()` fails, the error is displayed as:
```
Error: HTTP 500
```
Or in the catch case:
```
Error: Failed to fetch
```
These are developer-level messages that mean nothing to a journalist or community member.

**Recommendation:** Map common errors to plain-language messages:
- HTTP 404: *"No data available for this county on this date. Try an adjacent date or a different county."*
- HTTP 500/503: *"The story generator is temporarily unavailable. Please try again in a moment."*
- Network failure ("Failed to fetch"): *"Unable to connect. Please check your internet connection."*

Apply the same treatment to chat errors. Also: after an error on `generateStory()`, re-enable the Generate Story button so the user can retry without refreshing.

**Effort: Small**

---

### Issue 7.3 — When smoke or fires return no data, there is no user-visible feedback
**Severity: Nice to have**

`loadSmoke()` and `loadFires()` silently return early if the server returns 0 features. The user has no way to know whether fires are absent from the map because (a) there are no fires, or (b) the data failed to load.

**Recommendation:** When a layer returns 0 features, update the layer label in the control with a subtle "No data" or "None detected" state — e.g., gray out the layer row checkbox and label. This tells the user the layer is active but genuinely empty, which is meaningful for a smoke/fire product.

**Effort: Small**

---

## 8. HISTORIC EVENTS PANEL

### Issue 8.1 — The events list is unsorted and inconsistently ordered
**Severity: Nice to have**

The 8 hardcoded events appear in this order: 2025, 2018, 2021, 2020, 2020, 2017, 2017, 2013. This is neither chronological (newest first), chronological (oldest first), nor sorted by severity. The Camp Fire (85 deaths) appears before the Dixie Fire which appears before August Complex — there's no discernible ranking logic.

**Recommendation:** Sort by date descending (most recent first) for a news-forward product. Add a subtle "Most deadly" or "Largest acreage" tag to 2–3 anchor events to signal why they matter. Consider adding one more event from 2022 (McKinney Fire) to fill the gap.

**Effort: Small**

---

### Issue 8.2 — The dropdown has no max-height, and event names truncate with ellipsis
**Severity: Nice to have**

If the events list grows beyond 8 items, the dropdown will extend off-screen with no scroll. Additionally, `.event-name` has `white-space: nowrap; overflow: hidden; text-overflow: ellipsis;` — the "Palisades & Eaton Fires" name already approaches this limit.

**Recommendation:** Add `max-height: 60vh; overflow-y: auto;` to `#events-list`. Consider two-line event names (remove `white-space: nowrap`) since the serif typeface makes multi-line names more readable than truncated ones.

**Effort: Small**

---

### Issue 8.3 — Dropdown close behavior: clicking map dismisses it, but Escape key does not
**Severity: Nice to have**

The document-level `click` handler closes the events dropdown correctly. However, pressing `Escape` does not close it, violating standard dropdown UX convention and WCAG 2.1 success criterion 1.4.13 (content on hover or focus can be dismissed via keyboard).

**Recommendation:** Add a `keydown` listener for `Escape` to call `closeEventsPanel()`. This is also good practice for the info tooltips.

**Effort: Small** (2–3 lines of JS)

---

## Priority Action Matrix

| Priority | Issue | Effort |
|---|---|---|
| 🔴 Critical | 6.1 — Mobile layout broken (bottom sheet + touch targets) | Large |
| 🔴 Critical | 4.1 — WCAG contrast failures across text colors | Medium |
| 🔴 Critical | 2.1 — No hover tooltip showing county name + PM2.5 | Small |
| 🔴 Critical | 1.1 — Default date is not today, unexplained | Small |
| 🟠 Important | 3.1 — "Generate Story" requires a second click | Medium |
| 🟠 Important | 7.2 — Raw HTTP error codes shown to users | Small |
| 🟠 Important | 2.3 — No cursor: pointer on county polygons | Small |
| 🟠 Important | 2.4 — Smoke + PM2.5 layers visually indistinguishable | Medium |
| 🟠 Important | 4.3 — Font size below 0.7rem for interactive labels | Small |
| 🟠 Important | 3.2 — "USG*" label is cryptic | Small |
| 🟠 Important | 2.2 — Onboarding tip too brief (5 seconds) | Small |
| 🟠 Important | 5.1 — Amber overused, diluting importance signal | Medium |
| 🟠 Important | 7.1 — Loading states overwrite each other in parallel | Medium |
| 🟠 Important | 5.2 — Layer dots too small to distinguish | Small |
| 🟡 Nice to have | 1.2 — No primary CTA in welcome panel | Small |
| 🟡 Nice to have | 3.4 — "In the News" lacks visual structure | Medium |
| 🟡 Nice to have | 4.2 — Narrative line-height 1.95 too loose | Small |
| 🟡 Nice to have | 7.3 — No feedback when layer returns 0 features | Small |
| 🟡 Nice to have | 8.1 — Historic events unsorted | Small |
| 🟡 Nice to have | 8.2 — Dropdown no max-height, names truncate | Small |
| 🟡 Nice to have | 8.3 — Escape key doesn't close dropdown | Small |
| 🟡 Nice to have | 3.3 — "Particulate Matter PM2.5" is redundant | Small |
| 🟡 Nice to have | 1.3 — Duplicate wordmark in header + welcome panel | Small |

---

## Recommended Sprint Breakdown

### Sprint 1 — Accessibility + Quick Wins (1–2 days)
- Fix WCAG contrast values (`--text-dim`, `--text-muted`, opacity-based amber)
- Add `cursor: pointer` on GeoJSON layers
- Add county name + PM2.5 Leaflet tooltip on hover
- Fix "USG*" → full label
- Fix error messages (HTTP codes → plain language)
- Fix default date to today or add explanation
- Extend onboarding tip to 10s
- Fix Escape key on dropdown
- Fix loading text to not overwrite ("Loading map data…")

### Sprint 2 — Core Interaction Improvements (2–3 days)
- Auto-trigger narrative generation on county click (remove explicit button)
- Differentiate smoke layer color from PM2.5 (redesign to blue-gray)
- Update layer dots to 8×8px circles
- Reduce amber overuse (audit each instance)
- Add "No data detected" state for empty layers
- Sort historic events chronologically (newest first)
- Font size audit: enforce 0.7rem floor

### Sprint 3 — Mobile (3–5 days)
- Implement bottom sheet pattern for county panel on mobile
- Increase touch targets to 44×44px minimum
- Collapse layer/legend controls into FAB or bottom bar on mobile
- Fix footer/zoom overlap on narrow screens
- Test flatpickr behavior on iOS/Android

---

## What's Working Well (Keep These)

- **PM2.5 color scale** — the green → yellow → orange → red → purple → deep purple progression is semantically correct and matches EPA conventions. The count-up animation on PM2.5 number is a lovely detail.
- **The grain texture + glassmorphism** — creates genuine editorial premium feel without being heavy-handed.
- **Cormorant Garamond for narrative text** — italic serif for the AI-generated story is exactly right. It signals "this is writing" rather than "this is a data readout."
- **The `worst-badge` with blinking dot** — the "Worst Affected County" badge with animated red dot is a strong signal without being sensational.
- **Historic events panel design** — the year / name / location / note three-column structure is well-organized and scannable.
- **The flame marker animation** — flickering CSS flame icons for fire points are delightful and informative (size = intensity).
- **`pulseLayer` on historic event auto-open** — flashing the amber border to draw attention to the auto-selected county is smart UX for the historic events flow.
- **Panel crossfade animation** — the 0.3s translateX crossfade between welcome and county views feels smooth and polished.
