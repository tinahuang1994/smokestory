# Journalist Review: SmokeStory Financial Impact Page
**Reviewed by:** Climate & Economics Desk
**Date:** March 26, 2026
**Pages reviewed:** `/impact` and `/methodology`
**Story context:** 2025 LA wildfires economic damage — on deadline, need a quotable number

---

## Bottom Line Up Front

This page is more credible than most NGO or startup economic dashboards I encounter. The methodology is unusually transparent. The explicit warning that the three numbers must not be added together is rare and responsible — most advocacy sites would happily let readers do that math. The headline number ($36B–$40B) is defensible enough to mention in copy **with caveats**, but I would not quote SmokeStory as the primary source. I would use this page to identify the right sources to call (CAL FIRE, CAR, Milliman) and to verify that this number sits in a credible range. The comparison chart showing how this estimate relates to Moody's, Milliman, and UCLA Anderson is the most useful element on the page for a journalist.

The page has real problems I address below, but none are disqualifying. Fix the top two before you start getting press calls.

---

## 1. Quotability

### The $36B–$40B Headline Number

**Severity: Concern**

The $36B–$40B figure is mathematically sound and the methodology page shows the arithmetic openly. The inputs — CAL FIRE structure counts, CAR median prices — are legitimate public sources. The range sits logically between Milliman (insured only, lower) and UCLA Anderson (broader scope, much higher), which is the right neighborhood.

What I cannot verify on deadline: whether the CAR 2024 median price for Pacific Palisades ($3.31M) is the right proxy for destroyed structures specifically. Palisades is a diverse geography. The methodology page itself acknowledges "neighborhood medians mask bimodal value distribution" — that is a significant caveat buried in a collapsible dropdown. A $3.31M median applied to 6,831 structures is a $22.6B assumption that depends entirely on whether those destroyed structures were representative of the neighborhood's median. The methodology does not cite a specific CAR publication by name or date — just "CAR 2024."

**Would I cite it without calling an expert?** No. I would call someone at Milliman or a real estate economist at UCLA before putting a figure in print. But I would cite this page as the basis for knowing which experts to ask, and I would describe the range as consistent with independent actuarial estimates.

**What my editor would push back on:** "Who is SmokeStory and why should I trust their math over Milliman?" That question has a good answer — this estimate measures something different (market value including uninsured) — but the page does not make that case clearly enough until you scroll deep.

### The $0.5B–$1.0B Smoke Health Cost

**Severity: Minor note**

This is actually the most interesting number for a climate story because no other published LA wildfire estimate includes it. The methodology is EPA BenMAP, which is a legitimate and well-documented federal tool. The numbers are reproducible. The page is honest that it uses cost-of-illness (COI) rather than value-of-statistical-life (VSL), and explains why — that is the right methodological choice for an acute event and it is rare to see that explained at this level of transparency.

Problem: the label "SmokeStory Unique Contribution" on the card makes this look like a marketing claim rather than a factual one. It reads as boastful. A reporter would quote this number cautiously, needing to attribute it to EPA BenMAP methodology applied by SmokeStory, not simply to "SmokeStory."

---

## 2. Trust Signals

**Overall verdict: Above average for an independent project, below average for something I would cite without verification.**

What builds trust:
- CAL FIRE, CAR, EPA BenMAP, EPA AQS, BLS — these are all primary government sources with known reputations. A journalist can check every one of them.
- The explicit "must not be added together" warning, repeated three times, demonstrates the authors understand the risk of misuse. This is not something a bad-faith actor would include.
- The methodology page shows the actual arithmetic. The number $36.03B is displayed with the multiplication shown. That is auditable.
- The comparison to Milliman and UCLA Anderson is appropriate and honest — neither number is cherry-picked.
- The limitations sections in the methodology page are specific and self-critical. "DINS counts subject to revision" and "AQS data preliminary — final QA available 6+ months post-collection" are things a journalist needs to know.
- The Sathaye et al. (2024) citation for Estimate 02 is named, journal-identified, and has a findable title. I can look that up.

What undermines trust:
- The footer lists "Claude AI" alongside NOAA, EPA, and NASA. This is a significant credibility problem. More on this below.
- SmokeStory self-describes as "independent open-source project, not an insurance company, government agency, or academic institution." That is an honest disclaimer, but it also means there is no institutional accountability. No named author, no affiliated institution, no byline.
- The GitHub link goes to a personal repository (github.com/tinahuang1994/smokestory). That is fine for transparency purposes, but it confirms this is one person's project, not an organization.

---

## 3. Missing Context

**What the page does not answer that I need to know:**

### No Named Author or Contact

**Severity: Would not cite**

There is no byline, no named researcher, no contact email, no institutional affiliation. The GitHub link reveals a username (tinahuang1994) but that is not the same as a professional attribution. If I cite this page, I have no one to call for comment, no way to verify credentials, and no way to inform the source that I am using their work. This is a hard stop for most newsrooms. I cannot write "according to SmokeStory" without explaining what SmokeStory is, and this page never tells me.

**Fix:** Add a byline. Name the person or team. Include an email. Even "Developed by [Name], independent researcher" is better than nothing.
**Effort:** Small

### Publication or Last-Updated Date

**Severity: Concern**

The data vintage is noted (CAL FIRE February 5, 2025; CAR 2024) but there is no "this page was last updated on X" timestamp. For a story running in March 2026, a reader cannot tell whether these estimates have been revised since initial publication. CAL FIRE DINS figures are explicitly flagged as subject to revision on the methodology page, which means this could be stale.

**Fix:** Add a "Last updated" date to the page header of both impact.html and methodology.html.
**Effort:** Small

### The CAR Citation Is Too Vague

**Severity: Concern**

The California Association of Realtors is cited as "CAR 2024" throughout. No specific report title, no URL, no report month. CAR publishes multiple products — quarterly median price reports, county-level reports, ZIP-level data. $3.31M for Pacific Palisades and $1.425M for Altadena need to be traceable to a specific published document. If I call CAR's press office, I need to be able to say "your Q3 2024 county report" or "your October 2024 ZIP-level data."

**Fix:** Expand the citation to include report name, month, and a URL or at minimum the path to find it on car.org.
**Effort:** Small

### The "75,000 homes within 5 miles" Assumption Is Not Sourced at Impact Level

**Severity: Minor note**

Estimate 02 uses "roughly 75,000 homes within 5 miles" as a core input. On the impact page, this number appears without any sourcing. The methodology page acknowledges it is "approximate, derived from LA County Assessor parcel counts and Zillow Research CSV data" but does not show the calculation. For a $3.9B figure, I would want to see how 75,000 and $175B were derived.

**Fix:** Add a brief calculation note to the methodology page showing how 75,000 structures and $175B total value were estimated.
**Effort:** Small to Medium

---

## 4. Red Flags

### "Claude AI" in the Footer

**Severity: Would not cite**

The page footer reads: "NOAA HMS · EPA AQS · NASA VIIRS · Claude AI"

Listing Claude AI alongside federal scientific agencies implies it is a data source of equivalent standing. It is not. Claude is a large language model; it does not collect empirical data. If it was used for drafting, calculations, or code generation, that belongs in a separate "Tools Used" note — not in a data sources footer next to NOAA and NASA. Any editor who sees this will immediately question the entire page. Any fact-checker will flag it. This is the single biggest credibility problem on the page.

**Fix:** Remove "Claude AI" from the data sources footer. If AI tools were used in production, disclose this in a separate production note distinct from the data attribution line.
**Effort:** Small — this is one line of HTML

### The Upper Bound Methodology for Estimate 01 Is Thin

**Severity: Concern**

The upper bound of $40B is derived by applying a "4% demand surge" to the $36B lower bound. The methodology page justifies this as "vs Milliman's 15% — we use market value not replacement cost as base." That comparison is reasonable but the 4% figure itself is not sourced. Where does 4% come from? Is it from a published study? Is it an internal assumption? The lower bound ($36.03B) is derived from primary data; the upper bound ($40B) is derived from an unsourced adjustment. A range implies both ends are equally supported.

**Fix:** Cite the specific basis for the 4% demand surge assumption — a published study, historical comparable, or at minimum label it explicitly as an internal assumption.
**Effort:** Small

### Estimate 02 Uses a Single Academic Paper as Its Entire Basis

**Severity: Concern**

The $3.9B neighborhood value impact is built entirely on the 2.2% figure from Sathaye et al. (2024). The methodology page notes that "2.2% is average across many fires — 2025 LA fires may exceed this given urban intensity" and that the "study sample may not include events of this scale." These are meaningful caveats. Applying a rate derived from smaller, less urban fires to one of the most expensive residential fire events in US history is an extrapolation that a real estate economist would push back on. The self-identified limitation that the 2.2% may be too low is buried in a collapsible dropdown.

This is not a reason to remove the estimate. It is a reason to surface the caveat more prominently.

**Fix:** Add a brief note next to the $3.9B figure on the impact card flagging that this uses a multi-fire average rate and may understate impact for an urban fire of this scale.
**Effort:** Small

### No Shareable or Static Version Exists

**Severity: Concern**

The page is a dynamic web application with interactive maps, collapsible sections, and live data layers pulled from an API. There is no PDF download, no static archive link, no DOI, no permalink with a version number. If this page changes after I cite it, I have no way to document what it said when I used it. The methodology page lists "Version 3.0" — that is good — but it does not tell me what changed from Version 2.0 or when Version 3.0 was released.

**Fix:** Add a PDF export button or, at minimum, a note that the current version is 3.0 with a release date. A Wayback Machine-friendly static snapshot would help.
**Effort:** Medium

---

## 5. Usability for Deadline

**Verdict: Good design, critical information too slow to surface.**

### Finding the Number: Fast

The $36B–$40B headline is visible within seconds. The three-card layout is clear. The "must not be added together" warning is prominent. This is well-designed.

### Understanding What the Number Means: Slow

The key context — that this measures market value of destroyed structures, not insured losses, not total economic impact — requires clicking through to the methodology page and then opening collapsible sections. For a journalist with 20 minutes, this is too many clicks. The comparison chart (Moody's, Milliman, SmokeStory, UCLA Anderson) is extremely useful and should be higher on the page, ideally visible alongside the headline number.

**Fix:** Move the comparison chart above the three cards, or add a single line under the headline number explaining the scope difference from Milliman.
**Effort:** Small

### Contact: Does Not Exist

There is no contact information anywhere on either page. For a reporter on deadline who wants to quote a source, this is a dead end.

**Fix:** Add a contact line to the methodology page — even a GitHub issue link or a public email.
**Effort:** Small

### Download or Export: Does Not Exist

No PDF, no CSV, no data download. The map cannot be exported.

**Fix:** Add a simple "Download methodology as PDF" or "View data on GitHub" link.
**Effort:** Medium

---

## Summary: Priority Fixes Before Press Coverage

| Priority | Issue | Severity | Effort |
|----------|-------|----------|--------|
| 1 | Remove "Claude AI" from data sources footer | Would not cite | Small |
| 2 | Add named author / contact information | Would not cite | Small |
| 3 | Add a last-updated date to both pages | Concern | Small |
| 4 | Specify the CAR citation — report name, month, URL | Concern | Small |
| 5 | Source the 4% demand surge assumption | Concern | Small |
| 6 | Surface the "urban fire caveat" for Estimate 02 outside the collapsible | Concern | Small |
| 7 | Move the comparison chart higher on the impact page | Concern | Small |
| 8 | Show calculation basis for 75,000-home / $175B figures | Minor note | Small-Medium |
| 9 | Add a static/downloadable version | Concern | Medium |
| 10 | Rename "SmokeStory Unique Contribution" badge to something less promotional | Minor note | Small |

---

## Final Assessment

If I were writing a story about the total economic damage of the 2025 LA wildfires, I would use this page for three things:

1. The comparison chart showing where different estimates sit relative to each other — this is genuinely useful and well-explained.
2. The $0.5B–$1.0B smoke health cost estimate as context for a separate angle on public health economics, attributed to "an independent analysis using EPA BenMAP methodology."
3. Pointers to the primary sources I actually want to quote: CAL FIRE DINS data, Milliman's actuarial report, UCLA Anderson's estimate, and the Sathaye et al. paper.

I would not cite the $36B–$40B figure directly without calling an actuary or real estate economist to confirm the range. But I would arrive at those calls better-informed because of this page, which is worth something.

The methodology transparency is genuinely impressive for an independent project. Fix the Claude AI footer and add a contact line before you start promoting this to journalists, because those two issues will stop a story in its tracks.
