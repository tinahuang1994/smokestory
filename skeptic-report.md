# SmokeStory Financial Impact Page — Skeptic & Risk Review

**Reviewer perspective:** Harshest reasonable critic, fact-checker, risk analyst
**Files reviewed:** `frontend/impact.html`, `frontend/methodology.html`
**Date of review:** 2026-03-26
**Scope:** Identify every plausible way this page could be misused, misquoted, or criticized

---

## Executive Summary

The Financial Impact page is largely well-constructed. It explicitly warns multiple times that the three estimates must not be added together, and the methodology page is unusually transparent for a non-academic source. However, there are significant vulnerabilities that a determined critic or a lazy journalist could exploit. The most serious risks are: (1) the $36B–$40B headline figure can easily be de-contextualized, (2) the comparison bar chart has a framing flaw that overstates SmokeStory's position relative to peer firms, (3) Estimate 03 excludes mortality costs without making this prominent enough on the impact page, and (4) the fire perimeters on the map are explicitly hard-coded approximations with no label saying so on the map itself.

---

## Section 1: Misuse Risks

---

### RISK 1.1 — Headline figure misquoted as a total economic loss
**Risk level: HIGH**

The $36B–$40B figure dominates the page visually. It appears in large serif type at 5.5rem, centered, and is the first number a reader sees after the hero section. The caveat that follows — "Three independent estimates are shown below. They measure different things and must not be added together" — is presented in italic small text with a left border, styled as a quiet footnote rather than a warning.

A journalist writing on deadline could reasonably screenshot the headline number and write: *"According to SmokeStory, the LA wildfires caused $40 billion in damage."* This attribution would be technically false (SmokeStory says $36B–$40B in direct property destruction, not total damage), but the page's visual hierarchy invites exactly this misreading.

The hero section also juxtaposes "29 Lives Lost · 150,000 Residents Displaced" directly above the financial section, which emotionally primes readers to read the financial number as a comprehensive toll.

**Fix:** Add a visible, non-italic subheading directly beneath `$36B — $40B` that reads something like: **"Direct property destruction only — not total economic cost."** The current copy says "in property destroyed" in small text beneath the number but this reads as a subtitle, not a limitation. Additionally, the word "preliminary" should appear on the headline number itself, not just in the fine-print disclaimer at the bottom.
**Effort: Small**

---

### RISK 1.2 — Addition of all three estimates to produce a false total of ~$41B
**Risk level: HIGH**

A reader or journalist who skims the three cards might add $36–40B + $3.9B + $0.5–1.0B and report a composite figure of approximately $40–45 billion. The "must not be added together" warning exists in three places: the headline note, Card 3's detail text, and the bottom disclaimer. However, it does not appear as a visible label on Cards 1 and 3, and it is absent between Cards 1 and 2 at the visual level where addition would intuitively occur.

The "Separate — Not Additive" badge on Card 2 is the right instinct, but it is styled in subdued muted-color text and rendered at 0.5rem (very small). Card 1 has no such badge. Card 3 has no such badge.

**Fix:** Add a "Do Not Add" or "Not Additive" badge to Cards 1 and 3 at the same visual level as the badge on Card 2. Consider adding a thin horizontal rule between the cards section and a single-sentence callout in a visually distinct box: "These three numbers are not a sum. Do not add them." This is more actionable than the current italic note.
**Effort: Small**

---

### RISK 1.3 — Estimate 02 ($3.9B) misread as realized cash losses
**Risk level: MEDIUM**

Card 2 includes the phrase "This is a paper loss — not money paid out — and may recover over time." This is good. However, the card number `$3.9B` is displayed at the same visual weight (1.9rem monospace, white) as the other estimates. The "paper loss" qualifier appears only in `card-desc` at 0.75rem in dim text. A reader scanning the three numbers for a quick brief could record $3.9B as a loss on par with the others.

The methodology page (under Number 2 Limitations) says "Paper loss may partially recover," but this is buried inside a collapsed collapsible section that requires a click to view.

**Fix:** Add the phrase "(unrealized)" directly after the number: `$3.9B (unrealized)`. Alternatively, style the number differently — e.g., in a lighter weight or with a tilde prefix `~$3.9B` — to signal it is a different type of figure. Expand the key limitation by default on the impact page (not collapsed).
**Effort: Small**

---

## Section 2: Overstatement Risks

---

### RISK 2.1 — Comparison bar chart misleads by mixing incomparable methodologies
**Risk level: HIGH**

The bar chart in Section 5 places SmokeStory's $36B–$40B directly against Moody's RMS ($20–30B) and Milliman ($25–39B). The chart note explains that Moody's and Milliman measure insured losses only, while SmokeStory measures market value including uninsured losses. However, the visual effect of the chart is that SmokeStory's number looks larger and more comprehensive than the insurance firms', which a reader could interpret as SmokeStory producing a higher, more authoritative estimate.

The deeper problem is that the bar lengths are not proportional to the numbers. The SmokeStory bar is set at `width:29%` while Moody's is at `width:19%`. If the bars were drawn to true scale against a common baseline (say, $0–$170B), SmokeStory at $38B midpoint and Moody's at $25B midpoint would be closer together than the chart implies. The UCLA Anderson bar at `width:100%` representing $95–164B appears roughly 3.5x wider than SmokeStory's bar, but the midpoint ratio is approximately 4x — the UCLA bar is actually slightly undersized relative to the others, making SmokeStory look proportionally bigger.

Additionally, the chart is labeled "Published Estimates from Independent Sources" in the section subtitle. SmokeStory's own estimate appears in this chart as a highlighted row. Calling SmokeStory's estimate a "published estimate from an independent source" alongside Moody's and Milliman implies a parity of institutional credibility that does not exist. SmokeStory explicitly disclaims being an insurance company, government agency, or academic institution.

**Fix:** (a) Make bar widths proportional to actual dollar values against a shared scale, or remove bars entirely and use a simple table. (b) Relabel the section subtitle to something like "How Our Estimate Compares to Published Figures" to make clear SmokeStory is not presenting itself as a peer of Moody's. (c) Add a tooltip or note explaining why comparing these estimates is not straightforward (different scopes, different methods).
**Effort: Medium**

---

### RISK 2.2 — "SmokeStory Unique Contribution" badge on Estimate 03 overstates novelty
**Risk level: MEDIUM**

Card 3 carries the badge "SmokeStory Unique Contribution" in teal styling, which is the most visually distinctive badge on the page. The methodology page reinforces this: "No other published LA wildfire estimate includes smoke health cost."

This claim may be factually accurate at the time of writing, but it is unverified and unfalsifiable as stated. Academic researchers, public health departments, and the EPA itself may have produced or will produce comparable calculations. More importantly, the BenMAP methodology used is a standard EPA tool — any analyst with the same PM2.5 data could reproduce this calculation. Calling it a "unique contribution" implies a degree of original research that may not withstand scrutiny.

Furthermore, the COI (Cost of Illness) methodology is well-documented and relatively mechanical. A fact-checker at a newspaper could reasonably ask: "Is this actually unique, or is it just that SmokeStory was the first to publish it on a webpage?"

**Fix:** Replace "SmokeStory Unique Contribution" with a more defensible badge such as "Smoke Health Cost Estimate" or "Not Included in Other Published Estimates (as of Feb 2025)." Add a date caveat to any uniqueness claim.
**Effort: Small**

---

### RISK 2.3 — The $175B housing stock figure is treated as a known quantity, not an approximation
**Risk level: MEDIUM**

The impact page card for Estimate 02 states the calculation uses "roughly 75,000 homes within 5 miles of these fires, worth about $175B combined." The word "about" is present, which is good. However, the methodology page's mono-block calculation uses `~$175B` and then produces a precise output of `$3.85B`, rounded to `$3.9B`. Displaying a two-significant-figure input alongside a four-significant-figure output implies false precision.

The methodology page notes (under Assumptions, A4) that `$175B housing stock is approximate, derived from LA County Assessor parcel counts and Zillow Research CSV data.` This is adequately caveated — but only for a reader who clicks open the collapsed Assumptions section. The impact page card does not surface this caveat at all beyond the word "about."

A critic could reasonably ask: If the housing stock estimate were off by 20% (a plausible range for an approximation combining two heterogeneous data sources), the Estimate 02 output would shift from $3.9B to $3.1B or $4.7B — a meaningful variation for a figure presented as a single point estimate.

**Fix:** On the impact page card, change `$3.9B` to `~$3.9B` and add a parenthetical such as "(based on approximately $175B housing stock estimate)." On the methodology page, widen the output to a range rather than a point estimate: e.g., `$3.5B–$4.3B` to reflect the uncertainty in the stock figure. Or at minimum, do not round `$3.85B` up to `$3.9B` if the inputs are only approximate.
**Effort: Small to Medium**

---

### RISK 2.4 — The 4% demand surge upper bound is not adequately explained or sourced
**Risk level: MEDIUM**

The methodology page states: "Upper bound (4% demand surge): $40.0B." Assumption A4 explains this is "vs Milliman's 15% — we use market value not replacement cost as base." However, the 4% figure itself has no source citation. Where does 4% come from? Is this an industry standard, a historical average from previous disasters, or a judgment call by the SmokeStory authors?

On the impact page, the range `$36B–$40B` appears with no explanation of what drives the range — a user reading only the impact page would have no idea that the upper bound is derived from a demand-surge assumption. The explanation is on the methodology page under a collapsed Assumptions section.

**Fix:** Add a one-line source or rationale for the 4% demand surge figure in the methodology page (e.g., cite a specific historical disaster study or explicitly state it is a conservative author judgment). On the impact page, consider adding a tooltip or footnote to the `$36B–$40B` range explaining that the range reflects pre-fire market value (low) to market value with post-fire demand adjustment (high).
**Effort: Small**

---

## Section 3: Understatement Risks

---

### RISK 3.1 — Exclusion of mortality costs from Estimate 03 is not prominent enough on the impact page
**Risk level: HIGH**

Estimate 03 is $0.5B–$1.0B. This uses the COI (Cost of Illness) methodology, which explicitly excludes mortality risk. The methodology page acknowledges this prominently: "COI excludes mortality risk — deliberate conservative choice." The limitations section reinforces: "COI excludes mortality risk."

However, on the impact page, Card 3 lists the components of the estimate as "hospital visits, emergency room trips, missed work days, and asthma attacks." Death is not mentioned. A public health researcher or a critic aware of EPA's own guidance would note that the VSL (Value of Statistical Life) approach — which includes mortality — typically produces estimates 5 to 20 times larger than COI for equivalent pollution events. For a wildfire event that killed 29 people and where PM2.5 averaged 44.8 µg/m³ (nearly 5x the safe limit) for 14 days, excluding mortality from a health cost estimate is a significant conservative choice that should be disclosed on the impact page, not just the methodology page.

If a public health academic encounters this page and calculates a VSL-based estimate of $5B–$10B (which is plausible for this exposure level and population), they could credibly argue that SmokeStory's $0.5B–$1.0B is a severe underestimate that understates the human cost of the fires.

**Fix:** Add a visible note to Card 3 on the impact page stating explicitly: "This estimate excludes mortality costs. Including mortality using VSL methodology would produce a substantially higher figure. We use COI as a conservative, acute-event-appropriate approach." This protects against the criticism that the figure is deliberately low, and is honest about the methodological choice.
**Effort: Small**

---

### RISK 3.2 — Estimate 01 excludes contents, vehicles, infrastructure, and land — not stated on the impact page
**Risk level: MEDIUM**

The methodology page clearly states what Estimate 01 does NOT measure: "Land value · Contents and personal property · Infrastructure · Uninsured losses beyond structure value." This is good practice.

However, the impact page Card 1 describes Estimate 01 only as "The buildings that burned, valued at what they were worth before the fire." This does not explicitly tell readers that personal property, vehicles, contents, and infrastructure are excluded. A homeowner who lost a $2M house plus $200K in contents plus a car could read Card 1 and conclude that SmokeStory's estimate captures their full loss — it does not.

The UCLA Anderson total economic estimate of $95B–$164B includes these broader categories. The gap between $36–40B and $95–164B is partly explained by scope differences, but the impact page does not make this intuitive.

**Fix:** Add a brief exclusion note to Card 1's description text: "Structures only — does not include contents, vehicles, infrastructure, or land value." This can fit in one line and prevents readers from believing the figure is a complete picture of individual losses.
**Effort: Small**

---

### RISK 3.3 — Limitations are hidden behind collapsed collapsible sections on the methodology page
**Risk level: MEDIUM**

The methodology page uses collapsible expand/collapse sections for Assumptions and Limitations for each of the three estimates. This is a reasonable UX choice for a long document, but it means a casual reader who does not click to expand will miss all the following critical caveats:

- Estimate 01: "Neighborhood medians mask bimodal value distribution"; "DINS counts subject to revision"
- Estimate 02: "2.2% is average across many fires — 2025 LA fires may exceed this given urban intensity"; "Study sample may not include events of this scale"; "No distance-decay model applied within the zone"
- Estimate 03: "COI excludes mortality risk"; "Wildfire PM2.5 may be more harmful per µg/m³ than general rate (toxic ash compounds)"; "AQS data preliminary"

These are material limitations. A journalist who reads only the visible text of the methodology page will see the calculations and the favorable validation ("Our number sits above Milliman and below UCLA") without seeing the limitations.

**Fix:** Either (a) expand all limitation sections by default on the methodology page, or (b) add a visible "Key Limitations" summary box near the top of the methodology page that lists the three most important limitations for each estimate. The current overview box only addresses the non-additive nature of the estimates.
**Effort: Small to Medium**

---

### RISK 3.4 — Wildfire-specific PM2.5 toxicity not flagged on the impact page
**Risk level: LOW**

The methodology page notes under Estimate 03 Limitations: "Wildfire PM2.5 may be more harmful per µg/m³ than general rate (toxic ash compounds)." This is a known finding in air quality science — wildfire smoke contains benzene, heavy metals, and other compounds not present in general urban PM2.5 at the same concentration level. Using population-average BenMAP incidence rates that were developed from general urban PM2.5 studies may understate health impacts by a meaningful factor.

This limitation is correctly identified in the methodology. But the impact page's Card 3 states that the calculation uses "the same method the EPA uses" — which is accurate but potentially misleading, because the EPA's BenMAP rates were not specifically calibrated for wildfire smoke.

**Fix:** Add to Card 3's detail text: "Note: BenMAP rates are based on general urban PM2.5. Wildfire smoke may carry additional toxic compounds, so actual health impacts could be higher." This is consistent with what the methodology page says and protects against expert criticism.
**Effort: Small**

---

## Section 4: Reputational Risks

---

### RISK 4.1 — "SmokeStory is not an insurance company or government agency" disclaimer is insufficiently prominent
**Risk level: HIGH**

The disclaimer appears in two places: (1) the bottom disclaimer section of the impact page, rendered in `var(--text-muted)` (#40405a — extremely low contrast against the dark background) at 0.58rem monospace, centered; (2) the methodology page's disclaimer box in similar styling.

Both disclaimers are easy to miss. The styling — tiny, low-contrast, monospace, lowercase — is more decorative than informative. On a dark background (#04040a), #40405a text has a contrast ratio of approximately 2.5:1, which is below the WCAG AA standard of 4.5:1 for normal text. This means the disclaimer is technically unreadable for many users.

If this page were cited in a news article and then fact-checked, the first thing a fact-checker would note is: "SmokeStory is not a peer-reviewed source, not a government agency, and these are preliminary estimates — why is this disclosed only in fine print?" The visual design of the page — premium dark aesthetic, authoritative monospace numbers, amber highlight palette — projects institutional credibility that the content disclaimers explicitly walk back. There is a meaningful gap between what the page looks like and what the disclaimer says it is.

**Fix:** Move the "SmokeStory is an independent open-source project, not an insurance company, government agency, or academic institution" statement to a more prominent position: either (a) as a visible text block immediately below the hero section's title, or (b) as a colored alert banner at the top of the page. The disclaimer text color must be increased to at least #7a7a92 (which is still subdued but readable) or ideally a lighter value. At minimum, ensure WCAG AA contrast compliance.
**Effort: Small**

---

### RISK 4.2 — "Preliminary estimates" label is present but not visually prominent
**Risk level: MEDIUM**

The word "preliminary" appears in the bottom disclaimer of the impact page: "All figures are preliminary estimates using public data and established methodology." It does not appear on any of the three estimate cards, on the headline number, or in the section headers. A reader who never scrolls to the bottom of the page — or who screenshots just the top section — will never see the word "preliminary."

This is a material omission. The CAL FIRE DINS structure counts are explicitly from February 5, 2025, and the methodology page notes "DINS counts subject to revision." If official counts are later revised downward, the $36B–$40B figure would be reported without this context.

**Fix:** Add "(preliminary)" or "Estimate — subject to revision" in small but visible text directly beneath the `$36B–$40B` headline number. Do the same beneath each card number. This is a one-word change per location.
**Effort: Small**

---

### RISK 4.3 — No date-last-updated field or version number on the impact page
**Risk level: MEDIUM**

The methodology page carries "Version 3.0" in the page module label and lists data vintages (CAL FIRE February 5, 2025 · CAR 2024 · EPA AQS January 2025). The impact page carries the same data vintage in its disclaimer, but there is no "last updated" date, no version number, and no statement indicating whether estimates have been revised since initial publication.

If SmokeStory publishes updated estimates as more DINS data becomes available, users who bookmarked the original page would not know they are looking at revised figures. Conversely, users who see a cached or shared screenshot would not know the figures are from a specific data vintage.

**Fix:** Add a visible "Data as of: February 5, 2025 — subject to revision as official counts are updated" line to the impact page, ideally near the headline number. This mirrors standard practice for preliminary government and insurance loss estimates.
**Effort: Small**

---

### RISK 4.4 — Citing "Claude AI" in the page footer raises questions about AI involvement in calculations
**Risk level: MEDIUM**

The page footer of both pages reads: "Tracking Wildfire Smoke Across California · NOAA HMS · EPA AQS · NASA VIIRS · Claude AI"

Listing "Claude AI" alongside federal data sources (NOAA, EPA, NASA) in the footer of a page presenting financial estimates creates an implicit suggestion that Claude AI is a data source comparable to NOAA HMS or EPA AQS. A critic or fact-checker would reasonably ask: What role did Claude AI play in the calculations? Were the financial estimates generated by or validated by an AI? Is the methodology reproducible without AI?

This is a significant reputational liability. Presenting AI-generated or AI-assisted financial estimates without disclosing the nature of that assistance is a criticism that has been leveled at other AI-adjacent data projects. If the Claude AI citation refers to the narrative or design assistance rather than the calculations themselves, this should be clarified.

**Fix:** Either (a) remove "Claude AI" from the footer entirely if its role is limited to prose or UI assistance, (b) separate it clearly from the data source list with a note like "· Built with Claude AI (narrative assistance only)", or (c) add a statement in the methodology page explicitly clarifying Claude AI's role in the project. Mixing Claude AI with NOAA and EPA in an undifferentiated footer is the worst option.
**Effort: Small**

---

## Section 5: Specific Vulnerability Points

---

### RISK 5.1 — The 2.2% depreciation rate is not adequately caveated as a historical average on the impact page
**Risk level: HIGH**

On the impact page, Card 2's expanded detail section states: "Researchers studied dozens of California wildfires and found that homes near — but not in — a fire zone typically lose about 2.2% of their value." This is a reasonable summary of the academic finding.

However, the methodology page's own Limitations section acknowledges: "2.2% is average across many fires — 2025 LA fires may exceed this given urban intensity" and "Study sample may not include events of this scale." These are material caveats. The 2025 LA fires were among the most destructive in California history in terms of structure count and affected urban density, meaning the 2.2% average from a dataset of smaller, less urbanized fires may not apply.

The methodology page also notes (Assumptions A2) that post-fire CAR distressed sales data showed Altadena -39.1% and Palisades -23.7% declines, which are dramatically higher than 2.2%. The assumption dismisses these as "forced lot sales only, not typical residential transactions" — a defensible position, but one a critic could challenge. The 2.2% figure is being applied to surviving homes, while 39% and 24% drops are being observed in real data in the same zip codes.

**Fix:** On the impact page Card 2, add a sentence: "This 2.2% figure is a historical average from prior California fires and may understate impact given the scale of the 2025 LA fires." On the methodology page, add a visible (non-collapsed) note: "Post-fire Altadena and Palisades transaction data shows dramatically larger declines; we use the academic rate as a methodologically consistent baseline, not as a prediction of actual price movements."
**Effort: Small**

---

### RISK 5.2 — Fire perimeter approximations on the map have no visible disclaimer
**Risk level: HIGH**

The JavaScript code in `impact.html` contains the comment `// ── Fire perimeters (approximate GeoJSON) ──`. The polygons are manually hard-coded 8-point polygons:

```
Palisades: [[-118.60, 34.04], [-118.54, 34.01], [-118.46, 34.04], [-118.42, 34.08], ...]
Eaton:     [[-118.15, 34.16], [-118.07, 34.15], [-118.03, 34.18], [-118.04, 34.24], ...]
```

The map section header and subtitle ("Fire Perimeters & Air Quality · January 9, 2025 · Los Angeles County") give no indication that these are approximate polygons rather than official perimeters. The tooltip on hover shows `Palisades Fire — 23,448 acres` and `Eaton Fire — 14,117 acres` with no approximation caveat.

A user comparing these polygons to official CAL FIRE FRAP GeoJSON perimeters (listed as a data source in the methodology page's sources table) would find substantial discrepancies. The official Palisades perimeter has complex irregular geometry that the 8-point approximation does not capture. More critically, the actual perimeter determines which specific properties are inside vs. outside the fire zone — the basis for deciding which structures are counted in Estimate 01 vs. which are "nearby" for Estimate 02.

If the map perimeter is used for any calculation (rather than being purely decorative), this is a serious methodological flaw. If it is decorative only, the map should say so explicitly.

**Fix:** Add a visible label on the map (or directly below it): "Perimeters shown are approximations for illustration only. Official perimeters: CAL FIRE FRAP." Ideally, replace the hard-coded polygons with dynamically loaded official FRAP GeoJSON data. At minimum, add `approximate: true` as a property in the GeoJSON and surface it in the tooltip: "Palisades Fire — 23,448 acres (approximate boundary shown)."
**Effort: Small for disclaimer, Medium for actual FRAP data integration**

---

### RISK 5.3 — The $175B housing stock estimate has no error bound and no independent verification
**Risk level: MEDIUM**

The calculation in Estimate 02 uses `~$175B` as the total market value of ~75,000 surviving structures within 5 miles. The methodology page explains this comes from "LA County Assessor parcel counts and Zillow Research CSV data." No confidence interval, no margin of error, and no cross-check against a third source is provided.

LA County Assessor data is subject to Proposition 13 constraints — assessed values lag market values significantly. Zillow Research CSV data is a useful approximation but is based on Zillow's automated valuation model, which is known to have meaningful error rates (Zillow's own median error rate for off-market homes is approximately 6–7%). Using two sources that both have systematic undervaluation biases (Prop 13 assessor data and Zillow AVM) to arrive at a housing stock estimate and then treating it as a known input raises questions.

If the true housing stock value is $200B rather than $175B (a 14% difference, plausible given Prop 13 lag), Estimate 02 becomes $4.4B rather than $3.9B — a 13% change from a single input assumption.

**Fix:** Add explicit error bounds to the $175B figure: "~$175B ± 20% based on Zillow AVM and LA County Assessor data." Report Estimate 02 as a range ($3.1B–$4.7B) rather than a point estimate, or at minimum acknowledge the sensitivity of the output to this assumption.
**Effort: Small**

---

### RISK 5.4 — The 5-mile radius for Estimate 02 is product-defined, not literature-derived
**Risk level: MEDIUM**

The methodology page's Assumptions section for Estimate 02 states: "5-mile radius is product simplification, not a fixed academic threshold." The academic source (Sathaye et al. 2024) likely uses a different geographic unit or threshold for proximity. Applying the study's 2.2% depreciation rate to a 5-mile radius that was chosen for "product simplification" — rather than replicating the study's actual geographic specification — is a methodological mismatch.

The number of homes and the total housing stock value ($175B) are direct inputs derived from the 5-mile radius. If the actual study used a 1-mile or 2-mile radius (typical in hedonic pricing studies), applying 2.2% to a 5-mile radius would overstate the affected stock and therefore overstate the estimate.

**Fix:** Specify in the methodology page what geographic threshold Sathaye et al. (2024) used and explicitly state whether the 5-mile radius is broader or narrower than the study's specification. If broader, the $3.9B estimate should be qualified as a conservative upper bound assumption. This is currently disclosed only obliquely as a "product simplification."
**Effort: Small**

---

### RISK 5.5 — The Sathaye et al. (2024) citation is not fully verifiable as stated
**Risk level: MEDIUM**

The methodology page cites: "Sathaye et al. (2024), Landscape and Urban Planning — 'Climate change and real estate markets: An empirical study of the impacts of wildfires on home values in California.'"

The impact page card for Estimate 02 cites only: "Peer-reviewed study, Landscape and Urban Planning (2024)" — no author name, no title, no DOI, no link.

For a reader or fact-checker trying to verify this citation, the lack of a DOI, URL, or even a first-author name on the impact page creates a friction point. If the title or author name is slightly wrong (which happens in informal citation), the citation becomes unverifiable. Additionally, Landscape and Urban Planning is a legitimate journal but the specific article details provided — author name "Sathaye," full title — cannot be confirmed from the methodology page alone without external lookup.

A more substantive concern: the methodology page calls the method "quasi-experimental spatial panel models with propensity score matching" and the key finding "2.2% average property value decline." Without a DOI, it is not possible to confirm: (a) whether 2.2% is the paper's primary finding or a secondary result, (b) what the confidence interval on that 2.2% is, (c) whether the study's sample includes fires of comparable scale to the 2025 LA fires.

**Fix:** Add a DOI or stable URL to the Sathaye et al. citation on the methodology page. Add the confidence interval or range reported by the study (not just the point estimate). Add the author's first name and page number or article number.
**Effort: Small**

---

### RISK 5.6 — Uniform PM2.5 exposure assumption is not flagged on the impact page
**Risk level: LOW**

The methodology page notes under Estimate 03 Assumptions: "Uniform exposure assumed across 4.2M zone." In reality, PM2.5 exposure during a wildfire event is heavily spatially heterogeneous — residents immediately adjacent to the fire perimeter likely experienced far higher concentrations than those on the eastern side of LA County. The 44.8 µg/m³ average masks this variation.

Applying a mean exposure level uniformly to 4.2 million people understates the health burden on residents closest to the fires (who experienced higher concentrations) while potentially overstating it for residents farther away. The net effect on the total estimate is unclear, but the assumption is a simplification that a peer reviewer would challenge.

**Fix:** Add to the Estimate 03 limitations on the methodology page: "Spatial variation in PM2.5 exposure is not modeled. Communities immediately adjacent to fire perimeters likely experienced substantially higher concentrations, meaning the uniform-exposure assumption may understate peak health impacts for the most-exposed population while overstating for the least-exposed." This is already implied by the existing limitation "AQS data preliminary" but should be stated explicitly.
**Effort: Small**

---

## Section 6: Additional Observations

---

### RISK 6.1 — The hero section death toll figure (29 lives) may be under-reported
**Risk level: MEDIUM**

The hero section states "29 Lives Lost." As of the data vintage cited (February 2025), this is plausibly accurate for the combined Palisades and Eaton fires' directly confirmed fatalities. However, wildfire mortality figures are often revised upward over time as missing persons cases are resolved and excess mortality studies are completed. Using a single confirmed-fatalities figure without a "confirmed as of [date]" qualifier or a note that indirect mortality (from smoke exposure, evacuation stress, medical disruption) is not included creates a vulnerability.

If the actual death toll was later revised upward — or if a public health study estimated 100+ indirect deaths from smoke exposure — the "29 Lives Lost" figure on the impact page could look like a deliberate undercount.

**Fix:** Change to "29 Confirmed Deaths (as of February 5, 2025)" and add a footnote: "Does not include indirect deaths from smoke exposure or evacuation-related mortality."
**Effort: Small**

---

### RISK 6.2 — No explicit statement about what the page is NOT suitable for
**Risk level: LOW**

The current disclaimers tell users what the estimates measure and what SmokeStory is not. They do not tell users what the page should NOT be used for. Appropriate explicit restrictions would include: not for insurance claims, not for legal proceedings, not for government grant applications, not as a substitute for official loss assessments.

This is a low-probability risk but a high-consequence one: if someone uses the SmokeStory estimates in an insurance dispute or legal proceeding and they are challenged, SmokeStory could face reputational damage.

**Fix:** Add one sentence to the disclaimer section: "These estimates are for informational and educational purposes only and are not suitable for insurance claims, legal proceedings, or government applications."
**Effort: Small**

---

## Summary Table

| Risk ID | Risk | Level | Effort |
|---------|------|--------|--------|
| 1.1 | $36B–$40B headline misquoted as total economic loss | High | Small |
| 1.2 | Three estimates added together to produce false total | High | Small |
| 1.3 | $3.9B misread as realized cash loss | Medium | Small |
| 2.1 | Bar chart misleads by mixing incomparable methodologies | High | Medium |
| 2.2 | "SmokeStory Unique Contribution" badge overstates novelty | Medium | Small |
| 2.3 | $175B housing stock treated as known quantity, not approximation | Medium | Small–Medium |
| 2.4 | 4% demand surge upper bound not sourced | Medium | Small |
| 3.1 | Mortality exclusion not prominent on impact page | High | Small |
| 3.2 | Estimate 01 scope exclusions not stated on impact page | Medium | Small |
| 3.3 | Limitations hidden behind collapsed collapsibles | Medium | Small–Medium |
| 3.4 | Wildfire PM2.5 toxicity not flagged on impact page | Low | Small |
| 4.1 | Disclaimer text too low-contrast and visually buried | High | Small |
| 4.2 | "Preliminary" label absent from headline number and cards | Medium | Small |
| 4.3 | No last-updated date on impact page | Medium | Small |
| 4.4 | "Claude AI" in footer alongside federal data sources | Medium | Small |
| 5.1 | 2.2% depreciation rate not caveated as historical average on impact page | High | Small |
| 5.2 | Approximate fire perimeters on map have no visible disclaimer | High | Small–Medium |
| 5.3 | $175B housing stock has no error bound or independent verification | Medium | Small |
| 5.4 | 5-mile radius is product-defined, not literature-derived | Medium | Small |
| 5.5 | Sathaye et al. citation lacks DOI and confidence interval | Medium | Small |
| 5.6 | Uniform PM2.5 exposure assumption not flagged on impact page | Low | Small |
| 6.1 | Death toll figure may be under-reported without date caveat | Medium | Small |
| 6.2 | No explicit statement of inappropriate use cases | Low | Small |

---

## Priority Fixes (High-impact, Low-effort — Do First)

1. **Add "(preliminary)" and "direct property destruction only" directly beneath the $36B–$40B headline number.** (Risks 1.1, 4.2)
2. **Add "Do Not Add" badges or callout to Cards 1 and 3.** (Risk 1.2)
3. **Add a visible mortality exclusion note to Card 3 on the impact page.** (Risk 3.1)
4. **Add an approximate boundary disclaimer on or below the map.** (Risk 5.2)
5. **Increase contrast on disclaimer text and move the "independent open-source project" statement to a more prominent position.** (Risk 4.1)
6. **Add "(unrealized)" after the $3.9B figure in Card 2.** (Risk 1.3)
7. **Clarify "Claude AI" footer attribution.** (Risk 4.4)
8. **Restructure the comparison bar chart section subtitle to not imply SmokeStory is a peer of Moody's and Milliman.** (Risk 2.1 — partial fix, small effort)

---

*End of report.*
