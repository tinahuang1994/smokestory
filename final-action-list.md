# SmokeStory — Final Prioritized Action List
**Synthesized by:** Chief Editor / Product Lead
**Date:** 2026-03-26
**Source reports:** UX (ux-impact-report.md), SciComm (scicomm-report.md), Journalist (journalist-report.md), Skeptic (skeptic-report.md), Data Integrity (data-integrity-report.md)
**Files in scope:** `frontend/impact.html`, `frontend/methodology.html`, `frontend/index.html`

---

## CONFLICT RESOLUTION LOG

Before the action list, I record where agents disagreed and how I resolved each conflict.

**Conflict 1 — Bar chart proportions (UX vs. Data Integrity)**
UX says the bar widths are wrong and provides corrected values (Moody's 15%, Milliman 20%, SmokeStory 23%). Data Integrity independently verified the existing widths (19%, 25%, 29%) against midpoint math and found them proportionally correct to within 0.3 percentage points. **Resolution: Data Integrity's arithmetic is correct. The existing CSS widths are proportionally accurate.** However, both UX and Skeptic independently identified a legitimate framing problem — the section is called "Published Estimates from Independent Sources" which implies SmokeStory is a peer of Moody's, and bars of different methodological scopes are placed side-by-side without sufficient explanation. The fix is a label and note change, not a bar-width change.

**Conflict 2 — "Too much text" vs. "Not enough context" (Journalist vs. UX/SciComm)**
Journalist says "critical information is too slow to surface" and context requires too many clicks. UX adds narrative bridge text between sections. SciComm wants longer disclaimer text. These appear to conflict, but they do not: the issue is not total word count but where information appears. **Resolution: Surface critical caveats in-context (beside the numbers where they matter), not only in collapsible sections or page footers. Do not add another wall of text between the hero and the cards — instead add short, targeted inline qualifiers.** The UX agent's bridge paragraph is kept as a small addition. The SciComm disclaimer expansion is kept for the bottom section. The Journalist's usability concern about the comparison chart is addressed by position, not removal.

**Conflict 3 — "SmokeStory Unique Contribution" badge (Journalist vs. Skeptic)**
Journalist says "reads as a marketing claim rather than a factual one." Skeptic says it "overstates novelty" and could not withstand scrutiny. Neither says remove the concept, only the language. **Resolution: Rename the badge from "SmokeStory Unique Contribution" to "Not in Other Published Estimates" with a date qualifier. This is factually defensible and removes the self-promotional framing without eliminating the legitimate distinction.**

**Conflict 4 — How prominent should the "independent project" disclaimer be? (UX vs. Skeptic)**
UX wants the disclaimer more visible (amber styling, higher contrast). Skeptic wants it moved earlier on the page as a near-top alert. **Resolution: Both are right about contrast (current color fails WCAG AA). Skeptic's suggestion of a near-top banner is too aggressive — it would undermine the premium design and reads as defensive. UX's approach of amber-bordered block with higher-contrast text is the right treatment. The "independent project" statement should stay at the bottom in a restyled block, not become a page-top warning.**

**Conflict 5 — Add more text vs. maintain scannability (UX vs. Journalist)**
UX recommends adding eyebrow labels, badges, bridge paragraphs, breadcrumbs, and a welcome panel featured link — totaling perhaps 150 words of new content. Journalist says "critical information too slow to surface" and wants the comparison chart higher. **Resolution: Implement UX additions that are structural (labels, badges, hierarchy signals) and skip any that add word count without improving scanability. The comparison chart position is addressed as a separate item. The detailed bridge paragraph between headline and cards is retained as a small addition since it directly solves the Journalist's usability complaint.**

---

## ACTION LIST

---

### P0 — Must Fix Before Sharing Publicly

---

**A1**
- **Priority:** P0
- **Agents:** Journalist, Skeptic
- **Problem:** "Claude AI" appears in the data sources footer alongside NOAA HMS, EPA AQS, and NASA VIIRS, implying it is a government-equivalent data source; any editor or fact-checker who sees this will immediately question the entire page's credibility.
- **Exact fix:** In `impact.html` and any shared footer template, locate the footer line that reads `NOAA HMS · EPA AQS · NASA VIIRS · Claude AI` and remove `· Claude AI` from the data sources list entirely. If AI tool use must be disclosed, add it as a separate line: `Built with assistance from Claude AI (narrative and code) · Open source: github.com/tinahuang1994/smokestory`
- **Files:** `frontend/impact.html`, `frontend/methodology.html`
- **Effort:** Small

---

**A2**
- **Priority:** P0
- **Agents:** Journalist, Skeptic
- **Problem:** There is no named author, contact email, or institutional affiliation anywhere on either page; no journalist can quote or follow up with the source, making citation impossible for most newsrooms.
- **Exact fix:** Add the following block to the bottom of the `.disclaimer-section` on both `impact.html` and `methodology.html`, before the closing `</div>`:
```html
<div style="margin-top:14px;font-family:var(--mono);font-size:0.6rem;
            color:var(--text-dim);letter-spacing:0.06em;line-height:1.8;">
  <span style="color:var(--amber);letter-spacing:0.16em;text-transform:uppercase;
               font-size:0.52rem;">Contact</span><br>
  Developed by [Name], independent researcher · [email@domain.com]<br>
  Open source: <a href="https://github.com/tinahuang1994/smokestory"
    style="color:var(--amber);opacity:0.7;text-decoration:none;">
    github.com/tinahuang1994/smokestory</a>
</div>
```
Replace `[Name]` and `[email@domain.com]` with actual contact information.
- **Files:** `frontend/impact.html`, `frontend/methodology.html`
- **Effort:** Small

---

**A3**
- **Priority:** P0
- **Agents:** UX (2.1), SciComm (2.1), Skeptic (4.1)
- **Problem:** The "must not be added together" disclaimer is styled in `--text-muted` (#40405a) text at 0.58rem monospace on a near-black background — a contrast ratio of approximately 2.5:1, below WCAG AA minimum of 4.5:1, making it technically unreadable for many users and legally invisible as a disclosure.
- **Exact fix:** Replace the entire `.disclaimer-section` block in `impact.html` with the following (this simultaneously fixes the contrast, the visibility, and the "why" explanation from SciComm):
```html
<div class="disclaimer-section" style="
  border: 1px solid rgba(249,115,22,0.25);
  border-left: 4px solid var(--amber);
  background: rgba(249,115,22,0.05);
  padding: 20px 24px;
  text-align: left;">
  <div style="font-family:var(--mono);font-size:0.6rem;letter-spacing:0.2em;
              text-transform:uppercase;color:var(--amber);margin-bottom:10px;">
    Important — How to Read These Numbers
  </div>
  <div style="font-family:var(--sans);font-size:0.72rem;color:var(--text-dim);
              line-height:1.75;font-weight:300;">
    These three estimates must not be added together because they measure categorically
    different things. Estimate 01 is the replacement value of buildings that burned.
    Estimate 02 is an unrealized paper decline in value for surviving homes on different
    properties — adding it to Estimate 01 would count separate properties twice.
    Estimate 03 is a healthcare and productivity cost, not a property cost at all.
    Summing them would mix incompatible accounting categories.<br><br>
    All figures are preliminary estimates using public data and established methodology.
    Data vintage: CAL FIRE February 5, 2025 · CAR 2024 · EPA AQS January 2025.
    SmokeStory is an independent open-source project, not an insurance company,
    government agency, or academic institution. These estimates are for informational
    and educational purposes only and are not suitable for insurance claims, legal
    proceedings, or government applications.
  </div>
  <a href="/methodology" class="methodology-link" style="
    opacity:0.85;margin-top:14px;display:inline-block;font-size:0.62rem;">
    Read Full Methodology →</a>
</div>
```
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A4**
- **Priority:** P0
- **Agents:** SciComm (1.1), Skeptic (1.1), UX (2.1)
- **Problem:** The page `<title>` says "Financial Impact" and the `<h1>` says "Financial Impact," but the headline number ($36B–$40B) is only the direct property destruction figure — a reader who screenshots the top of the page or sees a social share will reasonably infer it is the total economic cost of the fires.
- **Exact fix:**
  1. Change `<title>` in `impact.html` from:
     ```html
     <title>Financial Impact · SmokeStory</title>
     ```
     to:
     ```html
     <title>Property Destruction Estimates · 2025 LA Wildfires · SmokeStory</title>
     ```
  2. Change `<h1>` from:
     ```html
     <h1 class="hero-title">Palisades &amp; Eaton Fires<br>Financial Impact</h1>
     ```
     to:
     ```html
     <h1 class="hero-title">Palisades &amp; Eaton Fires<br>Economic Cost Estimates</h1>
     ```
  3. Change the `.headline-sub` text from `in property destroyed` to `market value of destroyed buildings — direct property destruction only`
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A5**
- **Priority:** P0
- **Agents:** SciComm (1.1), Skeptic (1.1, 4.2)
- **Problem:** The `.headline-note` appears after the $36B–$40B number and is styled as quiet body text; it does not prevent a reader from absorbing the number without the caveat, and the word "preliminary" never appears near the headline figure itself.
- **Exact fix:** Move the `.headline-note` div to appear above the `.headline-number` div, and replace its content with stronger language. Also add a "(preliminary)" qualifier below the number:
```html
<!-- Move headline-note ABOVE headline-number -->
<div class="headline-note" style="
  border-left:3px solid rgba(249,115,22,0.7);
  color:var(--text-dim);
  font-size:0.85rem;
  background:rgba(249,115,22,0.04);
  padding:12px 16px;
  margin-bottom:20px;
  text-align:left;">
  Three separate estimates are shown on this page. Each measures something different.
  They must not be added together. The number below is the direct property
  destruction figure only — not a total economic cost.
</div>
<div class="headline-number">$36B&thinsp;&ndash;&thinsp;$40B</div>
<div class="headline-sub">market value of destroyed buildings</div>
<div style="font-family:var(--mono);font-size:0.55rem;letter-spacing:0.12em;
            text-transform:uppercase;color:var(--text-muted);margin-top:4px;">
  Preliminary estimate · subject to revision
</div>
<div class="headline-location">Palisades + Eaton Fires · Los Angeles County</div>
```
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A6**
- **Priority:** P0
- **Agents:** Skeptic (4.4), Journalist (4)
- **Problem:** Same as A1 but applies to `index.html`'s footer — confirm the footer in the main map page also carries the "Claude AI" alongside federal data sources and remove it from there as well.
- **Exact fix:** Search `index.html` for the footer attribution line containing `Claude AI` and remove `· Claude AI` from the data sources list, keeping NOAA HMS, EPA AQS, and NASA VIIRS only.
- **Files:** `frontend/index.html`
- **Effort:** Small

---

**A7**
- **Priority:** P0
- **Agents:** Skeptic (5.2), UX (3.2)
- **Problem:** The map shows hard-coded approximate 8-point polygon fire perimeters with no visible disclaimer; a reader comparing these to CAL FIRE FRAP official perimeters would find substantial discrepancies, and property owners near the boundary could take action based on incorrect data.
- **Exact fix:**
  1. Add to the map section subtitle in `impact.html`:
  ```html
  <div class="section-subtitle">
    Fire Perimeters &amp; Air Quality · January 9, 2025 · Los Angeles County
    <span style="color:rgba(249,115,22,0.6);margin-left:8px;font-size:0.8em;">
      (Perimeters are approximate — see
      <a href="https://www.fire.ca.gov/incidents" target="_blank"
         style="color:rgba(249,115,22,0.7);text-decoration:none;">CAL FIRE</a>
      for official boundaries)
    </span>
  </div>
  ```
  2. Update both fire perimeter tooltip bindings to append `<br><span style="color:#7a7a92;font-size:0.65em;">Approximate boundary — not for legal use</span>` after the acreage line.
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A8**
- **Priority:** P0
- **Agents:** SciComm (3.1), Journalist (1), Skeptic (2.4)
- **Problem:** The COI vs. VSL methodology choice for Estimate 03 is explained in the methodology page with the note "VSL designed for chronic long-term exposure, not acute 14-day events" — this explanation is technically contestable (VSL is used for acute risks in federal rulemaking) and will be challenged by health economists; it also reads as evasive rather than transparent.
- **Exact fix:** In `methodology.html`, find the assumption line:
```html
<li><span class="assumption-id">A1</span>COI method used, not VSL. VSL designed for chronic long-term exposure, not acute 14-day events.</li>
```
Replace with:
```html
<li><span class="assumption-id">A1</span>Cost of Illness (COI) method used rather than Value of Statistical Life (VSL). COI counts only direct, measurable costs: hospital bills, emergency room fees, and lost wages. VSL — which government agencies use to price the statistical risk of premature death — would produce a substantially larger number, and is not used here because SmokeStory's sensor data does not provide the mortality attribution analysis that VSL calculations require. COI is a deliberate, conservative lower bound.</li>
```
- **Files:** `frontend/methodology.html`
- **Effort:** Small

---

**A9**
- **Priority:** P0
- **Agents:** Skeptic (3.1), SciComm (2.2)
- **Problem:** Card 03 on the impact page lists health cost components (hospital visits, ER, work days, asthma attacks) without mentioning that mortality costs are excluded; a public health researcher could credibly argue the $0.5B–$1.0B is a severe underestimate, and this is not disclosed on the impact page at all.
- **Exact fix:** In `impact.html`, in the Card 03 `card-detail` expanded section, move the health-cost category warning to the top and add a mortality exclusion disclosure. Replace the opening of that `card-detail` div with:
```html
<div class="card-detail">
  <strong style="color:var(--amber);">Note: This is a healthcare cost, not a property cost.
  It must not be added to Estimates 01 or 02. This estimate also excludes mortality costs —
  including mortality using VSL methodology would produce a substantially higher figure.
  COI is used as a conservative, verifiable lower bound.</strong>
  <br><br>
  SmokeStory's air quality data recorded LA County's air quality during the fires. For 14
  days, PM2.5 levels averaged 44.8 µg/m³ — nearly 5 times the EPA's safe limit of 9.0 µg/m³.
  <br><br>
  We used the EPA's published health impact formulas and cost figures — the same tools the EPA
  uses in its own air quality regulations — to estimate the health burden of the smoke. This
  approach counts hospital admissions, emergency room visits, lost work days, and asthma
  attacks caused by elevated PM2.5, then converts each using EPA-published cost values.
```
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A10**
- **Priority:** P0
- **Agents:** Data Integrity (Issue 3), Data Integrity (Issue 4), Data Integrity (Issue 5)
- **Problem:** Two calculation transcription errors exist in the methodology page: work-loss days shows 691,464 but the stated inputs produce 691,656 (192-day discrepancy); restricted-activity days shows 1,082,016 but inputs produce 1,082,592 (576-day discrepancy); the base total shows $546M but the sum of displayed line items is $546.2M — a visible arithmetic inconsistency that a fact-checker will immediately catch.
- **Exact fix:** In `methodology.html`, find the health impact functions mono-block and make these corrections:
  - Change `691,464 days` to `691,656 days` for work-loss days
  - Change `1,082,016 days` to `1,082,592 days` for restricted-activity days
  - Change `Base total: $546M` to `Base total: $546.2M`
  - Verify that the cost lines for work-loss (`$193.6M`) and restricted-activity (`$103.9M`) still round correctly with the corrected day counts (they do — see Data Integrity report verification).
- **Files:** `frontend/methodology.html`
- **Effort:** Small

---

### P1 — Should Fix Soon

---

**A11**
- **Priority:** P1
- **Agents:** Journalist (2), Skeptic (4.3), Data Integrity (Issue 6)
- **Problem:** Neither impact.html nor methodology.html shows a "last updated" date; the methodology page has "Version 3.0" but no release date; data sources like CAL FIRE DINS are flagged as subject to revision, so readers cannot tell if estimates are current.
- **Exact fix:** Add a visible last-updated line to both pages. In `impact.html`, add directly beneath the `.hero-stats` block:
```html
<div style="font-family:var(--mono);font-size:0.55rem;letter-spacing:0.12em;
            text-transform:uppercase;color:var(--text-muted);margin-top:12px;">
  Data as of: February 5, 2025 · Estimates subject to revision as official counts are updated
</div>
```
In `methodology.html`, update the version label to include the date: `Version 3.0 — Published [date]`
- **Files:** `frontend/impact.html`, `frontend/methodology.html`
- **Effort:** Small

---

**A12**
- **Priority:** P1
- **Agents:** Journalist (3), SciComm (5.2), Data Integrity (Issue 7), Skeptic (5.5)
- **Problem:** The CAR (California Association of Realtors) citation appears as "CAR 2024" in the methodology page without specifying which report, month, or URL; the Sathaye et al. citation is missing a DOI and full publication details needed for journalist verification.
- **Exact fix:**
  1. In `methodology.html`, find `<td class="source-name">CAR 2024</td>` and replace with:
  ```html
  <td class="source-name">California Association of Realtors (CAR) 2024 Median Home Price Report</td>
  <td>Pre-fire median sale prices by neighborhood</td>
  <td class="source-access">public reports — car.org/marketdata</td>
  ```
  2. Also in `methodology.html`, find `<div class="highlight-box-title">Pre-Fire Market Values — CAR 2024</div>` and replace with:
  ```html
  <div class="highlight-box-title">Pre-Fire Market Values — California Association of Realtors (CAR) 2024</div>
  ```
  3. In `methodology.html`, find the Sathaye et al. citation block and add `[Add: Volume, Issue, Pages/Article number, DOI when confirmed]` as a placeholder. In `impact.html` Card 02's source line, update from `Peer-reviewed study, Landscape and Urban Planning (2024)` to `Sathaye et al. (2024), Landscape and Urban Planning — full citation on methodology page`.
- **Files:** `frontend/methodology.html`, `frontend/impact.html`
- **Effort:** Small (text only, pending DOI confirmation which is a separate research task)

---

**A13**
- **Priority:** P1
- **Agents:** Journalist (4), Skeptic (2.4)
- **Problem:** The 4% demand surge assumption that drives the upper bound of $40B (vs. $36B lower bound) is unsourced in both pages; a range implies both endpoints are equally supported, but the upper bound is derived from an internal assumption with no published basis.
- **Exact fix:** In `impact.html`, Card 01's `card-detail` expanded section, after "This gives us the market value of what burned," add:
```html
Our lower bound is $36B. The upper bound of $40B adds a 4% adjustment for reconstruction
cost pressure — when tens of thousands of homes need rebuilding simultaneously, contractor
costs and materials prices typically rise. This is a conservative industry assumption; Milliman
used 15% for the same factor. [Citation for 4% to be added — currently an author judgment
based on post-disaster construction market literature.]
```
In `methodology.html`, under Estimate 01 Assumptions, add a note to the demand surge line: `[Author judgment based on post-disaster construction cost literature — specific citation pending.]`
- **Files:** `frontend/impact.html`, `frontend/methodology.html`
- **Effort:** Small

---

**A14**
- **Priority:** P1
- **Agents:** Skeptic (1.2), UX (2.1)
- **Problem:** Cards 01 and 03 have no "not additive" badge while Card 02 has a "Separate — Not Additive" badge; a reader scanning the three cards could add all three figures without seeing the warning at the card visual level.
- **Exact fix:** In `impact.html`, add the same badge style as Card 02's badge to Cards 01 and 03. The badge should read "Not Additive" and use the same `.card-badge` class. Specifically for Card 03, the badge text can be "Do Not Add — Different Category" to reinforce that this is a health cost, not a property cost.
```html
<!-- Add to Card 01, alongside other card badges -->
<div class="card-badge">Not Additive</div>

<!-- Add to Card 03, alongside existing "SmokeStory Unique Contribution" badge -->
<div class="card-badge" style="border-color:rgba(239,68,68,0.3);color:#f87171;">
  Do Not Add — Different Category
</div>
```
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A15**
- **Priority:** P1
- **Agents:** Skeptic (2.2), Journalist (1)
- **Problem:** The "SmokeStory Unique Contribution" badge reads as self-promotional marketing copy and implies novel scientific contribution; "any analyst with the same PM2.5 data could reproduce this calculation" and the claim of uniqueness may not withstand scrutiny.
- **Exact fix:** In `impact.html`, find the Card 03 badge that reads "SmokeStory Unique Contribution" and replace its text with:
```html
<div class="card-badge" style="background:rgba(20,184,166,0.12);border-color:rgba(20,184,166,0.3);color:#2dd4bf;">
  Not in Other Published LA Wildfire Estimates (as of Feb 2025)
</div>
```
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A16**
- **Priority:** P1
- **Agents:** SciComm (1.2), Skeptic (3.2)
- **Problem:** Card 01's title "Market Value of Destroyed Structures" and description do not tell readers that land, contents, vehicles, and infrastructure are excluded; a homeowner could read the card and believe SmokeStory's estimate captures their full loss.
- **Exact fix:** In `impact.html`, make two changes to Card 01:
  1. Change `card-title` from `Market Value of Destroyed Structures` to `Market Value of Destroyed Buildings`
  2. Change `card-desc` from: `The buildings that burned, valued at what they were worth before the fire. Based on CAL FIRE field inspections of every damaged structure.` to: `The buildings that burned, valued at what they were worth before the fire. Does not include land, contents, vehicles, or infrastructure. Based on CAL FIRE field inspections of every damaged building.`
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A17**
- **Priority:** P1
- **Agents:** SciComm (1.3)
- **Problem:** Card 02's title "Nearby Home Values Affected" is ambiguous and could be confused with physically damaged homes (Estimate 01) rather than surviving homes experiencing a statistical value decline.
- **Exact fix:** In `impact.html`, change the Card 02 `card-title` from `Nearby Home Values Affected` to `Drop in Value: Homes Near the Fire Zones`
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A18**
- **Priority:** P1
- **Agents:** Skeptic (1.3), SciComm (4.2)
- **Problem:** The $3.9B figure for Estimate 02 is displayed at the same visual weight as the other estimates with no signal that it is an unrealized paper value, not a cash transaction; readers scanning the cards can record it as a loss on par with the others.
- **Exact fix:** In `impact.html`, make two changes to Card 02:
  1. Add `(unrealized)` directly after the card number: change `$3.9B` display to `$3.9B (unrealized)`
  2. Expand the `card-desc` to: `Properties that survived but lost value because of their proximity to the fires. This is a paper loss — meaning the value declines on paper, but no cash changes hands and no one writes a check. These properties have not sold at a loss. The decline may recover over time as the neighborhood rebuilds.`
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A19**
- **Priority:** P1
- **Agents:** Skeptic (5.1), Journalist (4)
- **Problem:** The 2.2% property value depreciation rate used for Estimate 02 is a historical average across many California wildfires, but the card presents it as a precise applicable rate; the methodology page notes this may understate impact for the 2025 LA fires given their urban scale, but this caveat is inside a collapsed section.
- **Exact fix:** In `impact.html`, Card 02's expanded `card-detail`, add after the description of the 2.2% rate:
```html
<br><br>
Note: This 2.2% figure is a historical average from prior California wildfires and
may understate impact for the 2025 LA fires, which were among the largest urban fires
in California history. The actual decline for surviving properties may be higher.
```
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A20**
- **Priority:** P1
- **Agents:** SciComm (4.1)
- **Problem:** The Card 01 expanded section explains the lower bound ($36B) but never explains where the upper bound ($40B) comes from; a reader expanding the card to understand the range gets no answer.
- **Exact fix:** In `impact.html`, Card 01 `card-detail`, find the passage: `We multiplied that by what homes in those neighborhoods were worth before the fire — $3.3M average in Pacific Palisades, $1.4M average in Altadena.` and replace the follow-on sentence with:
```html
That produces our lower bound of $36B.
<br><br>
The upper bound of $40B applies a modest 4% adjustment for reconstruction cost pressure —
when tens of thousands of homes need rebuilding simultaneously, contractor costs and
materials prices typically rise. This is a conservative figure; insurance industry
estimates have used 15% for the same factor.
```
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A21**
- **Priority:** P1
- **Agents:** SciComm (4.3)
- **Problem:** The Estimate 03 range nearly doubles ($0.5B to $1.0B) with no explanation of what drives the upper bound; readers cannot assess whether this reflects genuine ambiguity or methodological weakness.
- **Exact fix:** In `impact.html`, Card 03 `card-detail`, add after the EPA methodology sentence:
```html
<br><br>
The lower bound ($0.5B) is our direct calculation from observed PM2.5 levels. The upper
bound ($1.0B) reflects two sources of uncertainty: air quality monitors do not cover every
neighborhood equally, so some areas may have experienced higher exposure than our data shows;
and vulnerable populations — the elderly, people with chronic illness — face higher health
risks than the population-average rates we used.
```
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A22**
- **Priority:** P1
- **Agents:** SciComm (5.3), Skeptic (3.4)
- **Problem:** The Card 03 expanded section says "We used the same method the EPA uses" which implies EPA endorsement; EPA's BenMAP rates were developed for general urban PM2.5, not specifically wildfire smoke which may carry additional toxic compounds.
- **Exact fix:** In `impact.html`, Card 03, replace the sentence `We used the same method the EPA uses to calculate the economic cost of air pollution: counting hospital visits, emergency room trips, missed work days, and asthma attacks caused by the smoke.` with:
```html
We used the EPA's published health impact formulas and cost figures — the same tools the
EPA uses in its own air quality regulations — to estimate the health burden of the smoke.
Note: BenMAP rates are based on general urban PM2.5. Wildfire smoke may carry additional
toxic compounds (benzene, heavy metals), so actual health impacts could be higher than
shown here.
```
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A23**
- **Priority:** P1
- **Agents:** UX (4.1), UX (6.3)
- **Problem:** The impact card CTA on the main map page uses `target="_blank"` which opens the Financial Impact page in a new tab; on mobile this creates a confusing navigation fork; the CTA is also styled as plain amber text with no button shape, making it look like a footnote rather than a call-to-action.
- **Exact fix:** In `index.html`, find the impact card CTA anchor tag. Remove `target="_blank"` and restyle it as a bordered button:
```js
`<a href="/impact" ` +
   `style="display:inline-block;font-family:'DM Mono',monospace;font-size:0.6rem;` +
          `letter-spacing:0.12em;text-transform:uppercase;color:#f97316;` +
          `text-decoration:none;border:1px solid rgba(249,115,22,0.35);` +
          `padding:7px 14px;margin-top:4px;` +
          `background:rgba(249,115,22,0.08);">` +
  `See Financial Impact Report →` +
`</a>`
```
- **Files:** `frontend/index.html`
- **Effort:** Small

---

**A24**
- **Priority:** P1
- **Agents:** Data Integrity (Issue 1), UX (1.1)
- **Problem:** The hero headline number and the index.html impact card both use a spaced em-dash (`$36B — $40B`) while all other appearances use an en-dash (`$36B – $40B`); the inconsistency is visible and the em-dash can be misread as a subtraction sign.
- **Exact fix:**
  1. In `impact.html`, find the `.headline-number` div containing `$36B — $40B` and change to `$36B&thinsp;&ndash;&thinsp;$40B`
  2. In `index.html`, find the JS string containing `$36B — $40B` in the impact card injection and change to `$36B&thinsp;&ndash;&thinsp;$40B`
- **Files:** `frontend/impact.html`, `frontend/index.html`
- **Effort:** Small

---

**A25**
- **Priority:** P1
- **Agents:** Data Integrity (Issue 2)
- **Problem:** The comparison bar in `impact.html` shows Milliman as `$25B – $39B` while `methodology.html` (the authoritative source) states `$25.2B–$39.4B`; the rounded version understates the upper bound by $0.4B.
- **Exact fix:** In `impact.html`, find the bar label for Milliman in the comparison chart and change `$25B – $39B` to `$25.2B – $39.4B`.
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A26**
- **Priority:** P1
- **Agents:** Data Integrity (Issue 6)
- **Problem:** `impact.html` calls the three figures "Estimate 01/02/03" throughout, while `methodology.html` uses "Number 1/2/3" as section headings; a reader following the link from the impact page to the methodology page must mentally remap the nomenclature.
- **Exact fix:** In `methodology.html`, change the three H2 section headings from `Number 1`, `Number 2`, `Number 3` to `Estimate 01 — Direct Property Destruction`, `Estimate 02 — Property Value Impact`, `Estimate 03 — Acute Smoke Health Cost` to match `impact.html`'s terminology.
- **Files:** `frontend/methodology.html`
- **Effort:** Small

---

**A27**
- **Priority:** P1
- **Agents:** UX (3.1), Data Integrity (Section 3)
- **Problem:** The map has no persistent info control showing data sources, vintage dates, or what each layer represents; a reader looking at the map cold has no context for the fire perimeters, smoke plumes, or PM2.5 counties.
- **Exact fix:** Add a positioned Leaflet info control to `impact.html` in the `<script>` block after `fireLayer.addTo(map)`:
```js
const infoControl = L.control({ position: 'bottomleft' });
infoControl.onAdd = function() {
  const div = L.DomUtil.create('div');
  div.innerHTML = `
    <div style="background:rgba(4,4,10,0.95);border:1px solid rgba(249,115,22,0.22);
                padding:10px 13px;font-family:'DM Mono',monospace;font-size:0.58rem;
                color:#7a7a92;letter-spacing:0.04em;line-height:1.7;max-width:220px;">
      <div style="color:#f97316;margin-bottom:5px;letter-spacing:0.14em;
                  text-transform:uppercase;font-size:0.52rem;">Data Sources</div>
      <div>&#x25A0; Fire Perimeters — CAL FIRE, Feb 5 2025 (approximate)</div>
      <div>&#x25A0; Smoke Plumes — NOAA HMS</div>
      <div>&#x25A0; PM2.5 — EPA AQS, Jan 9 2025</div>
    </div>`;
  return div;
};
infoControl.addTo(map);
```
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A28**
- **Priority:** P1
- **Agents:** SciComm (5.1), Data Integrity (Issue 7), Skeptic (5.5)
- **Problem:** The Sathaye et al. (2024) citation in `methodology.html` lacks volume, issue, page number, and DOI; a journalist on deadline cannot follow up on the citation as written, and without a DOI, the confidence interval on the 2.2% finding cannot be verified.
- **Exact fix:** This is a two-part fix. First, confirm the actual DOI and publication details for the Sathaye et al. paper (this is a research task, not a code task). Second, once confirmed, update `methodology.html` to include the full citation including DOI. As an interim measure before the DOI is confirmed, add a visible placeholder:
```html
<p>Sathaye et al. (2024), <em>Landscape and Urban Planning</em> —
"Climate change and real estate markets: An empirical study of the impacts of wildfires
on home values in California."
<strong style="color:var(--amber);">[DOI pending confirmation — add before public launch]</strong></p>
```
- **Files:** `frontend/methodology.html`
- **Effort:** Medium (requires external research to confirm DOI)

---

**A29**
- **Priority:** P1
- **Agents:** UX (2.3), Skeptic (2.1)
- **Problem:** The comparison chart section subtitle "Published Estimates from Independent Sources" implies SmokeStory is a peer-institution of Moody's and Milliman, which it explicitly disclaims; this is a framing vulnerability that critics or fact-checkers will exploit.
- **Exact fix:** In `impact.html`, find the `.section-subtitle` or heading of the comparison section and change it from "Published Estimates from Independent Sources" (or equivalent) to "How This Estimate Compares to Other Published Figures." Also add a `chart-note` line: `Note: These estimates measure different scopes — Moody's and Milliman measure insured losses only; SmokeStory and UCLA Anderson measure broader market value. Direct comparison requires understanding these differences.`
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A30**
- **Priority:** P1
- **Agents:** Skeptic (6.1)
- **Problem:** "29 Lives Lost" has no date qualifier; wildfire death tolls are often revised upward, and indirect deaths from smoke exposure are not included; if the figure is later revised, the uncaveated number on the page will look like a deliberate undercount.
- **Exact fix:** In `impact.html`, change `29 Lives Lost` in the hero stats to `29 Confirmed Deaths (as of Feb 5, 2025)` and add a tooltip or adjacent fine print: `Direct fire fatalities only — does not include indirect deaths from smoke exposure or evacuation-related mortality.`
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A31**
- **Priority:** P1
- **Agents:** SciComm (5.2), SciComm (5.4)
- **Problem:** "CAR 2024" appears without expansion in the methodology page's highlight box headers and sources table; "DINS" is used without expansion; "CHIS 2021-2022" is unexpanded — all three are opaque to journalists who are not industry insiders.
- **Exact fix:** In `methodology.html`:
  1. Replace `Structure Counts — CAL FIRE DINS, February 5, 2025` with `Structure Counts — CAL FIRE Damage Inspection System (DINS), February 5, 2025`
  2. Replace `<li>DINS counts subject to revision</li>` with `<li>CAL FIRE Damage Inspection (DINS) counts are subject to revision as field assessments are updated</li>`
  3. Replace `<td class="source-name">CHIS 2021–2022</td>` / `<td>Asthma population</td>` / `<td class="source-access">public UCLA CHIS</td>` with `<td class="source-name">California Health Interview Survey (CHIS) 2021–2022</td>` / `<td>LA County asthma prevalence estimate (450,000 patients)</td>` / `<td class="source-access">public — healthpolicy.ucla.edu/chis</td>`
- **Files:** `frontend/methodology.html`
- **Effort:** Small

---

### P2 — Nice to Have

---

**A32**
- **Priority:** P2
- **Agents:** UX (1.2)
- **Problem:** No visual cue establishes that the three cards are subordinate to and expanding upon the headline number; a first-time reader may think there are four separate estimates.
- **Exact fix:** Add an eyebrow label above the cards grid in `impact.html`:
```html
<div class="cards-section">
  <div style="font-family:var(--mono);font-size:0.58rem;letter-spacing:0.26em;
              text-transform:uppercase;color:var(--text-muted);margin-bottom:20px;
              padding-bottom:14px;border-bottom:1px solid var(--border);">
    Three Independent Estimates &mdash; Each Measures Something Different
  </div>
  <div class="cards-grid">
```
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A33**
- **Priority:** P2
- **Agents:** UX (2.2)
- **Problem:** After the headline number block, the page moves directly into abstract financial cards with no connective tissue explaining why these three types of estimates exist.
- **Exact fix:** Add a one-sentence bridge paragraph between the `.headline-section` and `.cards-section` in `impact.html`:
```html
<div style="font-family:var(--sans);font-size:0.85rem;font-weight:300;
            color:var(--text-dim);line-height:1.75;text-align:center;
            max-width:560px;margin:0 auto 40px;">
  Insurance companies count what was insured. Economists count broader market losses.
  SmokeStory adds what neither measures: the health cost of the smoke itself.
  Three lenses on the same disaster — each valid, none additive.
</div>
```
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A34**
- **Priority:** P2
- **Agents:** UX (1.4)
- **Problem:** All three cards are identical in visual weight; Card 01 carries the headline figure and represents the primary story estimate but is indistinguishable from Cards 02 and 03.
- **Exact fix:** Add a "Headline Estimate" badge and subtle amber background tint to Card 01 in `impact.html`:
```html
<div class="estimate-card" style="background:rgba(249,115,22,0.06);border-left:4px solid var(--amber);">
  <div class="card-label">Estimate 01</div>
  <div class="card-badge" style="background:rgba(249,115,22,0.18);border-color:rgba(249,115,22,0.5);color:var(--amber);">
    Headline Estimate
  </div>
```
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A35**
- **Priority:** P2
- **Agents:** UX (5.2), Journalist (5)
- **Problem:** The methodology link in the disclaimer section is at low opacity (0.65) and there are no inline methodology links within the expanded card detail sections; engaged readers who expand a card to read detail must scroll all the way to the bottom to find the link.
- **Exact fix:**
  1. Increase methodology link opacity: `.methodology-link { opacity: 0.8; font-size: 0.62rem; }`
  2. Add a `Full methodology →` link inside each card-detail section after the source citation, pointing to the corresponding anchor (`/methodology#estimate-01`, `/methodology#estimate-02`, `/methodology#estimate-03`).
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A36**
- **Priority:** P2
- **Agents:** Skeptic (2.3), Journalist (3)
- **Problem:** The $175B housing stock estimate for Estimate 02 is presented as a near-precise input with no error bound; if it is off by 20% (plausible given Prop 13 assessor lag and Zillow AVM error rates), Estimate 02 shifts from $3.9B to $3.1B–$4.7B.
- **Exact fix:** In `impact.html` Card 02, change the description of the housing stock from `roughly 75,000 homes within 5 miles of these fires, worth about $175B combined` to `roughly 75,000 homes within 5 miles of these fires, worth an estimated $175B combined (±20% — see methodology for detail)`. In `methodology.html`, under Estimate 02 Assumptions, add: `A4 — $175B housing stock ±20% uncertainty range. Input derived from LA County Assessor parcel data (subject to Proposition 13 lag) and Zillow AVM (median error ~6-7% for off-market homes). Estimate 02 output range under this uncertainty: $3.1B–$4.7B.`
- **Files:** `frontend/impact.html`, `frontend/methodology.html`
- **Effort:** Small

---

**A37**
- **Priority:** P2
- **Agents:** Skeptic (5.4)
- **Problem:** The 5-mile radius used for Estimate 02 is described as a "product simplification" in the methodology page, not derived from the Sathaye et al. study's actual geographic specification; if the study used a narrower radius, applying 2.2% to a 5-mile zone overstates the affected stock.
- **Exact fix:** In `methodology.html`, under Estimate 02 Assumptions, expand the 5-mile radius note to: `5-mile radius is a product simplification. The Sathaye et al. study uses [confirm the study's geographic threshold]. If the study's specification is narrower than 5 miles, this estimate may overstate the affected housing stock. [Confirm and update before public launch.]`
- **Files:** `frontend/methodology.html`
- **Effort:** Small

---

**A38**
- **Priority:** P2
- **Agents:** UX (1.1), UX (4.2)
- **Problem:** The house emoji in the impact card eyebrow label (`🏠 Estimated Property Impact`) breaks the design system's restrained monospace aesthetic.
- **Exact fix:** In `index.html`, find the impact card JS string containing `🏠 Estimated Property Impact` and remove the emoji: `Estimated Property Impact`
- **Files:** `frontend/index.html`
- **Effort:** Small

---

**A39**
- **Priority:** P2
- **Agents:** UX (3.3)
- **Problem:** The map height at 50vh with a 320px minimum is cramped on mobile; both fires are ~35 miles apart and at zoom 10 a 320px tall map cannot show both in frame simultaneously.
- **Exact fix:** In `impact.html`, change the map height CSS:
```css
#impact-map {
  height: 55vh;
  min-height: 380px;
}
```
And update the default zoom from 10 to 9 with a slightly east-shifted center: `center: [34.13, -118.35], zoom: 9`
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A40**
- **Priority:** P2
- **Agents:** UX (6.2)
- **Problem:** On mobile, the Leaflet layer control stays open (not collapsed), occupying about a third of the map's usable width on a 375px screen.
- **Exact fix:** In `impact.html`'s `<script>` block, change the layer control initialization to collapse on mobile:
```js
const isMobile = window.innerWidth < 640;
let layerControl = L.control.layers(null, overlays, {
  position: 'topright',
  collapsed: isMobile
}).addTo(map);
```
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A41**
- **Priority:** P2
- **Agents:** UX (5.3), Journalist (5)
- **Problem:** The impact page is only discoverable by selecting the specific LA County + January 9, 2025 combination; there is no persistent navigation link to `/impact` from the main page for users who arrive without that context.
- **Exact fix:** Add a small "Featured Analysis" block to the `#welcome-view` panel in `index.html` that provides a direct link to `/impact` regardless of selected county and date.
- **Files:** `frontend/index.html`
- **Effort:** Small

---

**A42**
- **Priority:** P2
- **Agents:** SciComm (3.2)
- **Problem:** "Quasi-experimental spatial panel models with propensity score matching" is unexplained academic jargon in the methodology page that will be opaque to journalists and policymakers.
- **Exact fix:** In `methodology.html`, after the sentence about the method, add: `In plain terms: the researchers compared home sale prices in neighborhoods near wildfires to comparable neighborhoods that were not near wildfires, controlling for other factors that affect price, to isolate the fire's specific effect on value.`
- **Files:** `frontend/methodology.html`
- **Effort:** Small

---

**A43**
- **Priority:** P2
- **Agents:** UX (3.4)
- **Problem:** When the map loads, `smokeLayer` and `pm25Layer` fetch asynchronously; if the API is slow, readers see only "Fire Perimeters" in the layer control and may conclude those layers don't exist.
- **Exact fix:** Add a loading note below the map in `impact.html`:
```html
<div id="map-loading-note" style="font-family:var(--mono);font-size:0.58rem;
     color:var(--text-muted);margin-top:8px;letter-spacing:0.06em;">
  Loading smoke and air quality layers...
</div>
```
Hide it after both layers are loaded in the `updateLayers()` function.
- **Files:** `frontend/impact.html`
- **Effort:** Small

---

**A44**
- **Priority:** P2
- **Agents:** Journalist (4)
- **Problem:** There is no PDF export, static archive link, or DOI-style permalink; if the page changes after a journalist cites it, they have no way to document what it said at the time of citation; "Version 3.0" exists on methodology.html but has no release date.
- **Exact fix:** Add a "Download methodology as PDF" link and a GitHub "view source at this commit" link on `methodology.html`. At minimum, add the Version 3.0 release date to the version label. A full static archive is Medium effort.
- **Files:** `frontend/methodology.html`
- **Effort:** Medium

---

**A45**
- **Priority:** P2
- **Agents:** Skeptic (5.6)
- **Problem:** The Estimate 03 methodology uses a uniform PM2.5 exposure assumption across 4.2M people, but wildfire PM2.5 exposure is spatially heterogeneous; this is noted in methodology.html's assumptions but not explicitly stated in the limitations as a distinct item.
- **Exact fix:** In `methodology.html`, under Estimate 03 Limitations, add: `Spatial variation in PM2.5 exposure is not modeled. Communities immediately adjacent to fire perimeters likely experienced substantially higher concentrations than the 44.8 µg/m³ county average. This uniform-exposure assumption may understate peak health impacts for the most-exposed population while overstating for the least-exposed.`
- **Files:** `frontend/methodology.html`
- **Effort:** Small

---

## QUICK WINS

All Small-effort P0 and P1 items that a developer can knock out in a single session (approximately 2–4 hours total):

| ID | Priority | Fix | File(s) |
|----|----------|-----|---------|
| A1 | P0 | Remove "Claude AI" from data sources footer | impact.html, methodology.html |
| A2 | P0 | Add author name and contact email to disclaimer section | impact.html, methodology.html |
| A3 | P0 | Restyle disclaimer section with amber border, higher contrast, expanded "why" text | impact.html |
| A4 | P0 | Change `<title>` and `<h1>` from "Financial Impact" to "Economic Cost Estimates" | impact.html |
| A5 | P0 | Move headline-note above headline-number; add "preliminary" tag under number | impact.html |
| A6 | P0 | Remove "Claude AI" from index.html footer | index.html |
| A7 | P0 | Add "approximate boundary" disclaimer to map section subtitle and tooltips | impact.html |
| A8 | P0 | Rewrite COI vs VSL assumption in methodology page with accurate explanation | methodology.html |
| A9 | P0 | Move Card 03 category warning to top of expanded detail; add mortality exclusion note | impact.html |
| A10 | P0 | Fix work-loss days (691,464 → 691,656), restricted-activity days (1,082,016 → 1,082,592), base total ($546M → $546.2M) | methodology.html |
| A11 | P1 | Add "Data as of: February 5, 2025" line to impact.html; add release date to Version 3.0 in methodology.html | impact.html, methodology.html |
| A12 | P1 | Expand CAR 2024 citation; add author name to Card 02 source line | methodology.html, impact.html |
| A13 | P1 | Add explanation and caveat for 4% demand surge in card detail and methodology | impact.html, methodology.html |
| A14 | P1 | Add "Not Additive" badges to Cards 01 and 03 | impact.html |
| A15 | P1 | Rename "SmokeStory Unique Contribution" badge to "Not in Other Published LA Wildfire Estimates (as of Feb 2025)" | impact.html |
| A16 | P1 | Change Card 01 title to "Destroyed Buildings"; add exclusions note to description | impact.html |
| A17 | P1 | Change Card 02 title to "Drop in Value: Homes Near the Fire Zones" | impact.html |
| A18 | P1 | Add "(unrealized)" after $3.9B; expand paper loss description | impact.html |
| A19 | P1 | Add 2.2% historical average caveat to Card 02 expanded detail | impact.html |
| A20 | P1 | Explain $36B → $40B upper bound mechanism in Card 01 expanded detail | impact.html |
| A21 | P1 | Explain $0.5B–$1.0B range drivers in Card 03 expanded detail | impact.html |
| A22 | P1 | Revise "same method the EPA uses" language; add wildfire PM2.5 toxicity note | impact.html |
| A23 | P1 | Remove `target="_blank"` from impact card CTA; restyle as button | index.html |
| A24 | P1 | Standardize all headline number dashes to en-dash with thin spaces | impact.html, index.html |
| A25 | P1 | Fix Milliman range on comparison bar from `$25B–$39B` to `$25.2B–$39.4B` | impact.html |
| A26 | P1 | Rename methodology.html section headings from "Number 1/2/3" to "Estimate 01/02/03" | methodology.html |
| A27 | P1 | Add Leaflet info control with data source provenance to map | impact.html |
| A29 | P1 | Relabel comparison chart section as "How This Estimate Compares to Other Published Figures" | impact.html |
| A30 | P1 | Change "29 Lives Lost" to "29 Confirmed Deaths (as of Feb 5, 2025)" with indirect mortality note | impact.html |
| A31 | P1 | Expand DINS, CHIS acronyms in methodology page | methodology.html |

---

## FINAL SUMMARY

### Is the page ready to share with journalists?

**No — not yet. Estimated status: "Almost" with approximately 3–4 hours of developer work remaining.**

The page is substantially more credible than most independent project dashboards and would survive scrutiny from a sympathetic reader. However, two issues are hard stops for any professional journalist: the "Claude AI" attribution alongside federal agencies (A1/A6) and the absence of any named author or contact information (A2). No editor will allow a reporter to cite an unattributed page with an AI listed as a scientific data source. These two items can be fixed in under 30 minutes.

Beyond those two stops, five additional P0 issues must be resolved before press outreach: the page title/framing (A4), the headline-note positioning and "preliminary" tag (A5), the map perimeter disclaimer (A7), the COI/VSL methodology explanation (A8), and the mortality exclusion disclosure on Card 03 (A9). The calculation errors in the methodology page (A10) must also be corrected before any fact-checker reviews the work.

### The 3 Most Important Things to Fix First

1. **Remove "Claude AI" from the data sources footer and add a named author with contact email (A1, A2, A6).** These are the single biggest credibility barriers to press coverage. A journalist cannot cite an unattributed page. An editor cannot approve a story sourcing an AI as a data peer of NOAA and EPA. Both fixes are under 15 minutes of work each.

2. **Reframe the page title and hero to make clear this is not a total economic cost (A4, A5).** The current "Financial Impact" framing and the visual dominance of $36B–$40B invites exactly the misquotation that would undermine the project's credibility: "SmokeStory says fires cost $40 billion." The page actually says something more careful and interesting, and the framing should reflect that.

3. **Fix the disclaimer contrast, expand the "why you can't add these" explanation, and add the mortality exclusion note to Card 03 (A3, A9).** These three items transform the page's relationship with a critical reader from "I see warnings buried in fine print" to "this project clearly understands the risks of misuse and is taking them seriously." The current fine-print treatment signals legal cover-your-ass, not scientific integrity.

### What Is Working Well and Should NOT Be Changed

- **The comparison chart (Moody's vs. Milliman vs. SmokeStory vs. UCLA Anderson).** This is the best element on the page. The SciComm reviewer called it "the best-executed piece of science communication on the page." The Journalist called it "the most useful element on the page for a journalist." The Data Integrity audit confirmed the bar proportions are mathematically correct. Do not restructure this section — only update the subtitle framing (A29) and add the chart-note clarification.

- **The three-card structure with explicit separation.** The decision to show three separate estimates with explicit "Separate — Not Additive" labeling is rare and responsible. The Journalist reviewer specifically praised the "must not be added together" warning as something "most advocacy sites would happily let readers do." Preserve the structure; only improve the visual weight and placement of the warning.

- **The methodology page's arithmetic transparency.** Showing the full multiplication chain ($22.61B + $13.42B = $36.03B) is a trust signal that almost no independent project provides. The Data Integrity audit confirmed all major calculations are correct. Do not simplify or hide this — it is what gives the page credibility with expert readers.

- **The "How We Calculated This" expand panels.** The instinct to provide auditable methodology at the card level is correct. The fix is not to remove these but to improve the expand-button affordance (UX 2.4, but that is P2) and to ensure the most critical caveats appear in the visible card text, not only in the collapsed section.

- **The dark-glass aesthetic and typographic system.** The premium design builds credibility. The UX reviewer noted it is "cohesive" and "the dark-glass aesthetic is credible." Do not redesign. Small fixes to contrast ratios and border weights (A3) are within the design system, not departures from it.

### Estimated Total Effort to Reach "Ready to Share" State

- **P0 items (A1–A10):** 10 items, all Small effort except A10 which is Small-Medium. Estimated: **2–3 hours** of developer time.
- **P1 items (A11–A31):** 21 items, all Small effort except A28 (Medium — requires external DOI research). Developer-side code changes: **3–5 hours**. External research task (Sathaye et al. DOI, 4% demand surge citation, CAR specific report URL): **1–2 hours** of research time.

**Total to "ready to share": approximately 6–8 hours of combined developer and researcher time.**

The P2 items are genuine polish and discoverability improvements but none is a blocker for a journalist-ready state. They represent an additional 4–6 hours if prioritized.

---

*All file paths referenced are absolute: `/Users/tinahuang/Desktop/smokestory/frontend/impact.html`, `/Users/tinahuang/Desktop/smokestory/frontend/methodology.html`, `/Users/tinahuang/Desktop/smokestory/frontend/index.html`.*
