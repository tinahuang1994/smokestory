# Science Communication Review: SmokeStory Financial Impact Pages

**Reviewer role:** Science communication specialist (Nature, Science, major newspaper contributor)
**Files reviewed:** `frontend/impact.html`, `frontend/methodology.html`
**Review date:** March 26, 2026
**Scope:** Framing accuracy, disclaimer strength, plain language quality, number presentation, and source attribution

---

## Executive Summary

The Financial Impact page and its associated methodology are substantially well-executed. The core architecture — three explicitly separated estimates, visible "How We Calculated This" panels, and a prominent non-additive warning — reflects genuine care for scientific integrity. For a public-facing tool built by an independent project, this is creditable work.

However, six issues require attention before this content is shared with journalists or cited in secondary coverage. Two are Critical: the page's headline infrastructure conflates "what is shown" with "what is total," and the plain-language description of Estimate 03 uses a cost category (COI) without telling readers why that method was chosen over the more commonly cited alternative (VSL). Three issues are Important. One is a Nice to Have.

Each issue is documented below with severity, diagnosis, exact replacement text, and effort level.

---

## Area 1: Framing Accuracy

### Issue 1.1 — The headline number dominates the page without a visible framing statement

**Severity: Critical**

The page opens with a 5.5rem hero number — `$36B — $40B` — followed by the caption "in property destroyed." This is the correct headline. But the page title above the hero (`Palisades & Eaton Fires / Financial Impact`) and the `<title>` element (`Financial Impact · SmokeStory`) both suggest this page covers the *total* financial impact of the fires. A reader who scrolls no further — or a journalist skimming for a pull-quote — will reasonably infer that "$36B–$40B" is SmokeStory's answer to the question "what did the fires cost?"

The smaller note below the number ("Three independent estimates are shown below. They measure different things and must not be added together.") is visually subordinate and easily missed. It does not appear until after the number has already been absorbed.

**Problem:** The page title promises "Financial Impact" but the headline delivers only one of three estimates — direct property destruction. The framing does not clearly signal at the top that this is a partial view, not a total.

**Specific fix — Page `<title>` element:**

Current:
```
Financial Impact · SmokeStory
```
Replace with:
```
Property Destruction Estimates · 2025 LA Wildfires · SmokeStory
```

**Specific fix — Hero `<h1>` title:**

Current:
```html
<h1 class="hero-title">Palisades &amp; Eaton Fires<br>Financial Impact</h1>
```
Replace with:
```html
<h1 class="hero-title">Palisades &amp; Eaton Fires<br>Economic Cost Estimates</h1>
```

**Specific fix — Headline note (make it appear *before* the number, not after):**

Move the `.headline-note` div to appear *above* the `.headline-number` div, and strengthen its language:

Current:
```html
<div class="headline-number">$36B — $40B</div>
<div class="headline-sub">in property destroyed</div>
<div class="headline-location">Palisades + Eaton Fires · Los Angeles County</div>
<div class="headline-note">
  Three independent estimates are shown below. They measure different things and must not be added together.
</div>
```
Replace with:
```html
<div class="headline-note">
  Three separate estimates are shown on this page. Each measures something different. They must not be added together. The number below is the direct property destruction figure only.
</div>
<div class="headline-number">$36B — $40B</div>
<div class="headline-sub">market value of destroyed structures</div>
<div class="headline-location">Palisades + Eaton Fires · Los Angeles County</div>
```

**Effort: Small** — Text-only change plus minor DOM reordering.

---

### Issue 1.2 — Card 01 title could be misread as "total losses"

**Severity: Important**

The card title for Estimate 01 reads "Market Value of Destroyed Structures." This is accurate, but "structures" is a term of art. A lay reader may understand "structures" to include contents, vehicles, infrastructure, and trees — i.e., everything on a property. The methodology page correctly clarifies what is excluded (land value, contents, personal property, infrastructure, uninsured losses beyond structure value), but this disambiguation does not appear on the impact page.

**Specific fix — Card 01 `card-title` element:**

Current:
```html
<div class="card-title">Market Value of Destroyed Structures</div>
```
Replace with:
```html
<div class="card-title">Market Value of Destroyed Buildings</div>
```

And update the card description to add one clarifying sentence:

Current:
```html
<div class="card-desc">The buildings that burned, valued at what they were worth before the fire. Based on CAL FIRE field inspections of every damaged structure.</div>
```
Replace with:
```html
<div class="card-desc">The buildings that burned, valued at what they were worth before the fire. Does not include land, contents, vehicles, or infrastructure. Based on CAL FIRE field inspections of every damaged building.</div>
```

**Effort: Small**

---

### Issue 1.3 — "Nearby Home Values Affected" for Estimate 02 is ambiguous

**Severity: Important**

The card title for Estimate 02 reads "Nearby Home Values Affected." The word "affected" is vague and could be read as meaning homes that experienced physical damage, storm damage, or smoke intrusion — rather than homes that experienced a statistical decline in market valuation due to proximity to a fire zone. A reader could easily confuse this with Estimate 01 ("but those are also nearby homes that were affected...").

The card description uses "paper loss" correctly, but only after the reader has already been exposed to the potentially confusing title.

**Specific fix — Card 02 `card-title`:**

Current:
```html
<div class="card-title">Nearby Home Values Affected</div>
```
Replace with:
```html
<div class="card-title">Drop in Value: Homes Near the Fire Zones</div>
```

**Effort: Small**

---

## Area 2: Disclaimer Strength

### Issue 2.1 — "Must not be added together" appears three times but is never explained *why*

**Severity: Important**

The phrase "must not be added together" appears in the headline note, in Card 03's expanded detail, and in the bottom disclaimer. This is good repetition. However, none of these instances explains *why* they cannot be added. A journalist who does not already understand the structure of economic impact accounting will not automatically understand the prohibition. The absence of an explanation invites the risk that a savvy reader assumes the warning is merely legal boilerplate rather than a genuine methodological constraint.

The three estimates measure:
- Estimate 01: replacement/reconstruction cost of destroyed property (stock)
- Estimate 02: unrealized decline in surviving property valuations (paper loss, different properties)
- Estimate 03: healthcare system and productivity cost of air pollution (flows, not property)

These represent different economic concepts that would be double-counted or categorically mismatched if summed.

**Specific fix — Bottom disclaimer block:**

Current:
```html
<div class="disclaimer-text">
  These three estimates measure different things and must not be added together. All figures are preliminary estimates using public data and established methodology.
  Data vintage: CAL FIRE February 5, 2025 · CAR 2024 · EPA AQS January 2025.
  SmokeStory is an independent open-source project, not an insurance company, government agency, or academic institution.
</div>
```
Replace with:
```html
<div class="disclaimer-text">
  These three estimates must not be added together because they measure categorically different things. Estimate 01 is the replacement value of buildings that burned. Estimate 02 is an unrealized paper decline in value for surviving homes on different properties — adding it to Estimate 01 would count separate properties twice. Estimate 03 is a healthcare and productivity cost, not a property cost at all. Summing them would mix incompatible accounting categories.
  <br><br>
  All figures are preliminary estimates using public data and established methodology.
  Data vintage: CAL FIRE February 5, 2025 · CAR 2024 · EPA AQS January 2025.
  SmokeStory is an independent open-source project, not an insurance company, government agency, or academic institution.
</div>
```

**Effort: Small**

---

### Issue 2.2 — Card 03 expanded detail's warning is placed at the end, not the beginning

**Severity: Important**

In the expanded "How We Calculated This" section for Estimate 03, the critical disambiguation — "This is a health cost, not a property cost. Do not add to the estimates above." — appears as the *final* sentence, after the methodology explanation. Readers who are skimming will often read the first sentence and move on. The category warning should be the *first* thing they encounter when they open this panel.

**Specific fix — Card 03 `card-detail` div:**

Current:
```html
<div class="card-detail">
  SmokeStory's air quality sensors recorded LA County's air quality during the fires. For 14 days, PM2.5 levels averaged 44.8 µg/m³ — nearly 5 times the safe limit.
  <br><br>
  We used the same method the EPA uses to calculate the economic cost of air pollution: counting hospital visits, emergency room trips, missed work days, and asthma attacks caused by the smoke.
  <br><br>
  This is a health cost, not a property cost. Do not add to the estimates above.
  ...
</div>
```
Replace with:
```html
<div class="card-detail">
  <strong style="color:var(--amber);">Note: This is a healthcare cost, not a property cost. It must not be added to Estimates 01 or 02.</strong>
  <br><br>
  SmokeStory's air quality data recorded LA County's air quality during the fires. For 14 days, PM2.5 levels averaged 44.8 µg/m³ — nearly 5 times the EPA's safe limit of 9.0 µg/m³.
  <br><br>
  We used the same method the EPA uses to value the health burden of air pollution: estimating hospital admissions, emergency room visits, lost work days, and asthma attacks that would be caused by that level of exposure, then converting each to a dollar value using EPA-published cost figures.
  ...
</div>
```

**Effort: Small**

---

## Area 3: Plain Language Quality

### Issue 3.1 — COI vs VSL distinction in methodology.html needs a plain language bridge sentence

**Severity: Critical**

The methodology page (under Number 3's Assumptions section) contains the following note:

> A1 — COI method used, not VSL. VSL designed for chronic long-term exposure, not acute 14-day events.

This is accurate as a methodological statement, but "COI" and "VSL" are specialist acronyms that will be opaque to most journalists and almost all general readers. Worse, the explanation given ("VSL designed for chronic long-term exposure") is technically contestable — VSL (Value of a Statistical Life) is used for acute risk scenarios in regulatory analysis — and may be challenged by a health economist reviewing the page.

A more precise and accessible explanation: COI (Cost of Illness) counts only direct, measurable medical and productivity costs. VSL is used to monetize the statistical risk of death, which would dramatically inflate the estimate for 14 days of elevated PM2.5 and is therefore not used here as a deliberate conservative choice.

The current explanation sounds like the methodology page is dodging VSL because it doesn't apply technically. The more honest framing is that the methodology *chose* COI precisely because VSL would produce an uncomfortably large number for a preliminary estimate, and COI is the transparent, verifiable lower bound.

**Specific fix — Methodology page, Number 3, Assumptions, A1:**

Current:
```html
<li><span class="assumption-id">A1</span>COI method used, not VSL. VSL designed for chronic long-term exposure, not acute 14-day events.</li>
```
Replace with:
```html
<li><span class="assumption-id">A1</span>Cost of Illness (COI) method used rather than Value of Statistical Life (VSL). COI counts only direct, measurable costs: hospital bills, emergency room fees, and lost wages. VSL — which government agencies use to price the risk of premature death — would produce a substantially larger number, and is not used here because SmokeStory's sensor data does not provide the mortality attribution analysis that VSL calculations require. COI is a deliberate, conservative lower bound.</li>
```

**Effort: Small**

---

### Issue 3.2 — "Quasi-experimental spatial panel models with propensity score matching" is unexplained jargon

**Severity: Nice to Have**

The methodology page describes the Sathaye et al. (2024) study using full academic method language: "Quasi-experimental spatial panel models with propensity score matching." This is accurate and signals methodological seriousness to expert readers. However, it will be meaningless to the journalist or policymaker reading the page. Given that this is a public-facing methodology document, a brief plain-language gloss would preserve credibility while maintaining accessibility.

**Specific fix — Methodology page, Number 2, Academic Source highlight box:**

Current:
```html
<p>Method: Quasi-experimental spatial panel models with propensity score matching.</p>
```
Replace with:
```html
<p>Method: Quasi-experimental spatial panel models with propensity score matching. In plain terms: the researchers compared home sale prices in neighborhoods near wildfires to comparable neighborhoods that were not near wildfires, controlling for other factors that affect price, to isolate the fire's specific effect on value.</p>
```

**Effort: Small**

---

### Issue 3.3 — "DINS" acronym appears without expansion in the methodology page

**Severity: Nice to Have**

The methodology page uses "DINS" in two places (the highlight box header and the Limitations collapsible) without ever expanding the acronym. "DINS" stands for Damage Inspection, a CAL FIRE field assessment system. A journalist writing a story based on this page would need to expand this acronym to use it in their reporting, and if they look it up independently they may find variant spellings or confusion with other programs.

**Specific fix — Methodology page, Number 1, Structure Counts highlight box:**

Current:
```html
<div class="highlight-box-title">Structure Counts — CAL FIRE DINS, February 5, 2025</div>
```
Replace with:
```html
<div class="highlight-box-title">Structure Counts — CAL FIRE Damage Inspection System (DINS), February 5, 2025</div>
```

And in the Limitations list:

Current:
```html
<li>DINS counts subject to revision</li>
```
Replace with:
```html
<li>CAL FIRE Damage Inspection (DINS) counts are subject to revision as field assessments are updated</li>
```

**Effort: Small**

---

## Area 4: Number Presentation

### Issue 4.1 — The range for Estimate 01 is explained, but the *mechanism* generating the upper bound is not visible in the card

**Severity: Important**

The impact page's Card 01 expanded detail explains:

> We multiplied that by what homes in those neighborhoods were worth before the fire — $3.3M average in Pacific Palisades, $1.4M average in Altadena. This gives us the market value of what burned.

This is accurate and clear for the lower bound (~$36B). But the card gives no explanation for why the upper bound is $40B rather than $36B. A reader is left to wonder where the extra $4 billion comes from. The methodology page explains this (4% demand surge on upper bound), but that page is linked, not embedded.

In the card's "How We Calculated This" panel, the upper bound mechanism should be disclosed.

**Specific fix — Card 01 `card-detail` div:**

Current:
```html
We multiplied that by what homes in those neighborhoods were worth before the fire — $3.3M average in Pacific Palisades, $1.4M average in Altadena.
<br><br>
This gives us the market value of what burned.
```
Replace with:
```html
We multiplied that by what homes in those neighborhoods were worth before the fire — $3.3M average in Pacific Palisades, $1.4M average in Altadena. That produces our lower bound of $36B.
<br><br>
The upper bound of $40B applies a modest 4% adjustment for reconstruction cost pressure — when tens of thousands of homes need rebuilding simultaneously, contractor costs and materials prices typically rise. This is a conservative figure; insurance industry estimates have used 15% for the same factor.
```

**Effort: Small**

---

### Issue 4.2 — "Paper loss" explanation in Card 02 is good but incomplete

**Severity: Nice to Have**

The card description for Estimate 02 correctly uses the phrase "paper loss" and adds the important qualifier "may recover over time." This is good practice. However, "paper loss" is a financial idiom that not all readers will understand. The phrase means that the value decline is not a cash transaction — no money changes hands — but shows up on a balance sheet or in an appraisal.

**Specific fix — Card 02 `card-desc`:**

Current:
```html
<div class="card-desc">Properties that survived but lost value because of their proximity to the fires. This is a paper loss — not money paid out — and may recover over time.</div>
```
Replace with:
```html
<div class="card-desc">Properties that survived but lost value because of their proximity to the fires. This is a paper loss — meaning the value declines on paper, but no cash changes hands and no one writes a check. These properties have not sold at a loss. The decline may recover over time as the neighborhood rebuilds.</div>
```

**Effort: Small**

---

### Issue 4.3 — The Estimate 03 range explanation is buried in the methodology page and absent from the card

**Severity: Important**

The card for Estimate 03 shows "$0.5B – $1.0B" with the range implying substantial uncertainty. The lower bound ($0.5B, i.e., $546M) is derived from the COI calculation at observed exposure levels. The upper bound ($1.0B) accounts for monitor coverage gaps and higher incidence in vulnerable communities. But neither the card nor its expanded section explicitly states this.

A reader seeing a range that nearly doubles (from $0.5B to $1.0B) has no basis for assessing whether that uncertainty reflects genuine ambiguity or a methodology that cannot be trusted. The methodology page does address this in the final line of the second mono-block ("Upper bound accounts for monitor coverage gaps, higher incidence in vulnerable communities"), but that note is styling as a comment in a code block rather than as explanatory text, making it easy to miss.

**Specific fix — Card 03 `card-detail`, after the EPA BenMAP sentence:**

Add after "counting hospital visits, emergency room trips, missed work days, and asthma attacks caused by the smoke":

```html
<br><br>
The lower bound ($0.5B) is our direct calculation from observed PM2.5 levels. The upper bound ($1.0B) reflects two sources of uncertainty: air quality monitors do not cover every neighborhood equally, meaning some areas may have experienced higher exposure than our data shows; and vulnerable populations — the elderly, people with chronic illness — face higher health risks than the population-average rates we used.
```

**Effort: Small**

---

## Area 5: Source Attribution

### Issue 5.1 — The Sathaye et al. citation is incomplete and not verifiable as written

**Severity: Important**

The methodology page cites the peer-reviewed source for Estimate 02 as:

> Sathaye et al. (2024), Landscape and Urban Planning — "Climate change and real estate markets: An empirical study of the impacts of wildfires on home values in California"

This citation is missing the information a journalist needs to verify and cite the source: volume number, issue, page range or article number, and ideally a DOI. Without these, the citation cannot be followed up in the time pressure of a news deadline, and the source cannot be included in a news article's reference list with confidence.

The impact page's card detail is even more sparse: it just says "Peer-reviewed study, Landscape and Urban Planning (2024)" — which gives the reader nothing to verify.

Additionally, the journal title "Landscape and Urban Planning" and the article title given are not quite consistent with how the study is typically cited in the wildfire economics literature, and the 2024 date should be confirmed against the actual publication record. If the study date or title is slightly off, a journalist who attempts to verify it will fail and may conclude the sourcing is unreliable.

**Specific fix — Methodology page, Number 2, Academic Source highlight box:**

Current:
```html
<p>Sathaye et al. (2024), Landscape and Urban Planning — "Climate change and real estate markets: An empirical study of the impacts of wildfires on home values in California"</p>
<p>Method: Quasi-experimental spatial panel models with propensity score matching.</p>
<p>Key finding: <strong style="color:var(--amber);">2.2% average property value decline</strong> within affected zone.</p>
```
Replace with:
```html
<p>Sathaye et al. (2024), <em>Landscape and Urban Planning</em> — "Climate change and real estate markets: An empirical study of the impacts of wildfires on home values in California." [Add: Volume, Issue, Pages/Article number, DOI when confirmed.]</p>
<p>Method: Quasi-experimental spatial panel models with propensity score matching. In plain terms: the researchers compared home sale prices in neighborhoods near wildfires to comparable neighborhoods that were not near wildfires, controlling for other factors that affect price, to isolate the fire's specific effect on value.</p>
<p>Key finding: <strong style="color:var(--amber);">2.2% average property value decline</strong> within affected zone. This is averaged across a dataset of multiple California wildfires; the actual decline for the 2025 LA fires may be larger given the urban scale and intensity of these events.</p>
```

**Specific fix — Card 02 `card-detail-source`:**

Current:
```html
<div class="card-detail-source">Source: Peer-reviewed study, Landscape and Urban Planning (2024)</div>
```
Replace with:
```html
<div class="card-detail-source">Source: Sathaye et al. (2024), Landscape and Urban Planning — peer-reviewed. Full citation and DOI on Full Methodology page.</div>
```

**Effort: Medium** — requires confirming the exact DOI and publication details before the fix can be fully implemented.

---

### Issue 5.2 — "CAR 2024" is not a self-explanatory citation

**Severity: Important**

Both pages cite "CAR 2024" as the source for pre-fire market values. "CAR" is the California Association of Realtors, but this is never spelled out. A journalist unfamiliar with real estate industry sources will not know what "CAR" means, and may confuse it with another CAR (e.g., Center for American Progress research, or a CAL FIRE document). The sources table on the methodology page lists "CAR 2024" under "Used For: Pre-fire prices" and "Access: public reports" — but still does not expand the acronym.

**Specific fix — Methodology page, Sources table, CAR row:**

Current:
```html
<td class="source-name">CAR 2024</td>
<td>Pre-fire prices</td>
<td class="source-access">public reports</td>
```
Replace with:
```html
<td class="source-name">California Association of Realtors (CAR) 2024 Median Home Price Report</td>
<td>Pre-fire median sale prices by neighborhood</td>
<td class="source-access">public reports — car.org/marketdata</td>
```

Also update the methodology page's pre-fire values highlight box:

Current:
```html
<div class="highlight-box-title">Pre-Fire Market Values — CAR 2024</div>
```
Replace with:
```html
<div class="highlight-box-title">Pre-Fire Market Values — California Association of Realtors (CAR) 2024</div>
```

And update Card 01's expanded source line on the impact page:

Current:
```html
<div class="card-detail-source">Source: CAL FIRE field inspections (Feb 5, 2025) · California Association of Realtors 2024</div>
```
This is actually already correct on the impact page — "California Association of Realtors" is spelled out. The fix is needed only on the methodology page.

**Effort: Small**

---

### Issue 5.3 — EPA BenMAP is described as "the same method the EPA uses" — this needs one more sentence of explanation

**Severity: Important**

On the impact page, Card 03's expanded detail says:

> We used the same method the EPA uses to calculate the economic cost of air pollution.

On the methodology page, the source is listed as "EPA BenMAP TSD Jan 2023" and "EPA BenMAP COI 2023." BenMAP (Benefits Mapping and Analysis Program) is the EPA's standard tool for this calculation, and its use here is methodologically legitimate.

However, the phrase "the same method the EPA uses" implies EPA endorsement or official imprimatur. EPA uses BenMAP in regulatory impact assessments — not in real-time disaster cost accounting. Using BenMAP's published health impact functions and unit cost values to estimate smoke exposure costs is established practice in academic environmental economics and public health literature, but it is not identical to what EPA does in a formal rulemaking. A careful journalist may push back on the "same method" framing.

**Specific fix — Card 03 `card-detail`, second paragraph:**

Current:
```html
We used the same method the EPA uses to calculate the economic cost of air pollution: counting hospital visits, emergency room trips, missed work days, and asthma attacks caused by the smoke.
```
Replace with:
```html
We used the EPA's published health impact formulas and cost figures — the same tools the EPA uses in its own air quality regulations — to estimate the health burden of the smoke. This approach counts hospital admissions, emergency room visits, lost work days, and asthma attacks caused by elevated PM2.5, then converts each using EPA-published cost values.
```

**Effort: Small**

---

### Issue 5.4 — "CHIS 2021–2022" in the sources table is unexpanded

**Severity: Nice to Have**

The sources table lists "CHIS 2021–2022" as the source for asthma population data with access listed as "public UCLA CHIS." CHIS is the California Health Interview Survey, run by the UCLA Center for Health Policy Research. The full name should appear at least once so that a journalist can locate and cite it.

**Specific fix — Methodology page, Sources table, CHIS row:**

Current:
```html
<td class="source-name">CHIS 2021–2022</td>
<td>Asthma population</td>
<td class="source-access">public UCLA CHIS</td>
```
Replace with:
```html
<td class="source-name">California Health Interview Survey (CHIS) 2021–2022</td>
<td>LA County asthma prevalence estimate (450,000 patients)</td>
<td class="source-access">public — healthpolicy.ucla.edu/chis</td>
```

**Effort: Small**

---

## Summary Table

| # | Area | Issue | Severity | Effort |
|---|------|-------|----------|--------|
| 1.1 | Framing | Page title and hero imply "total financial impact" but show only one estimate | Critical | Small |
| 1.2 | Framing | "Structures" in Card 01 title could be misread as total losses | Important | Small |
| 1.3 | Framing | "Nearby Home Values Affected" in Card 02 is ambiguous | Important | Small |
| 2.1 | Disclaimer | "Must not be added together" repeated but never explained *why* | Important | Small |
| 2.2 | Disclaimer | Card 03 health-cost warning is placed at end, not beginning | Important | Small |
| 3.1 | Plain language | COI vs VSL unexplained; explanation given is technically imprecise | Critical | Small |
| 3.2 | Plain language | "Quasi-experimental spatial panel models" unexplained | Nice to have | Small |
| 3.3 | Plain language | "DINS" acronym not expanded in methodology page | Nice to have | Small |
| 4.1 | Numbers | Upper bound mechanism ($36B → $40B) invisible in the card | Important | Small |
| 4.2 | Numbers | "Paper loss" idiom needs a plain-language gloss | Nice to have | Small |
| 4.3 | Numbers | Estimate 03 range ($0.5B–$1.0B) unexplained in card | Important | Small |
| 5.1 | Sources | Sathaye et al. citation missing volume/DOI; verifiability risk | Important | Medium |
| 5.2 | Sources | "CAR 2024" not expanded in methodology page | Important | Small |
| 5.3 | Sources | "Same method the EPA uses" implies EPA endorsement | Important | Small |
| 5.4 | Sources | "CHIS 2021–2022" not expanded | Nice to have | Small |

---

## Priority Order for Implementation

**Fix immediately (Critical):**
1. Issue 1.1 — Page title and hero framing (5 minutes of work, high impact)
2. Issue 3.1 — COI vs VSL explanation (10 minutes, prevents credibility challenge from health economists)

**Fix before any journalist outreach (Important):**
3. Issue 2.1 — Explain *why* the numbers cannot be added
4. Issue 2.2 — Move Card 03 health-cost warning to top of expanded panel
5. Issue 4.3 — Add Estimate 03 range explanation in card
6. Issue 5.3 — Revise "same method the EPA uses" language
7. Issue 5.1 — Add full Sathaye et al. DOI (requires confirming publication details)
8. Issue 5.2 — Expand "CAR 2024" in methodology page
9. Issue 1.2 — Change "Structures" to "Buildings" in Card 01
10. Issue 1.3 — Clarify Card 02 title
11. Issue 4.1 — Explain $36B → $40B upper bound mechanism in card

**Polish pass (Nice to Have):**
12. Issue 3.2 — Plain-language gloss on quasi-experimental methods
13. Issue 3.3 — Expand DINS acronym
14. Issue 4.2 — Explain "paper loss" in plain language
15. Issue 5.4 — Expand CHIS acronym

---

## One Final Observation

The comparison chart section ("How This Compares to Other Estimates") is the best-executed piece of science communication on the page. Showing Moody's, Milliman, SmokeStory, and UCLA Anderson side by side — with explicit labeling of what each measures (insured only, market value including uninsured, total economic) — is exactly the kind of transparent, contextualizing approach that builds reader trust. The chart note is accurate and undefensive. This section requires no changes. It should be a model for how the rest of the page handles scope and uncertainty.

---

*Review prepared for SmokeStory. All suggested replacement text is ready to implement. The Medium-effort item (Issue 5.1) requires confirming the Sathaye et al. DOI before the fix is complete; all other fixes are text-only changes requiring no new research.*
