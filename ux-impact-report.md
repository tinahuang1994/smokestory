# SmokeStory Financial Impact Page — UX/UI Review
**Reviewed by:** Senior UX/UI Designer (Data Journalism & Financial Products)
**Date:** 2026-03-26
**Files reviewed:** `frontend/impact.html`, `frontend/index.html`
**Scope:** Financial Impact page (`/impact`), entry point card on the main map page

---

## Executive Summary

The Financial Impact page has a strong editorial foundation: the typographic system is cohesive, the dark-glass aesthetic is credible, and the three-card structure correctly separates distinct estimates. The headline number ($36B–$40B) is visually dominant. However, several issues undermine clarity, trust, and discoverability — particularly around the "must not add" disclaimer, the comparison chart's ambiguous proportions, the map's missing info button, and the entry-point CTA on the main page. None of these are blocking issues, but several are Important-level problems that would concern a financial editor.

---

## 1. VISUAL HIERARCHY

### 1.1 — Headline number legibility
**Severity:** Important

**Problem:** `$36B — $40B` uses an em dash with spaces (`—`) inside `.headline-number`. This is a typographic punctuation choice that can read as a subtraction sign to numerically-oriented audiences, especially at large sizes. Financial publications (Bloomberg, WSJ) universally use an en dash with thin spaces (`–`) for numeric ranges. The current em dash also makes the range asymmetric: `$36B` and `$40B` are not visually balanced around a wide separator.

**Fix:** Change the HTML in the hero section from:
```html
<div class="headline-number">$36B — $40B</div>
```
to:
```html
<div class="headline-number">$36B&thinsp;&ndash;&thinsp;$40B</div>
```
Apply the same fix to the card number in Card 01:
```html
<div class="card-number">$36B&thinsp;&ndash;&thinsp;$40B</div>
```
And in `index.html` impact card (line ~1610):
```js
`$36B&thinsp;&ndash;&thinsp;$40B`
```

**Effort:** Small

---

### 1.2 — Headline number is not visually anchored as THE primary estimate
**Severity:** Important

**Problem:** The `.headline-section` block shows `$36B–$40B` large in amber, then immediately below it renders the three cards which also repeat that same number at 1.9rem in white. The page gives no visual cue that the three cards are subordinate to — and expanding upon — the headline. There is no section eyebrow label before the cards grid saying "The Three Estimates" or similar, and no section separator. A first-time reader may think there are four separate estimates.

**Fix:** Add a section-level eyebrow label and a top-border separator above `.cards-section`:
```html
<div class="cards-section">
  <div style="font-family:var(--mono);font-size:0.58rem;letter-spacing:0.26em;
              text-transform:uppercase;color:var(--text-muted);margin-bottom:20px;
              padding-bottom:14px;border-bottom:1px solid var(--border);">
    Three Independent Estimates &mdash; Each Measures Something Different
  </div>
  <div class="cards-grid">
    <!-- cards -->
  </div>
</div>
```

**Effort:** Small

---

### 1.3 — Amber left border on cards is too thin to be a strong financial signal
**Severity:** Nice to have

**Problem:** The cards use `border-left: 3px solid var(--amber)`. At 3px on a dark card against a near-black background, this border reads as a subtle design accent rather than a meaningful financial categorization signal. Bloomberg and FT use 4–6px colored borders on category-coded items. Additionally, on hover the border transitions to `var(--border-amber)` (an orange at only 22% opacity) which is dimmer than the default state — this is backwards; hover should reinforce, not dim.

**Fix 1 — Increase border width:**
```css
.estimate-card {
  border-left: 4px solid var(--amber);
}
```

**Fix 2 — Fix hover state so it stays bright:**
```css
.estimate-card:hover {
  border-color: rgba(249,115,22,0.2);
  border-left-color: var(--amber-l); /* #fb923c — brighter on hover */
  background: rgba(249,115,22,0.04);
}
```

**Effort:** Small

---

### 1.4 — Card 01 lacks visual differentiation from Cards 02 and 03 as the HEADLINE card
**Severity:** Important

**Problem:** All three cards are identical in visual weight. Card 01 carries the headline figure (`$36B–$40B`) and represents the primary "story" estimate, but it is indistinguishable from Cards 02 and 03. Readers accustomed to data journalism (NYT, The Economist) expect the lead figure to be visually dominant. Cards 02 and 03 carry the "Separate — Not Additive" and "SmokeStory Unique Contribution" badges but Card 01 carries no badge at all, making it feel like it might be the most uncertain entry.

**Fix:** Add a "HEADLINE ESTIMATE" badge to Card 01 and apply a subtle amber background tint to differentiate it:
```html
<!-- CARD 1 -->
<div class="estimate-card" style="background:rgba(249,115,22,0.06);border-left:4px solid var(--amber);">
  <div class="card-label">Estimate 01</div>
  <div class="card-badge" style="background:rgba(249,115,22,0.18);border-color:rgba(249,115,22,0.5);color:var(--amber);">
    Headline Estimate
  </div>
  <!-- rest of card unchanged -->
</div>
```

**Effort:** Small

---

### 1.5 — Card numbers use DM Mono at 1.9rem — slightly small for financial figures
**Severity:** Nice to have

**Problem:** `.card-number` is set to `font-size: 1.9rem`. On a 900px content column, three cards side by side render these numbers at roughly 110px wide each. The number feels appropriately sized at desktop, but on iPad (768–900px range) the three-column grid forces the cards quite narrow and the numbers can feel cramped.

**Fix:** Increase to `2.1rem` and add a `min-width: 0` on the card to prevent overflow:
```css
.card-number {
  font-size: 2.1rem;
}
.estimate-card {
  min-width: 0; /* allows text to wrap or scale in flex/grid context */
}
```

**Effort:** Small

---

## 2. INFORMATION FLOW

### 2.1 — "Must not be added together" disclaimer is buried and styled too quietly
**Severity:** Critical

**Problem:** The most important editorial rule on this page — that the three estimates measure different things and must not be summed — appears in two places: (1) as a small italic note in `.headline-note` (border-left at 40% opacity, body text at 0.8rem) and (2) in the footer `.disclaimer-section` in `--text-muted` color at 0.58rem monospace. Neither treatment is prominent enough. The `.disclaimer-section` uses `border-left: 3px solid rgba(255,255,255,0.06)` — this is effectively invisible and conveys no urgency. A reader who screenshots only the cards section and shares them would have no warning in frame. This is the kind of omission that causes reputational damage for a financial data publication.

**Fix 1 — Strengthen the inline `.headline-note` above the cards:**
```css
.headline-note {
  border-left: 3px solid rgba(249,115,22,0.7); /* increase from 0.4 to 0.7 opacity */
  color: var(--text-dim); /* increase from --text-muted (#40405a) to --text-dim (#7a7a92) */
  font-size: 0.85rem; /* increase from 0.8rem */
  background: rgba(249,115,22,0.04); /* add subtle amber tint */
  padding: 12px 16px; /* increase from 10px 16px */
}
```

**Fix 2 — Completely restyle the `.disclaimer-section` at the bottom:**
```html
<div class="disclaimer-section" style="
  border: 1px solid rgba(249,115,22,0.25);
  border-left: 4px solid var(--amber);
  background: rgba(249,115,22,0.05);
  padding: 20px 24px;">
  <div style="font-family:var(--mono);font-size:0.6rem;letter-spacing:0.2em;
              text-transform:uppercase;color:var(--amber);margin-bottom:10px;opacity:0.9;">
    Important Note on Methodology
  </div>
  <div class="disclaimer-text" style="
    color: var(--text-dim); /* up from --text-muted */
    font-size: 0.65rem; /* up from 0.58rem */
    text-align: left;">
    These three estimates measure different things and must not be added together.
    All figures are preliminary estimates using public data and established methodology.
    Data vintage: CAL FIRE February 5, 2025 · CAR 2024 · EPA AQS January 2025.
    SmokeStory is an independent open-source project, not an insurance company,
    government agency, or academic institution.
  </div>
  <a href="/methodology" class="methodology-link" style="
    opacity: 0.85;
    margin-top: 14px;
    display: inline-block;">Read Full Methodology →</a>
</div>
```

**Effort:** Small

---

### 2.2 — Page narrative flow: hero leads with human toll, then loses emotional thread
**Severity:** Nice to have

**Problem:** The hero correctly opens with "29 Lives Lost · 150,000 Residents Displaced" which establishes human stakes before the financial numbers. However, after the headline number block, the page moves directly into abstract financial cards with no connective tissue explaining why these three different types of estimates exist. A reader unfamiliar with insurance vs. market value vs. health economics will not understand why these three numbers are so different in scale ($36B vs. $3.9B vs. $0.5–$1B).

**Fix:** Add a one-sentence bridge paragraph between the `.headline-section` and `.cards-section`:
```html
<div style="font-family:var(--sans);font-size:0.85rem;font-weight:300;
            color:var(--text-dim);line-height:1.75;text-align:center;
            max-width:560px;margin:0 auto 40px;">
  Insurance companies count what was insured. Economists count broader market losses.
  SmokeStory adds what neither measures: the health cost of the smoke itself.
  Three lenses on the same disaster — each valid, none additive.
</div>
```

**Effort:** Small

---

### 2.3 — Comparison bar chart has misleading proportions
**Severity:** Critical

**Problem:** The bar chart in `.comparison-section` assigns `width:100%` to UCLA Anderson ($95B–$164B) and `width:29%` to the SmokeStory estimate ($36B–$40B). However, 29% of $164B is approximately $47.5B — which overrepresents the SmokeStory figure. Moody's at `width:19%` would imply ~$31B (close enough) but Milliman at `width:25%` implies ~$41B, which is within range of the stated $25B–$39B. The inconsistency is that the bars appear to be arbitrary visual decisions rather than scaled to the stated values.

More critically: the chart uses `--text-muted` color (`#40405a`) for all non-highlighted bar labels. At this contrast ratio (~2.4:1 against `#04040a`) this fails WCAG AA (minimum 4.5:1 for normal text). The `.bar-value` spans at `var(--text-muted)` are even harder to read.

**Fix 1 — Normalize bars to a consistent reference value.** Using $164B as 100%:
- Moody's $20B–$30B (mid: $25B) → `width: 15%`
- Milliman $25B–$39B (mid: $32B) → `width: 20%`
- SmokeStory $36B–$40B (mid: $38B) → `width: 23%`
- UCLA Anderson $95B–$164B → `width: 100%`

Update the HTML:
```html
<div class="bar-fill" style="width:15%;"></div>   <!-- Moody's -->
<div class="bar-fill" style="width:20%;"></div>   <!-- Milliman -->
<div class="bar-fill highlighted" style="width:23%;"></div>  <!-- SmokeStory -->
<div class="bar-fill" style="width:100%;"></div>  <!-- UCLA Anderson -->
```

**Fix 2 — Add a note clarifying the scale baseline:**
Add to `.chart-note`:
```
Bars scaled to UCLA Anderson's upper estimate ($164B) as 100%. SmokeStory's Estimate 01 measures market value of destroyed structures only; UCLA Anderson measures total economic impact including indirect losses.
```

**Fix 3 — Increase contrast on non-highlighted bar labels:**
```css
.bar-label {
  color: var(--text-dim); /* #7a7a92 — up from --text-muted #40405a */
}
.bar-label .bar-value {
  color: var(--text-dim); /* up from --text-muted */
}
```

**Effort:** Medium

---

### 2.4 — "How We Calculated This" expand buttons are too quiet and ambiguous in affordance
**Severity:** Nice to have

**Problem:** The `.card-expand-trigger` buttons use `opacity: 0.75` on amber text at `0.55rem` font size. At this size the interactive affordance is weak — users may not recognise these as clickable. The `↓` arrow is a good signal but the label "How We Calculated This" does not communicate that it reveals methodology detail. On mobile, the 6px padding makes the touch target too small (Apple HIG recommends 44px minimum).

**Fix:**
```css
.card-expand-trigger {
  font-size: 0.6rem;       /* up from 0.55rem */
  opacity: 0.85;            /* up from 0.75 */
  padding: 8px 0 4px;      /* increase vertical padding for touch target */
  min-height: 44px;         /* meet touch target minimum */
  display: flex;
  align-items: center;
}
```
Change button label from `How We Calculated This ↓` to `+ Sources & Methodology` for better scannability and a clearer affordance signal.

**Effort:** Small

---

## 3. MAP SECTION

### 3.1 — No info button (ⓘ) with metadata for fire perimeter layer
**Severity:** Important

**Problem:** The map shows fire perimeters with a tooltip on hover, but there is no persistent info button or map legend explaining what the red polygons represent, their data source, or their vintage date (CAL FIRE Feb 5, 2025). A reader looking at the map cold has no context. The layer control panel lists "Fire Perimeters", "Smoke Plumes", and "PM2.5 Counties" but provides no metadata about any of them. For a data journalism product this is a significant omission — NYT and Bloomberg always include inline data provenance for map layers.

**Fix:** Add a positioned info control to the map. Place it in the `<script>` block after `fireLayer.addTo(map)`:
```js
// Info button for fire perimeter layer
const infoControl = L.control({ position: 'bottomleft' });
infoControl.onAdd = function() {
  const div = L.DomUtil.create('div');
  div.innerHTML = `
    <div style="background:rgba(4,4,10,0.95);border:1px solid rgba(249,115,22,0.22);
                padding:10px 13px;font-family:'DM Mono',monospace;font-size:0.58rem;
                color:#7a7a92;letter-spacing:0.04em;line-height:1.7;max-width:220px;">
      <div style="color:#f97316;margin-bottom:5px;letter-spacing:0.14em;
                  text-transform:uppercase;font-size:0.52rem;">Data Sources</div>
      <div>&#x25A0; Fire Perimeters — CAL FIRE, Feb 5 2025</div>
      <div>&#x25A0; Smoke Plumes — NOAA HMS</div>
      <div>&#x25A0; PM2.5 — EPA AQS, Jan 9 2025</div>
    </div>`;
  return div;
};
infoControl.addTo(map);
```

**Effort:** Small

---

### 3.2 — Fire perimeters are approximate polygons with no caveat
**Severity:** Important

**Problem:** The fire perimeters in `firePerimeters` are hand-drawn approximate GeoJSON polygons with 8–9 coordinate pairs each. These do not represent the actual CAL FIRE perimeters and could significantly mislead readers about which properties were affected. There is no disclaimer on the map that says "approximate" or "illustrative." If a reader whose property is near the boundary sees it inside or outside the polygon, they may take action based on incorrect data.

**Fix 1 — Add "APPROXIMATE" watermark text to map section title:**
```html
<div class="section-subtitle">
  January 9, 2025 · Los Angeles County
  <span style="color:rgba(249,115,22,0.5);margin-left:8px;">(Perimeters approximate — see CAL FIRE for official boundaries)</span>
</div>
```

**Fix 2 — Update the Palisades Fire tooltip to add the caveat:**
```js
lyr.bindTooltip(
  `<strong style="color:#ef4444">${feat.properties.name}</strong>
   <br>${feat.properties.acres} acres
   <br><span style="color:#7a7a92;font-size:0.65em;">Approximate boundary</span>`,
  { sticky: true }
);
```

**Effort:** Small

---

### 3.3 — Map height is too short at 50vh with a min-height of 320px
**Severity:** Nice to have

**Problem:** `#impact-map { height: 50vh; min-height: 320px; }` On a 1080px viewport this gives 540px — adequate. On a 768px viewport this gives 384px — functional but cramped when both fire perimeters are visible. On mobile (667px iPhone SE), this gives 334px which is very close to the minimum and forces the user to toggle layers without seeing both fires in frame simultaneously. The Palisades fire (west) and Eaton fire (east) are about 35 miles apart; at zoom 10, seeing both on a 320px-tall map requires significant pan.

**Fix:**
```css
#impact-map {
  height: 55vh;
  min-height: 380px;
}
```
Additionally, consider setting the default zoom to 9 (instead of 10) to show both fires in frame on load:
```js
const map = L.map('impact-map', {
  center: [34.13, -118.35], /* shift center east slightly to balance both fires */
  zoom: 9,
  /* ... */
});
```

**Effort:** Small

---

### 3.4 — Smoke and PM2.5 layers load asynchronously with no loading indicator
**Severity:** Nice to have

**Problem:** `smokeLayer` and `pm25Layer` are fetched from the API and added to `layerControl` only after the fetch resolves. If the API is slow, the map renders with only "Fire Perimeters" visible and no layer control entries for Smoke or PM2.5. A reader may conclude those layers do not exist and close the page. There is no spinner or "Loading layers..." state.

**Fix:** Add a loading placeholder in the layer control immediately, then replace it when the data arrives. A simpler approach is to add a note below the map:
```html
<div id="map-loading-note" style="font-family:var(--mono);font-size:0.58rem;
     color:var(--text-muted);margin-top:8px;letter-spacing:0.06em;">
  Loading smoke and air quality layers...
</div>
```
Then in the `updateLayers()` function, hide it after both layers are added:
```js
function updateLayers() {
  if (smokeLayer && !smokeAdded) {
    smokeAdded = true;
    layerControl.addOverlay(smokeLayer, 'Smoke Plumes');
    smokeLayer.addTo(map);
  }
  if (pm25Layer && !pm25Added) {
    pm25Added = true;
    layerControl.addOverlay(pm25Layer, 'PM2.5 Counties');
    pm25Layer.addTo(map);
  }
  if (smokeAdded && pm25Added) {
    const note = document.getElementById('map-loading-note');
    if (note) note.style.display = 'none';
  }
}
```

**Effort:** Small

---

## 4. ENTRY POINT (Main Page Impact Card)

### 4.1 — CTA "View Full Analysis →" is too quiet and not visually distinct as a button
**Severity:** Important

**Problem:** The impact card on the main page (rendered in `index.html` around line 1616) uses an `<a>` tag styled as plain amber text with `opacity:0.8`. At `0.6rem` font size and no background, border, or button shape, this link does not read as a call-to-action in a UI context. It could easily be mistaken for a footnote or metadata label. "VIEW FULL ANALYSIS →" (the original text) is strong copy but the visual treatment fails to deliver on it.

Additionally, the CTA uses `target="_blank"` which opens in a new tab. For an intra-site navigation between two pages of the same product, this is unusual and breaks the browser back-button expectation. The user is in the main SmokeStory app; clicking a link that opens a new tab is unexpected and may feel like leaving.

**Fix 1 — Make the CTA a proper button-style link:**
```js
`<a href="/impact" ` +  /* remove target="_blank" */
   `style="display:inline-block;font-family:'DM Mono',monospace;font-size:0.6rem;` +
          `letter-spacing:0.12em;text-transform:uppercase;color:#f97316;` +
          `text-decoration:none;border:1px solid rgba(249,115,22,0.35);` +
          `padding:7px 14px;margin-top:4px;` +
          `background:rgba(249,115,22,0.08);` +
          `transition:background 0.2s,border-color 0.2s;" ` +
   `onmouseover="this.style.background='rgba(249,115,22,0.16)';` +
               `this.style.borderColor='rgba(249,115,22,0.6)'" ` +
   `onmouseout="this.style.background='rgba(249,115,22,0.08)';` +
              `this.style.borderColor='rgba(249,115,22,0.35)'">` +
  `View Full Analysis →` +
`</a>`
```

**Fix 2 — Change CTA copy** from "View Full Analysis →" to something that signals the destination more specifically:
```
See Financial Impact Report →
```
This mirrors the page title ("Financial Impact") and sets expectations correctly.

**Effort:** Small

---

### 4.2 — Impact card eyebrow label includes a house emoji, inconsistent with design system
**Severity:** Nice to have

**Problem:** The eyebrow label reads `🏠 Estimated Property Impact`. The SmokeStory design system (visible in both HTML files) uses no emoji in its UI components — the entire aesthetic relies on monospace text, letterforms, and a restrained amber/dark palette. The house emoji breaks this character and looks amateurish against the carefully constructed typographic system. (The main `index.html` does use emoji in a few places — `🔥`, `📅`, `👇` — but these are in UI chrome and button labels, not in data cards.)

**Fix:** Remove the emoji from the impact card eyebrow:
```js
`Estimated Property Impact`
/* was: `🏠 Estimated Property Impact` */
```

**Effort:** Small

---

### 4.3 — Impact card number uses DM Mono but the rest of the card uses inline styles with no hover state on the number itself
**Severity:** Nice to have

**Problem:** The `$36B — $40B` number in the card (`font-size:1.6rem`) is smaller than the equivalent number on impact.html (`.headline-number` at `5.5rem`). This is appropriate for a sidebar card. However, the entire card is built with inline styles, which means it cannot be updated centrally if the design system changes, and it has no visual affordance suggesting it is a "teaser" that expands to more detail. The card would benefit from a subtle border-bottom under the number (like a data table row) to signal there is more to see.

**Fix:** This is a code quality issue more than a visual one. The card should ideally be extracted to a named CSS class. As a minimum, add a visual separator:
```js
`<div style="border-bottom:1px solid rgba(249,115,22,0.12);padding-bottom:10px;margin-bottom:10px;">` +
  `<div style="font-family:'DM Mono',monospace;font-size:1.6rem;...">$36B&thinsp;&ndash;&thinsp;$40B</div>` +
`</div>`
```

**Effort:** Small

---

## 5. NAVIGATION

### 5.1 — "← Back to Map" is styled identically to a generic UI button with no sense of place
**Severity:** Important

**Problem:** The `.back-link` in the header (`← Back to Map`) uses the same monospace small-caps styling as any other control. At `0.6rem`, `letter-spacing: 0.12em`, it is visually indistinct in the header — especially because it is the only interactive element in the header and the header does not communicate that the user is in a sub-section of SmokeStory. There is no breadcrumb, no page title indicator in the header itself, and the logo does not link back to the map.

On mobile (under 640px), the header shrinks and the tagline (`California Wildfire Intelligence`) is hidden. The page-level orientation comes entirely from the `Back to Map` button and the hero `h1`. That is acceptable but marginal.

**Fix 1 — Make the logo a back-link on impact.html:**
```html
<a href="/" style="display:flex;align-items:center;gap:10px;text-decoration:none;">
  <div class="logo-accent"></div>
  <div class="logo-block">
    <div class="logo">Smoke&thinsp;Story</div>
    <div class="tagline">California Wildfire Intelligence</div>
  </div>
</a>
```

**Fix 2 — Increase prominence of the back link:**
```css
.back-link {
  font-size: 0.65rem;           /* up from 0.6rem */
  padding: 7px 15px;            /* up from 6px 13px */
  border-color: rgba(255,255,255,0.12); /* slightly more visible at rest */
}
```

**Fix 3 — Add a breadcrumb trail in the header spacer area (between logo-sep and back-link):**
```html
<div style="font-family:var(--mono);font-size:0.55rem;color:var(--text-muted);
            letter-spacing:0.1em;text-transform:uppercase;">
  Map &rsaquo; Financial Impact
</div>
```

**Effort:** Small–Medium

---

### 5.2 — Flow to methodology.html: "Read Full Methodology →" is buried and styled at low opacity
**Severity:** Important

**Problem:** The link to `/methodology` appears twice: once in the `.disclaimer-section` at `opacity: 0.65` and once... only there. There is no inline link within any of the three cards' expanded detail sections pointing to methodology. A reader who expands Card 01 and reads the detail is already in the right mental frame to want the full methodology — but they would have to scroll all the way to the bottom of the page to find the link. This increases friction for the most engaged readers.

**Fix 1 — Add a methodology link inside each card-detail section**, after the source citation:
```html
<div class="card-detail-source">
  Source: CAL FIRE field inspections (Feb 5, 2025) · California Association of Realtors 2024
  <br><a href="/methodology#estimate-01" style="color:var(--amber);opacity:0.7;
     text-decoration:none;font-family:var(--mono);font-size:0.55rem;letter-spacing:0.08em;">
    Full methodology →</a>
</div>
```
Apply equivalently to Cards 02 and 03 with `#estimate-02` and `#estimate-03` anchors.

**Fix 2 — Increase the bottom methodology link opacity:**
```css
.methodology-link {
  opacity: 0.8; /* up from 0.65 */
  font-size: 0.62rem; /* up from 0.58rem */
}
```

**Effort:** Small

---

### 5.3 — No indication on main map page that the impact report exists before selecting the right county and date
**Severity:** Nice to have

**Problem:** The impact card is gated behind a specific county (LA County) and a specific date (January 9, 2025). A user who has never heard of the Palisades fires, or who loads the app on a different date, will never see the impact card. There is no persistent navigation link to `/impact` in the header or welcome panel. For a feature that represents significant editorial investment, this is a discoverability problem.

**Fix:** Add a small persistent link in the `#welcome-view` panel, within the existing welcome content flow:
```html
<div style="margin-top:20px;padding:14px 16px;
            border:1px solid rgba(249,115,22,0.18);border-left:3px solid var(--amber);
            background:rgba(249,115,22,0.05);">
  <div style="font-family:var(--mono);font-size:0.52rem;letter-spacing:0.2em;
              text-transform:uppercase;color:var(--amber);opacity:0.8;margin-bottom:6px;">
    Featured Analysis
  </div>
  <div style="font-family:var(--sans);font-size:0.8rem;color:var(--text-dim);
              margin-bottom:8px;line-height:1.5;">
    2025 LA Wildfires: $36B–$40B in property destroyed
  </div>
  <a href="/impact" style="font-family:var(--mono);font-size:0.58rem;
     text-transform:uppercase;letter-spacing:0.1em;color:var(--amber);
     text-decoration:none;opacity:0.8;">View Financial Impact →</a>
</div>
```

**Effort:** Small

---

## 6. MOBILE CONSIDERATIONS

### 6.1 — Three cards stack correctly at 768px breakpoint but gap is too large on narrow screens
**Severity:** Nice to have

**Problem:** The media query `@media (max-width: 768px) { .cards-grid { grid-template-columns: 1fr; } }` correctly stacks cards to a single column. However, the gap between stacked cards remains `20px` which is fine, but the `.page-content` padding of `32px` left/right is tight on a 375px iPhone. Combined with the card padding of `22px 20px`, the available text area is only 375 - 64 - 40 = 271px. At `1.9rem` DM Mono for the card numbers, `$36B – $40B` measures approximately 220px wide — close to the limit with no breathing room.

**Fix:**
```css
@media (max-width: 480px) {
  .page-content {
    padding-left: 18px;
    padding-right: 18px;
  }
  .estimate-card {
    padding: 18px 16px;
  }
  .card-number {
    font-size: 1.7rem;
  }
  .hero-title {
    font-size: 2.6rem;
  }
  .headline-number {
    font-size: 4rem;
  }
}
```

**Effort:** Small

---

### 6.2 — Map on mobile has no "tap to enter full-screen" affordance
**Severity:** Nice to have

**Problem:** On mobile, the map is 50vh tall (approximately 374px on iPhone 14). The layer control (`collapsed: false`) shows all layers permanently open. On a 375px wide screen, the layer control panel (approximately 120px wide) consumes about a third of the map's usable width. Combined with the zoom controls, the right side of the map is significantly overlaid with UI. Leaflet's default layer control does not collapse on mobile.

**Fix:** Change the layer control to start collapsed on narrow viewports:
```js
const isMobile = window.innerWidth < 640;
let layerControl = L.control.layers(null, overlays, {
  position: 'topright',
  collapsed: isMobile  /* collapse on mobile, open on desktop */
}).addTo(map);
```

**Effort:** Small

---

### 6.3 — The `target="_blank"` on the impact card CTA breaks mobile user flow
**Severity:** Important

**Problem:** As noted in section 4.1, the impact card CTA uses `target="_blank"`. On mobile, this opens the Financial Impact page in a new browser tab. The user then has to navigate back to the map using the browser's tab switcher — the `← Back to Map` button on `/impact` will not close the new tab, it will just navigate within that tab. This creates a confusing fork in navigation state.

**Fix:** Remove `target="_blank"` from the impact card link (see Fix 1 in section 4.1).

**Effort:** Small

---

### 6.4 — Hero title "Palisades & Eaton Fires\nFinancial Impact" may orphan on narrow screens
**Severity:** Nice to have

**Problem:** The hero `<h1>` uses `<br>` to force a two-line layout:
```html
<h1 class="hero-title">Palisades &amp; Eaton Fires<br>Financial Impact</h1>
```
At 480px or narrower, `Palisades & Eaton Fires` may be too wide for a single line at `font-size: 3.6rem`, which would cause it to wrap before the `<br>` and create a three-line title with an awkward orphan. At `2.6rem` (the recommended mobile size from 6.1) this becomes manageable, but should be verified.

**Fix:** Replace the hard `<br>` with a responsive approach:
```html
<h1 class="hero-title">
  Palisades &amp; Eaton Fires
  <span style="display:block;">Financial Impact</span>
</h1>
```
Add to mobile CSS:
```css
@media (max-width: 480px) {
  .hero-title {
    font-size: 2.4rem;
  }
}
```

**Effort:** Small

---

## Summary Table

| # | Area | Issue | Severity | Effort |
|---|------|--------|----------|--------|
| 1.1 | Visual Hierarchy | Em dash instead of en dash in number ranges | Important | Small |
| 1.2 | Visual Hierarchy | Three cards not visually subordinate to headline number | Important | Small |
| 1.3 | Visual Hierarchy | Card amber left border too thin; hover dims instead of brightens | Nice to have | Small |
| 1.4 | Visual Hierarchy | Card 01 not visually differentiated as headline card | Important | Small |
| 1.5 | Visual Hierarchy | Card numbers slightly small for 3-column layout at iPad widths | Nice to have | Small |
| 2.1 | Information Flow | "Must not add" disclaimer too quiet — Critical editorial risk | **Critical** | Small |
| 2.2 | Information Flow | Missing narrative bridge between estimates and why they differ | Nice to have | Small |
| 2.3 | Information Flow | Comparison bar widths are proportionally inaccurate; low contrast on labels | **Critical** | Medium |
| 2.4 | Information Flow | Expand buttons too small and under-afforded for interaction | Nice to have | Small |
| 3.1 | Map | No info button or data provenance for map layers | Important | Small |
| 3.2 | Map | Fire perimeters are approximate with no caveat | Important | Small |
| 3.3 | Map | Map too short; default zoom does not show both fires | Nice to have | Small |
| 3.4 | Map | No loading state while smoke/PM2.5 layers fetch | Nice to have | Small |
| 4.1 | Entry Point | CTA "View Full Analysis" is text-only, not button-shaped; wrong `target` | Important | Small |
| 4.2 | Entry Point | House emoji breaks design system character | Nice to have | Small |
| 4.3 | Entry Point | Card number has no affordance suggesting it is a teaser | Nice to have | Small |
| 5.1 | Navigation | "Back to Map" understyled; no breadcrumb for page orientation | Important | Small–Medium |
| 5.2 | Navigation | Methodology link buried at low opacity; not inline in card details | Important | Small |
| 5.3 | Navigation | Impact page not discoverable without hitting specific county+date | Nice to have | Small |
| 6.1 | Mobile | Page padding too wide for 375px viewports with current card padding | Nice to have | Small |
| 6.2 | Mobile | Layer control stays open on mobile, overlapping map | Nice to have | Small |
| 6.3 | Mobile | `target="_blank"` breaks mobile navigation flow | Important | Small |
| 6.4 | Mobile | Hard `<br>` in hero title may cause orphan line on narrow screens | Nice to have | Small |

---

## Priority Order for Development

### Fix immediately (Critical)
1. **2.1** — Restyle the "must not add together" disclaimer to be prominent and readable (amber left border, higher contrast text, increased font size)
2. **2.3** — Recalculate bar chart widths to be proportionally accurate; fix contrast on non-highlighted bar labels

### Fix in next sprint (Important)
3. **1.4** — Add "Headline Estimate" badge and amber tint to Card 01
4. **1.2** — Add section eyebrow label above cards grid to establish hierarchy
5. **4.1** — Restyle impact card CTA as a button; remove `target="_blank"`
6. **6.3** — Remove `target="_blank"` from impact card (same fix as 4.1)
7. **5.2** — Add inline methodology links in each card's expanded detail section
8. **3.1** — Add data provenance info control to the map
9. **3.2** — Add "approximate perimeter" caveat to map section title and tooltip
10. **5.1** — Increase back-link size; make logo a clickable back-link; add breadcrumb
11. **1.1** — Replace em dashes with en dashes in number ranges throughout

### Polish when time allows (Nice to have)
12. All items marked "Nice to have" above

---

*Report end. All file paths referenced are relative to the repository root `/Users/tinahuang/Desktop/smokestory/frontend/`.*
