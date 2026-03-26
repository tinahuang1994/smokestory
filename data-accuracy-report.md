# SmokeStory Data Accuracy Audit Report

**Date:** 2026-03-20
**Auditor:** Automated API cross-reference audit
**API Base:** https://smokestory.onrender.com

---

## Executive Summary

Five tests were run against the live API covering LA Fires (Jan 2025), the Camp Fire (Nov 2018), the 2020 smoke season, edge-case counties, and historical coverage. One **Critical** bug was identified involving dangerously incorrect PM2.5 data for Butte County on the Camp Fire day. Two **Important** issues were found related to data coverage gaps. Two **Minor** issues were found in error handling.

---

## TEST 1 — LA Fires (January 9, 2025)

**Endpoints:**
- `GET /map/pm25/06/20250109`
- `GET /map/smoke/20250109`
- `GET /map/fires/20250109`
- `GET /county/06/Los%20Angeles/20250109` *(additional verification)*

### Findings

#### 1a. PM2.5 — Los Angeles County

**Result: PARTIAL PASS / IMPORTANT ISSUE**

| Source | Value | Classification |
|---|---|---|
| `/map/pm25/06/20250109` GeoJSON | **LA County ABSENT** | — |
| `/county/06/Los%20Angeles/20250109` | **44.85 µg/m³** | Unhealthy for Sensitive Groups |

- The `/map/pm25` GeoJSON returns only ~21 of California's 58 counties. Los Angeles County is **entirely absent from the map layer**, meaning the map would display no PM2.5 dot or color for LA on one of the worst air quality days in California history.
- The `/county` endpoint **does** return valid data (44.85 µg/m³), confirming the data exists in the database but is not surfacing in the map GeoJSON.
- **Counties returned in map GeoJSON on 20250109:** Calaveras (11.61), Colusa (2.01), Fresno (14.79), Humboldt (12.0), Inyo (4.07), San Diego (5.21), and ~15 others — none from the LA/SoCal core.
- PM2.5 of 44.85 µg/m³ for LA County: the classification ("Unhealthy for Sensitive Groups") is **correct** per 2024 EPA AQS standards (threshold 35.5 µg/m³). The value itself is a county-wide daily mean and plausible given that large parts of the county (Long Beach, downtown) were less directly impacted than fire zones (Palisades, Altadena). However, the satellite smoke_density for LA is reported as **"Light"** despite the Palisades and Eaton fires producing dense smoke — this classification appears inconsistent with satellite imagery from that date.

**Anomalies:**
- LA County absent from map GeoJSON despite having monitor data.
- Smoke density "Light" for LA County on Jan 9, 2025 appears incorrect; satellite imagery shows heavy smoke over the LA Basin.
- San Francisco returns `pm25_mean: null` for this date despite having 7+ active EPA monitors. Narrative acknowledges the gap ("Ground-based PM2.5 monitoring data is not available") but the root cause of why SF monitors are not being ingested warrants investigation.

**Severity: Important** — the map would appear blank for LA County on a major wildfire day; county drill-down works correctly.

---

#### 1b. Smoke Polygons (Jan 9, 2025)

**Result: PASS**

- `GET /map/smoke/20250109` returns **65 features** with Light, Medium, and Heavy density classifications.
- Coverage spans from the Pacific Coast (~−127°W) to −75°W, with timestamps spanning 12:30–23:50 UTC from both GOES-WEST and GOES-EAST.
- Presence of smoke polygons over the LA region is consistent with the active fires.

**Severity: N/A (Pass)**

---

#### 1c. Fire Points (Jan 9, 2025)

**Result: PASS**

- `GET /map/fires/20250109` returns **1,085 fire detection points** statewide.
- Intense clustering near Los Angeles at **−118.54°W, 34.09°N** (consistent with Palisades Fire location).
- Peak FRP values reach **289.24 MW** in the LA cluster; brightness values peak at **367 K** — consistent with an intense active wildfire.
- Additional detections span the state from Nevada border to coastal regions.

**Severity: N/A (Pass)**

---

## TEST 2 — Camp Fire (November 8, 2018)

**Endpoints:**
- `GET /map/pm25/06/20181108`
- `GET /map/smoke/20181108`
- `GET /map/fires/20181108`
- `GET /county/06/Butte/20181108` *(additional verification)*

### Findings

#### 2a. PM2.5 — Butte County

**Result: CRITICAL FAIL**

| County | API Value | API Classification | Expected (Historical Record) |
|---|---|---|---|
| **Butte** | **6.6 µg/m³** | **"Good"** | **200–600+ µg/m³ ("Hazardous")** |
| Sonoma | 78.40 µg/m³ | Unhealthy | ~50–100 µg/m³ (plausible, downwind) |
| Solano | 62.91 µg/m³ | Unhealthy for Sensitive Groups | Plausible |
| Alameda | 24.29 µg/m³ | Good | Plausible |
| San Francisco | 23.91 µg/m³ | Good | Plausible |
| Contra Costa | 28.16 µg/m³ | Good | Plausible |

**This is a critical scientific error.** The Camp Fire ignited in Butte County (near Paradise, CA) on November 8, 2018 and became the deadliest wildfire in California history. EPA monitoring stations in Chico (Butte County) recorded PM2.5 values in the range of **200–600+ µg/m³** (well into "Hazardous" category, AQI 300–500+) on this date. Multiple state and federal air quality reports confirm Butte County experienced the worst air quality in recorded California history on this day.

The API returns **6.6 µg/m³ ("Good")** — off by a factor of 30–90x.

**The county narrative is dangerously wrong:**
> "Light smoke drifted across Butte County on Thursday, with PM2.5 levels at 6.6 µg/m³... air quality posed minimal health risks, and outdoor activities remained safe for all residents, including vulnerable populations."

This narrative directly contradicts historical record. On November 8, 2018, Butte County residents were being evacuated under a Code Red emergency; the air quality was life-threatening.

**Physical implausibility:** Sonoma (78.40 µg/m³) and Solano (62.91 µg/m³) — counties located 100–150 miles *downwind* from the fire — show PM2.5 values 10x higher than Butte County at the fire's origin point. This is physically impossible. The data either: (a) failed to ingest the Butte County monitor records, (b) averaged only monitors that were unaffected or offline, or (c) has a data pipeline error for that county/date combination.

**Severity: Critical** — generates a false narrative that outdoor air was safe in an active disaster zone.

---

#### 2b. Smoke Polygons (Nov 8, 2018)

**Result: PASS**

- `GET /map/smoke/20181108` returns **136 features** with Light, Medium, and Heavy density classifications.
- Coverage spans Northern California, Oregon, Washington, Idaho, and Montana — consistent with the Camp Fire plume reaching far north and east.
- GOES-EAST observations span 14:00–01:00 UTC, providing good temporal coverage.

**Severity: N/A (Pass)**

---

#### 2c. Fire Points (Nov 8, 2018)

**Result: PASS**

- `GET /map/fires/20181108` returns fire detection points.
- Intense cluster near **Paradise/Butte County** at −121.52°W, 39.75°N with FRP values up to **447.8 MW** — among the highest in the dataset, consistent with the Camp Fire's extreme intensity.
- Sample FRP values:
  - −121.527, 39.755: 447.8 MW
  - −121.509, 39.760: 309.39 MW
  - −121.485, 39.776: 398.69 MW

Fire points are correctly localized and scientifically plausible.

**Severity: N/A (Pass)**

---

## TEST 3 — 2020 Smoke Season (September 9, 2020)

**Endpoints:**
- `GET /map/pm25/06/20200909`
- `GET /map/smoke/20200909`
- `GET /map/fires/20200909`

### Findings

#### 3a. PM2.5 — Multiple Counties

**Result: PASS**

Counties with elevated PM2.5 (>35 µg/m³):

| County | PM2.5 Mean | Classification |
|---|---|---|
| Butte | 42.51 µg/m³ | Unhealthy for Sensitive Groups |
| Calaveras | 49.50 µg/m³ | Unhealthy for Sensitive Groups |
| Fresno | 60.84 µg/m³ | Unhealthy |

September 9, 2020 was the "orange sky day" in Northern California during the record 2020 fire season. Elevated PM2.5 across multiple counties is consistent with historical reports. Values are plausible (not at Camp Fire extremes, but clearly elevated).

**Note:** As with Test 1, the map endpoint covers only a subset of California's 58 counties, so the full extent of smoke impacts may not be visible on the map layer.

**Severity: N/A (Pass)**

---

#### 3b. Smoke Polygons (Sep 9, 2020)

**Result: PARTIAL PASS / MINOR CONCERN**

- `GET /map/smoke/20200909` returns **52 features**.
- Coverage is described as concentrated in the **Pacific Northwest and Northern California** with Light, Medium, and Heavy classifications.
- September 9, 2020 was characterized by an unprecedented smoke event blanketing the entire California coast from Oregon to San Diego. The 52-feature count and geographic distribution suggest coverage may be incomplete for central and southern California relative to what satellite imagery confirmed on that date.
- GOES data is from day "2020253" (day of year 253 = September 9) — date parsing is correct.

**Severity: Minor** — smoke coverage appears geographically constrained relative to the documented statewide event.

---

#### 3c. Fire Points (Sep 9, 2020)

**Result: PASS**

- `GET /map/fires/20200909` returns **676 fire points within California** (out of a larger total statewide/regional dataset).
- High fire point count is consistent with the 2020 fire season having millions of acres burning simultaneously.

**Severity: N/A (Pass)**

---

## TEST 4 — Edge Case Counties (January 9, 2025)

**Endpoints:**
- `GET /county/06/Alpine/20250109`
- `GET /county/06/San%20Francisco/20250109`
- `GET /county/06/Imperial/20250109`
- `GET /county/06/Modoc/20250109`

### Findings

#### 4a. Alpine County — Null PM2.5 (No Monitors)

**Result: PASS**

```json
{
  "pm25_mean": null,
  "smoke_density": null,
  "has_smoke": false,
  "narrative": "...the absence of ground-based PM2.5 monitoring stations in this remote area..."
}
```

- Correctly returns `null` PM2.5 — Alpine County has no EPA monitoring stations.
- Narrative gracefully acknowledges the monitoring gap and advises residents to follow official air quality reports.
- No crash or unhelpful error.

**Severity: N/A (Pass)**

---

#### 4b. San Francisco County — Unexpected Null PM2.5

**Result: FAIL**

```json
{
  "pm25_mean": null,
  "smoke_density": null,
  "has_smoke": false,
  "narrative": "...Ground-based PM2.5 monitoring data is not available for the county today..."
}
```

- San Francisco County has **7+ active EPA AQS monitoring stations** and consistently provides PM2.5 data. The API correctly ingested SF data for November 8, 2018 (23.91 µg/m³) — demonstrating the pipeline is capable of ingesting SF data.
- Returning `null` for January 9, 2025 suggests a data ingestion gap for that specific date, not a structural absence of monitors.
- The narrative treatment is graceful (acknowledges the gap), but the underlying null is a data completeness issue.
- **Cross-check:** The `/map/pm25` GeoJSON for the same date also omits SF, confirming this is a pipeline issue, not an endpoint issue.

**Severity: Important** — SF should almost never return null PM2.5; this indicates inconsistent EPA data ingestion for certain dates.

---

#### 4c. Imperial County — Valid PM2.5

**Result: PASS**

```json
{
  "pm25_mean": 3.4989734444444447,
  "smoke_density": null,
  "has_smoke": false,
  "narrative": "...PM2.5 levels at 3.50 µg/m³, classified as 'Good'..."
}
```

- Imperial County (southeastern CA, far from LA fires) correctly shows clean air at 3.50 µg/m³ "Good."
- Narrative contextualizes the contrast with LA County conditions.
- Minor: `pm25_mean` has excessive decimal precision (16 significant figures). Consider rounding to 2 decimal places in the API response.

**Severity: N/A (Pass) / Minor (precision)**

---

#### 4d. Modoc County — Null PM2.5 (Remote County)

**Result: PASS**

```json
{
  "pm25_mean": null,
  "smoke_density": null,
  "has_smoke": false,
  "narrative": "...No smoke has been detected in the area, though the region lacks ground-based air quality monitoring stations..."
}
```

- Modoc County is one of California's most remote counties with very limited monitoring. Null PM2.5 is expected and handled gracefully.

**Severity: N/A (Pass)**

---

## TEST 5 — Historical Coverage

**Endpoints:**
- `GET /map/smoke/01`
- `GET /map/smoke/20050801`
- `GET /map/smoke/20100715`
- `GET /map/smoke/20150901`

### Findings

#### 5a. Malformed Date Input: `/map/smoke/01`

**Result: FAIL**

```json
{"type":"FeatureCollection","features":[]}
```

- The API accepts a nonsensical date string (`"01"`) and silently returns an **empty FeatureCollection** rather than an error.
- Users or frontends sending malformed dates receive no indication that their query was invalid. This could manifest as the app appearing to show "no smoke" for an invalid date rather than flagging the input error.
- Expected behavior: HTTP 400 with a descriptive error message such as `{"error": "Invalid date format. Expected YYYYMMDD."}`.

**Severity: Minor** — silent failure on invalid input; could cause user confusion.

---

#### 5b. Oldest HMS Date: `/map/smoke/20050801`

**Result: PASS (with note)**

```json
{"type":"FeatureCollection","features":[]}
```

- The HMS Smoke product originated around August 2005. August 1, 2005 is at the very start of the historical record, so an empty features array is plausible (either no data was recorded or the system hadn't yet built full coverage).
- This is not an error per se, but there is no message distinguishing "no smoke detected on this date" from "data does not exist for this date." For dates before ~August 2005, a note clarifying the coverage start date would improve UX.

**Severity: Minor** — ambiguous empty response at historical boundary.

---

#### 5c. Intermediate Date: `/map/smoke/20100715`

**Result: PASS**

- Returns **71 features** with Light/Medium/Heavy density classifications.
- Date parsed correctly (day of year 196 = July 15, 2010).
- Covers North America as expected.

**Severity: N/A (Pass)**

---

#### 5d. Recent Historical Date: `/map/smoke/20150901`

**Result: PASS**

- Returns **83 features** with Light (38), Medium (29), and Heavy (16) density classifications.
- Coverage spans continental US, Canada, and parts of Mexico.
- Date parsed correctly (day 244 = September 1, 2015).

**Severity: N/A (Pass)**

---

## Summary Table

| Test | Check | Result | Severity |
|---|---|---|---|
| 1 — LA Fires | LA County PM2.5 present in map GeoJSON | **FAIL** — absent from map layer | Important |
| 1 — LA Fires | LA County PM2.5 value (44.85 µg/m³) plausible | PASS (plausible daily mean) | — |
| 1 — LA Fires | LA County severity classification correct | PASS ("Unhealthy for Sensitive Groups") | — |
| 1 — LA Fires | LA County smoke_density classification | **CONCERN** — "Light" on peak fire day | Minor |
| 1 — LA Fires | Smoke polygons present Jan 9, 2025 | PASS (65 features) | — |
| 1 — LA Fires | Fire points present near LA | PASS (1,085 total; FRP 289 MW near Palisades) | — |
| 1 — LA Fires | San Francisco PM2.5 null on active date | **FAIL** — should have monitor data | Important |
| 2 — Camp Fire | Butte County PM2.5 value correct | **CRITICAL FAIL** — 6.6 µg/m³ vs. 200–600+ µg/m³ actual | **Critical** |
| 2 — Camp Fire | Butte County narrative accurate | **CRITICAL FAIL** — "safe to be outdoors" on disaster day | **Critical** |
| 2 — Camp Fire | Smoke polygons covering NorCal | PASS (136 features) | — |
| 2 — Camp Fire | Fire points near Paradise/Butte County | PASS (FRP up to 447 MW at correct coordinates) | — |
| 3 — 2020 Season | Multiple counties elevated PM2.5 | PASS (Butte 42.5, Calaveras 49.5, Fresno 60.8) | — |
| 3 — 2020 Season | Smoke polygons widespread in CA | PARTIAL PASS — concentrated NorCal/PNW | Minor |
| 3 — 2020 Season | Fire point count | PASS (676 in CA) | — |
| 4 — Alpine | Null PM2.5, graceful handling | PASS | — |
| 4 — San Francisco | Valid PM2.5 returned | **FAIL** — null despite active monitors | Important |
| 4 — Imperial | Valid PM2.5 returned | PASS (3.50 µg/m³) | — |
| 4 — Modoc | Null PM2.5, graceful handling | PASS | — |
| 5 — Historical | Malformed date `/smoke/01` returns error | **FAIL** — silent empty response | Minor |
| 5 — Historical | Oldest HMS date `/smoke/20050801` | PASS (empty features, expected) | — |
| 5 — Historical | `/smoke/20100715` returns data | PASS (71 features) | — |
| 5 — Historical | `/smoke/20150901` returns data | PASS (83 features) | — |

---

## Prioritized Action Items

### 🔴 Critical (Fix Immediately)

**Bug 1: Butte County PM2.5 on Camp Fire Day (Nov 8, 2018)**
- API returns 6.6 µg/m³ ("Good") — actual value was 200–600+ µg/m³ ("Hazardous")
- Counties 100+ miles downwind (Sonoma: 78.4, Solano: 62.9) show values 10x higher than the fire origin — physically impossible
- Generated narrative declares "air quality posed minimal health risks, and outdoor activities remained safe for all residents" — this is false and could mislead users researching historical events
- **Likely cause:** Monitoring stations in Butte County may have gone offline, evacuated, or malfunctioned during the fire. The pipeline averaged the surviving monitor readings (possibly from less-affected eastern parts of the county) without flagging the data as potentially unrepresentative of actual conditions.
- **Fix:** Implement a data quality flag when fewer than a threshold number of monitors are active. Cross-reference satellite-derived smoke density ("Light" smoke was present per the has_smoke field) against PM2.5 values — a "Light smoke, Good air quality" flag at a fire's origin point on day-1 should trigger a data confidence warning. Consider supplementing sparse ground monitor data with satellite-based PM2.5 estimates (e.g., from NOAA or PurpleAir) for high-smoke events.

---

### 🟡 Important (Fix Soon)

**Bug 2: LA County and Many Counties Missing from `/map/pm25` GeoJSON**
- The map endpoint returns only ~21 of 58 California counties on certain dates.
- LA County is absent from the map layer on January 9, 2025 despite having valid monitor data (confirmed via county endpoint at 44.85 µg/m³).
- The map layer is the primary visualization surface — missing counties create false "no data" impressions on the most important dates.
- **Fix:** Audit the GeoJSON construction logic in the map endpoint. Ensure all counties with monitor data are included in the FeatureCollection. Investigate whether counties are being filtered by some spatial join or threshold condition.

**Bug 3: San Francisco PM2.5 Returning Null on Active Monitoring Dates**
- SF returned `null` for Jan 9, 2025 but returned valid data (23.91 µg/m³) for Nov 8, 2018.
- SF has 7+ EPA AQS monitoring stations that should provide near-continuous data.
- **Fix:** Audit the data ingestion pipeline for date-specific gaps. Check whether AQS data for certain 2024–2025 dates is being ingested correctly. Consider adding data freshness monitoring/alerting.

---

### 🟢 Minor (Address in Upcoming Sprint)

**Bug 4: Malformed Date Input Returns Silent Empty Response**
- `GET /map/smoke/01` returns `{"type":"FeatureCollection","features":[]}` — no indication of invalid input.
- **Fix:** Add date format validation. Return HTTP 400 with `{"error": "Invalid date format. Use YYYYMMDD (e.g., 20250109)."}` for non-YYYYMMDD inputs.

**Bug 5: LA County Smoke Density "Light" on Peak Fire Day**
- LA County smoke_density is reported as "Light" on January 9, 2025. Satellite imagery shows significant smoke over the LA Basin on this date.
- **Fix:** Verify HMS smoke polygon intersection logic for the LA Basin area; confirm whether the "Light" classification comes from the intersected polygon or a fallback.

**Bug 6: Excessive Decimal Precision in PM2.5 Values**
- Imperial County returns `pm25_mean: 3.4989734444444447` — 16 significant figures is excessive and suggests a floating-point aggregation artifact.
- **Fix:** Round PM2.5 values to 2 decimal places before serialization.

---

## Data Quality Assessment

| Data Source | Coverage | Accuracy | Notes |
|---|---|---|---|
| EPA AQS PM2.5 (ground monitors) | Partial (~21/58 counties on some dates) | Poor for Camp Fire; good otherwise | Monitor outages during disasters corrupt county averages |
| HMS Smoke Polygons | Good (GOES-EAST + GOES-WEST) | Good | Density classifications appear consistent |
| VIIRS/MODIS Fire Points | Excellent | Excellent | FRP values and coordinates are scientifically plausible |
| County Narratives (AI-generated) | Good | Depends on underlying data | Faithfully reflects input data; errors propagate from bad PM2.5 |

**Overall data pipeline health:** Good for normal conditions; **unreliable during active disasters** due to monitor outages producing misleadingly low ground-truth PM2.5 averages.

---

*Report generated: 2026-03-20*
*API version tested: live production at smokestory.onrender.com*
