# SmokeStory Financial Impact — Data Integrity Report

**Auditor:** Data Editor review
**Date:** 2026-03-26
**Files audited:**
- `/Users/tinahuang/Desktop/smokestory/frontend/impact.html`
- `/Users/tinahuang/Desktop/smokestory/frontend/methodology.html`
- `/Users/tinahuang/Desktop/smokestory/frontend/index.html`

---

## Executive Summary

The three files are largely consistent and the core calculations are mathematically correct. Seven issues were found: two inconsistencies (dash character mismatch on the headline figure, Milliman range rounded differently across files), two calculation discrepancies (work-loss days and restricted-activity days are off by small amounts), one rounding inconsistency (base total shown as $546M instead of $546.2M), one framing inconsistency (estimate naming convention differs between the two pages), and one minor source attribution gap. No issues were found with the headline estimate range ($36B–$40B), the $3.9B figure, the $0.5B–$1.0B figure, the structure counts, or the major calculation chain for Estimate 01.

**Issues by severity:**

| # | Type | File(s) | Effort |
|---|------|---------|--------|
| 1 | Inconsistency — dash character | impact.html | Small |
| 2 | Inconsistency — Milliman range | impact.html vs methodology.html | Small |
| 3 | Calculation error — work-loss days | methodology.html | Small |
| 4 | Calculation error — restricted-activity days | methodology.html | Small |
| 5 | Rounding inconsistency — base total | methodology.html | Small |
| 6 | Framing inconsistency — estimate naming | impact.html vs methodology.html | Small |
| 7 | Missing attribution detail — Sathaye 2024 | impact.html | Small |

---

## Section 1 — Number Consistency Check

### 1.1 $36B–$40B (Headline estimate)

| Location | Text as written | Status |
|----------|----------------|--------|
| impact.html — hero headline number (line 561) | `$36B — $40B` (em-dash, spaces) | **ISSUE — see Issue 1** |
| impact.html — Card 1 number (line 576) | `$36B – $40B` (en-dash) | OK |
| impact.html — Comparison bar value (line 664) | `$36B – $40B` (en-dash) | OK |
| methodology.html — section label (line 480) | `$36B – $40B` (en-dash) | OK |
| methodology.html — final range in calculation block (line 511) | `$36B – $40B` (en-dash) | OK |
| index.html — impact card injected via JS (line 1610) | `$36B — $40B` (em-dash, spaces) | **ISSUE — see Issue 1** |

Three of six appearances use an en-dash (`–`); two use a spaced em-dash (`—`). The hero on impact.html and the index.html impact card both use `—` while all other instances use `–`.

### 1.2 $3.9B

| Location | Text as written | Status |
|----------|----------------|--------|
| impact.html — Card 2 number (line 594) | `$3.9B` | OK |
| methodology.html — section label (line 560) | `$3.9B` | OK |
| methodology.html — final estimate line (line 578) | `$3.9B` | OK |

All consistent.

### 1.3 $0.5B–$1.0B

| Location | Text as written | Status |
|----------|----------------|--------|
| impact.html — Card 3 number (line 610) | `$0.5B – $1.0B` | OK |
| methodology.html — section label (line 615) | `$0.5B – $1.0B` | OK |
| methodology.html — final range (line 650) | `$0.5B – $1.0B` | OK |

All consistent.

### 1.4 16,249 structures

| Location | Text as written | Status |
|----------|----------------|--------|
| impact.html — Card 1 expanded detail (line 581) | `16,249 destroyed or seriously damaged structures` | OK |
| methodology.html — total destroyed count (line 491) | `16,249` | OK |

Consistent. Note: the sub-counts add up correctly: 6,831 + 9,418 = **16,249**. Verified.

### 1.5 29 lives lost

| Location | Text as written | Status |
|----------|----------------|--------|
| impact.html — hero stats (line 555) | `29 Lives Lost` | OK |

Only one mention in these files. Consistent with itself.

### 1.6 150,000 residents displaced

| Location | Text as written | Status |
|----------|----------------|--------|
| impact.html — hero stats (line 555) | `150,000 Residents Displaced` | OK |

Only one mention in these files. Consistent with itself.

### 1.7 6,831 Palisades destroyed / 9,418 Eaton destroyed

| Location | Text as written | Status |
|----------|----------------|--------|
| methodology.html — structure counts box (line 489–490) | `6,831` / `9,418` | OK |
| methodology.html — calculation block (lines 504–505) | `6,831` / `9,418` | OK |

Consistent across both appearances.

### 1.8 Pre-fire prices

| Location | Text as written | Status |
|----------|----------------|--------|
| impact.html — Card 1 expanded detail (line 583) | `$3.3M average in Pacific Palisades, $1.4M average in Altadena` | Rounded — OK for body copy |
| methodology.html — price box (lines 498–499) | `$3,310,000` / `$1,425,000` | OK — full precision |

The card text uses rounded figures ($3.3M, $1.4M) while the methodology uses full figures. This is appropriate for a summary card but worth noting. No error.

### 1.9 44.8 µg/m³ PM2.5

| Location | Text as written | Status |
|----------|----------------|--------|
| impact.html — Card 3 expanded detail (line 615) | `44.8 µg/m³` | OK |
| methodology.html — exposure data box (line 624) | `44.8 µg/m³` | OK |

Consistent.

### 1.10 4,200,000 exposed population

| Location | Text as written | Status |
|----------|----------------|--------|
| impact.html — Card 3 description (line 612) | `4.2 million residents` | OK |
| methodology.html — exposure data box (line 628) | `4,200,000` | OK |

Consistent.

### 1.11 Milliman range

| Location | Text as written | Status |
|----------|----------------|--------|
| impact.html — comparison bar (line 654) | `$25B – $39B` | **ISSUE — see Issue 2** |
| methodology.html — validation section (line 535) | `$25.2B–$39.4B` | OK — full precision |

The comparison bar on impact.html drops the decimal precision and rounds down both endpoints. This understates the Milliman range slightly (midpoint shifts from $32.3B to $32.0B).

### 1.12 UCLA Anderson range

| Location | Text as written | Status |
|----------|----------------|--------|
| impact.html — comparison bar (line 674) | `$95B – $164B` | OK |
| methodology.html — validation section (line 536) | `$95B–$164B` | OK |

Consistent (minor: impact.html uses spaces around dash, methodology does not — acceptable stylistic variation).

---

## Section 2 — Calculation Verification

All work shown below. Results are compared against values as stated in methodology.html.

### 2.1 Palisades destroyed: 6,831 × $3,310,000

```
6,831 × $3,000,000 = $20,493,000,000
6,831 ×   $310,000 =  $2,117,610,000
─────────────────────────────────────
Total              = $22,610,610,000
                   = $22.6106B
```

**Rounds to $22.61B.** Document states `$22.61B`. CORRECT.

### 2.2 Eaton destroyed: 9,418 × $1,425,000

```
9,418 × $1,000,000 =  $9,418,000,000
9,418 ×   $425,000 =  $4,002,650,000
─────────────────────────────────────
Total              = $13,420,650,000
                   = $13.4207B
```

**Rounds to $13.42B.** Document states `$13.42B`. CORRECT.

### 2.3 Subtotal destroyed: $22.61B + $13.42B

```
$22,610,610,000
+ $13,420,650,000
──────────────────
= $36,031,260,000
= $36.031B
```

**Rounds to $36.03B.** Document states `$36.03B`. CORRECT.

### 2.4 Major damage: 2,046 × $2,367,500 × 50%

Average price derivation:
```
($3,310,000 + $1,425,000) / 2 = $4,735,000 / 2 = $2,367,500
```

Calculation:
```
2,046 × $2,367,500 = ?
2,046 × $2,000,000 = $4,092,000,000
2,046 ×   $367,500 = $751,905,000
─────────────────────────────────────
2,046 × $2,367,500 = $4,843,905,000

× 50% = $2,421,952,500 = $2.422B
```

**Rounds to $2.42B.** Document states `$2.42B`. CORRECT.

### 2.5 Property value decline: $175B × 2.2%

```
$175,000,000,000 × 0.022 = $3,850,000,000 = $3.85B
```

**$3.85B rounds to $3.9B.** Document states `$3.85B → $3.9B`. CORRECT.

### 2.6 Acute hospital admissions: 800,000 × 0.17% × 3.58

```
800,000 × 0.0017 = 1,360
1,360 × 3.00     = 4,080.0
1,360 × 0.58     =   788.8
─────────────────────────────
1,360 × 3.58     = 4,868.8
```

**Rounds to 4,869.** Document states `4,869 cases`. CORRECT.

### 2.7 ER visits: 4,200,000 × 0.24% × 3.58

```
4,200,000 × 0.0024 = 10,080
10,080 × 3.00      = 30,240.0
10,080 × 0.58      =  5,846.4
──────────────────────────────
10,080 × 3.58      = 36,086.4
```

**Rounds to 36,086.** Document states `36,086 visits`. CORRECT.

### 2.8 Admissions cost: 4,869 × $40,000

```
4,869 × $40,000 = $194,760,000 = $194.76M
```

**Rounds to $194.8M.** Document states `$194.8M`. CORRECT.

### 2.9 ER cost: 36,086 × $1,200

```
36,086 × $1,000 = $36,086,000
36,086 ×   $200 =  $7,217,200
─────────────────────────────
Total           = $43,303,200 = $43.3M
```

**$43.3M.** Document states `$43.3M`. CORRECT.

### 2.10 Asthma cases: 450,000 × 3.0% × 3.58

```
450,000 × 0.030 = 13,500
13,500 × 3.00   = 40,500.0
13,500 × 0.58   =  7,830.0
─────────────────────────
13,500 × 3.58   = 48,330.0
```

**48,330 cases.** Document states `48,330 attacks`. CORRECT.

### 2.11 Asthma cost: 48,330 × $220

```
48,330 × $200 = $9,666,000
48,330 ×  $20 =   $966,600
────────────────────────────
Total         = $10,632,600 = $10.6M
```

**$10.6M.** Document states `$10.6M`. CORRECT.

### 2.12 Work-loss days: 4,200,000 × 0.046 × 3.58

```
4,200,000 × 0.046 = 193,200

193,200 × 3.00 = 579,600
193,200 × 0.50 =  96,600
193,200 × 0.08 =  15,456
─────────────────────────
193,200 × 3.58 = 691,656
```

**Correct answer: 691,656.** Document states `691,464 days`.

**DISCREPANCY: 691,656 − 691,464 = 192 days.** The published figure is 192 days lower than the stated inputs produce. See Issue 3.

### 2.13 Work-loss cost: 691,464 × $280 (using document's stated case count)

```
691,464 × $200 = $138,292,800
691,464 ×  $80 =  $55,317,120
───────────────────────────────
Total          = $193,609,920 = $193.6M
```

Using the document's stated 691,464 days: **$193.6M.** Document states `$193.6M`. Internally consistent.

If the corrected count (691,656) is used: 691,656 × $280 = $193,663,680 = **$193.7M** (rounds differently by $0.1M).

### 2.14 Restricted-activity days: 4,200,000 × 0.072 × 3.58

```
4,200,000 × 0.072 = 302,400

302,400 × 3.00 = 907,200
302,400 × 0.50 = 151,200
302,400 × 0.08 =  24,192
─────────────────────────
302,400 × 3.58 = 1,082,592
```

**Correct answer: 1,082,592.** Document states `1,082,016 days`.

**DISCREPANCY: 1,082,592 − 1,082,016 = 576 days.** See Issue 4.

### 2.15 Restricted-activity cost: 1,082,016 × $96 (using document's stated count)

```
1,082,016 × $100 = $108,201,600
1,082,016 ×   $4 =   $4,328,064
─────────────────────────────────
1,082,016 × $96  = $103,873,536 = $103.9M
```

Using the document's stated 1,082,016 days: **$103.9M.** Document states `$103.9M`. Internally consistent.

If the corrected count (1,082,592) is used: 1,082,592 × $96 = $103,929,832 = **$103.9M** (no change to displayed rounding).

### 2.16 Grand total — sum of all five cost components

Using the rounded per-line figures as displayed in methodology.html:

```
Admissions:          $194.8M
ER visits:            $43.3M
Asthma attacks:       $10.6M
Work loss:           $193.6M
Restricted activity: $103.9M
─────────────────────────────
Sum:                 $546.2M
```

**Document states `Base total: $546M`.** The sum of the displayed rounded components is **$546.2M**, not $546M. See Issue 5.

---

## Section 3 — Source Attribution

### Data Sources Table (methodology.html)

| Source | Date/Version | Findable? | Status |
|--------|-------------|-----------|--------|
| CAL FIRE DINS | Feb 5, 2025 | Yes — fire.ca.gov | OK |
| CAR 2024 | 2024 (annual report) | Yes — public reports | OK — could add specific report title |
| Zillow Research CSV | No date | Yes — zillow.com/research/data | Missing vintage date |
| LA County Assessor Open Data | No date | Yes — data.lacounty.gov | Missing vintage date |
| Sathaye et al. 2024 LUP | 2024 | Yes — peer-reviewed | **ISSUE — see Issue 7** |
| EPA AQS Param 88101 | Jan 2025 (in context) | Yes — public API | OK |
| EPA BenMAP TSD | Jan 2023 | Yes — epa.gov/benmap | OK |
| EPA BenMAP COI | 2023 | Yes — epa.gov/benmap | OK |
| BLS 2024 LA County | 2024 | Yes — bls.gov | OK |
| CHIS 2021–2022 | 2021–2022 | Yes — UCLA CHIS | OK |
| CAL FIRE FRAP | No date | Yes — public GeoJSON | Missing vintage date |
| NOAA HMS | No date | Yes — via SmokeStory | Missing date (acceptable for ongoing operational data) |

The Sathaye et al. reference is the most significant gap (Issue 7). All other sources have enough detail to locate the material. The three missing vintage dates (Zillow CSV, LA County Assessor, CAL FIRE FRAP) are minor.

### Sources cited in impact.html card detail panels (not in table)

| Source mentioned | Detail provided | Status |
|-----------------|----------------|--------|
| CAL FIRE field inspections (Feb 5, 2025) | Date included | OK |
| California Association of Realtors 2024 | Year included | OK |
| Peer-reviewed study, Landscape and Urban Planning (2024) | No author, no volume/issue | **ISSUE — see Issue 7** |
| EPA BenMAP methodology | No version date | Minor — full cite in methodology.html |

---

## Section 4 — Framing Consistency

### 4.1 Page title

| File | Title element | H1 / primary heading |
|------|--------------|---------------------|
| impact.html | `Financial Impact · SmokeStory` | `Palisades & Eaton Fires / Financial Impact` |
| methodology.html | `Full Methodology · SmokeStory` | `Full Methodology` |

The impact page title is `Financial Impact · SmokeStory`. The context block calls it "Financial Impact of the 2025 LA Wildfires" — this exact phrase does not appear verbatim in either file. The impact.html hero says "Palisades & Eaton Fires / Financial Impact" and methodology.html module label says "SmokeStory Financial Impact Module." These are close enough to be editorially consistent but the phrase "Financial Impact of the 2025 LA Wildfires" is not used verbatim anywhere.

### 4.2 Estimate naming convention

| File | Naming used |
|------|-------------|
| impact.html — card labels | `Estimate 01`, `Estimate 02`, `Estimate 03` |
| impact.html — chart note | `Estimate 01` |
| methodology.html — section headings | `Number 1`, `Number 2`, `Number 3` |
| methodology.html — section labels | `Headline Figure: $36B – $40B` / `Estimate: $3.9B` / `Estimate: $0.5B – $1.0B` |
| methodology.html — overview text | "three independent, clearly separated economic impacts" (no numbered labels used) |

**ISSUE — see Issue 6.** impact.html uses "Estimate 01/02/03" throughout. methodology.html uses "Number 1/2/3" for section headings. A reader following the link from impact.html to methodology.html must mentally remap the nomenclature.

---

## Section 5 — Bar Chart Proportions

The comparison chart on impact.html uses UCLA Anderson ($95B–$164B) as the 100% bar. All other bars should be proportional to that baseline.

**Reference midpoints:**

| Source | Displayed range | Midpoint used | Correct % of UCLA mid | CSS width set |
|--------|----------------|--------------|----------------------|---------------|
| Moody's RMS | $20B–$30B | $25.0B | 19.3% | 19% |
| Milliman | $25B–$39B (displayed) / $25.2B–$39.4B (methodology) | $32.0B / $32.3B | 24.7% / 24.9% | 25% |
| SmokeStory | $36B–$40B | $38.0B | 29.3% | 29% |
| UCLA Anderson | $95B–$164B | $129.5B | 100.0% | 100% |

**Calculation detail:**

UCLA midpoint: (95 + 164) / 2 = **$129.5B**

```
Moody's:    $25.0B / $129.5B = 19.31% → CSS 19%  (rounds down by 0.31pp — visually acceptable)
Milliman:   $32.3B / $129.5B = 24.94% → CSS 25%  (correct to nearest whole percent)
SmokeStory: $38.0B / $129.5B = 29.34% → CSS 29%  (rounds down by 0.34pp — visually acceptable)
UCLA:       100%              → CSS 100%           (correct)
```

**All four CSS widths are proportionally reasonable.** The Moody's and SmokeStory bars are each truncated by roughly 0.3 percentage points, which is imperceptible at this scale. No material error.

---

## Issues — Full Detail

### Issue 1 — Inconsistency: Dash character in $36B headline figure

- **Type:** Inconsistency
- **Where:** impact.html line 561 (hero `headline-number` div); index.html line 1610 (JS-injected impact card)
- **What:** The hero and the index.html card use a spaced em-dash: `$36B — $40B`. All other appearances (impact.html card 1, comparison bar value, methodology.html section label, methodology.html calculation block) use an en-dash: `$36B – $40B`. These render as visually distinct characters.
- **Fix:** Standardize on en-dash throughout. Change `$36B — $40B` to `$36B – $40B` in the two locations that use em-dash (impact.html line 561, index.html impact card JS string).
- **Effort:** Small

---

### Issue 2 — Inconsistency: Milliman range truncated on impact.html

- **Type:** Inconsistency
- **Where:** impact.html line 654 (comparison bar label `bar-value` span)
- **What:** impact.html displays Milliman as `$25B – $39B`. methodology.html (the authoritative source) states `$25.2B–$39.4B`. The impact.html version silently rounds down both endpoints, understating the upper bound by $0.4B. The midpoint shifts from $32.3B to $32.0B.
- **Fix:** Update the bar label in impact.html to `$25.2B – $39.4B` to match the methodology file and the actual published Milliman figure.
- **Effort:** Small

---

### Issue 3 — Calculation error: Work-loss days

- **Type:** Calculation error
- **Where:** methodology.html line 637 (health impact functions mono-block)
- **What:** The stated calculation `0.046 × 3.58` for 4,200,000 people yields:
  ```
  4,200,000 × 0.046 × 3.58 = 193,200 × 3.58 = 691,656 days
  ```
  The document states `691,464 days`. The discrepancy is **192 days** (691,656 − 691,464). This likely reflects rounding the intermediate step (193,200 rounded to 193,148 or similar), or a transcription error.
- **Impact on cost line:** At $280/day, a 192-day error = $53,760 — immaterial at the $193.6M scale and does not change the rounded dollar figure. The downstream cost figure (`$193.6M`) is correct given the document's own stated day count.
- **Fix:** Re-derive 691,464 from the actual intermediate rounding used (or correct to 691,656 and leave all downstream figures unchanged since rounding is unaffected).
- **Effort:** Small

---

### Issue 4 — Calculation error: Restricted-activity days

- **Type:** Calculation error
- **Where:** methodology.html line 638 (health impact functions mono-block)
- **What:** The stated calculation `0.072 × 3.58` for 4,200,000 people yields:
  ```
  4,200,000 × 0.072 × 3.58 = 302,400 × 3.58 = 1,082,592 days
  ```
  The document states `1,082,016 days`. The discrepancy is **576 days** (1,082,592 − 1,082,016).
- **Impact on cost line:** At $96/day, a 576-day error = $55,296 — immaterial at the $103.9M scale. The rounded cost figure is the same either way ($103.9M).
- **Fix:** Verify the exact BenMAP rate used (the rate in the document may be rounded; the source rate may differ at higher precision). Correct the day count or annotate the intermediate rounding.
- **Effort:** Small

---

### Issue 5 — Rounding inconsistency: Base total shown as $546M instead of $546.2M

- **Type:** Rounding inconsistency
- **Where:** methodology.html line 649 (`Base total: $546M`)
- **What:** The five rounded per-line dollar figures displayed directly above the total sum to:
  ```
  $194.8M + $43.3M + $10.6M + $193.6M + $103.9M = $546.2M
  ```
  The "Base total" line shows `$546M`. A reader summing the line items will get $546.2M, creating an apparent $0.2M discrepancy. The issue arises because the total is rounded to the nearest whole million while the components are rounded to one decimal place.
- **Fix:** Either change `$546M` to `$546.2M` for consistency with the line items, or add a parenthetical note such as "(rounded from $546.2M)". The final range `$0.5B – $1.0B` is unaffected.
- **Effort:** Small

---

### Issue 6 — Framing inconsistency: Estimate vs. Number naming

- **Type:** Inconsistency
- **Where:** impact.html (uses "Estimate 01", "Estimate 02", "Estimate 03"); methodology.html (uses "Number 1", "Number 2", "Number 3")
- **What:** The two pages use different naming conventions for the same three figures. impact.html uses zero-padded "Estimate 01/02/03" as card labels. methodology.html uses "Number 1/2/3" as H2 section headings. The section labels below the H2s in methodology.html do say "Estimate: $3.9B" and "Estimate: $0.5B–$1.0B" (and "Headline Figure: $36B–$40B" for Number 1), so partial alignment exists, but the primary heading labels differ.
- **Fix:** Standardize methodology.html H2 headings to "Estimate 01 — Direct Property Destruction", "Estimate 02 — Property Value Impact", "Estimate 03 — Acute Smoke Health Cost" to match impact.html's terminology.
- **Effort:** Small

---

### Issue 7 — Missing attribution detail: Sathaye et al. on impact.html card

- **Type:** Missing attribution
- **Where:** impact.html line 602 (Card 2 expand panel source line)
- **What:** The Card 2 source reads: `Peer-reviewed study, Landscape and Urban Planning (2024)`. No author, no article title, no volume/issue/page, and no DOI are given. The methodology.html page provides the author name (Sathaye et al.) and the article title, which is sufficient for a reader to find the paper. The impact.html card omits the author entirely.
- **Fix:** Update the source line in impact.html Card 2 to read: `Sathaye et al. (2024), Landscape and Urban Planning` — matching the format used in methodology.html.
- **Effort:** Small

---

## Appendix — Numbers Confirmed Correct

The following values were verified and found to be internally consistent and arithmetically correct:

| Value | Verified |
|-------|---------|
| 6,831 + 9,418 = 16,249 | Yes |
| 6,831 × $3,310,000 = $22.61B | Yes |
| 9,418 × $1,425,000 = $13.42B | Yes |
| $22.61B + $13.42B = $36.03B | Yes |
| 2,046 × $2,367,500 × 50% = $2.42B | Yes |
| $175B × 2.2% = $3.85B ≈ $3.9B | Yes |
| 800,000 × 0.17% × 3.58 = 4,869 | Yes |
| 4,200,000 × 0.24% × 3.58 = 36,086 | Yes |
| 4,869 × $40,000 = $194.8M | Yes |
| 36,086 × $1,200 = $43.3M | Yes |
| 48,330 × $220 = $10.6M | Yes |
| UCLA Anderson CSS bar = 100% (correct anchor) | Yes |
| Moody's CSS 19% proportional to $25B midpoint / $129.5B UCLA | Yes (within 0.3pp) |
| Milliman CSS 25% proportional to $32.3B midpoint / $129.5B UCLA | Yes |
| SmokeStory CSS 29% proportional to $38B midpoint / $129.5B UCLA | Yes (within 0.3pp) |
| $0.5B–$1.0B range consistent across files | Yes |
| $3.9B consistent across files | Yes |
| 44.8 µg/m³ consistent across files | Yes |
| 4,200,000 exposed population consistent across files | Yes |
| 16,249 structure count consistent across files | Yes |

---

*End of report. Seven issues identified: none affects the headline $36B–$40B estimate or the overall $0.5B–$1.0B health cost range. All issues are Small effort to fix.*
