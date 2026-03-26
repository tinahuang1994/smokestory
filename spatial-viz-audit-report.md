# SmokeStory — Spatial Data Visualization Audit
**Date:** March 20, 2026
**Auditor:** Senior Spatial Data Visualization Review
**Files audited:** `frontend/index.html`, `pipeline/build_layer.py`, `pipeline/goes_hms.py`, `pipeline/epa_aqs.py`, `pipeline/viirs_fire.py`, `api/main.py`
**Data sources:** EPA AQS (param 88101), NOAA HMS Smoke Polygons, NASA VIIRS SNPP via FIRMS

---

## Executive Summary

SmokeStory has the bones of a credible environmental data product. The data sources are scientifically reputable, the layer architecture is logical, and the choropleth design follows EPA category conventions. But three issues fundamentally undermine the product's scientific integrity:

1. **PM2.5 is averaged across monitors rather than taking the maximum** — a direct violation of EPA AQI methodology that causes systematic undercounting of air quality severity
2. **The PM2.5 color scale fails completely for red-green colorblind users** — Good and Unhealthy appear as the same color to ~8% of male users
3. **The smoke and PM2.5 layers use the same amber color** — on a dark map they blend into a visually undifferentiated orange field that communicates nothing

The data transparency issues compound these visualization problems: NRT fire data pulls multiple days of fires into a single-date view, and there is no AI disclosure on the narrative panel.

**Scientific integrity score: 5.5 / 10. Visualization clarity score: 6 / 10.**

---

## 1. PM2.5 CHOROPLETH DESIGN

### Issue 1.1 — PM2.5 aggregation uses mean instead of EPA AQI maximum
**Severity: Critical**

This is the most consequential bug in the application. In `api/main.py` (lines 189–193), PM2.5 values are aggregated as a **mean** across all monitors in a county:

```python
pm25_by_name = (
    df.groupby(df["county"].str.lower())["arithmetic_mean"]
    .mean()       # ← daily mean across all monitors
    .to_dict()
)
```

The comment in `build_layer.py` (line 191) confirms this is intentional: *"Daily average across all monitors in county (mean, not max)"*.

The EPA AQI convention is to use the **highest single monitor reading** to represent county-level air quality. This is because protection of health requires representing the worst exposure, not the average. In practice this matters enormously:

**Example — Los Angeles County during a wildfire:**
- Monitor near Santa Monica: 8 µg/m³ (Good)
- Monitor near Chatsworth (near fire): 220 µg/m³ (Hazardous)
- Monitor in Long Beach: 45 µg/m³ (USG)
- **Mean → ~91 µg/m³ (Unhealthy)** — displayed on map
- **Max → 220 µg/m³ (Hazardous)** — what EPA AQI shows

The map will systematically show counties as one or two AQI categories healthier than they actually are during wildfire events — precisely when accurate risk communication matters most.

The commit message "Revert PM2.5 to mean: consistency between map and narrative" suggests this was reverted to keep the narrative AI prompt consistent. The right fix is to pass both values (mean for narrative context, max for AQI category) rather than compromising the public health signal.

**Recommendation:** In `api/main.py`, change `.mean()` to `.max()` for the choropleth map coloring. Separately pass `arithmetic_mean` to the narrative generator if average context is desired. Add a field `pm25_max` alongside `pm25_mean` in the feature properties so the AI can reference both. Update the legend tooltip to read "Daily maximum PM2.5 reading (EPA AQI convention)."

**Effort: Small** — changing `.mean()` to `.max()` in one line. Updating the narrative generator to accept and use a mean separately is Medium.

---

### Issue 1.2 — Color scale fails colorblind users (see Section 6 for full analysis)
**Severity: Critical**

The six-category scale (green → yellow → orange → red → purple → dark purple) causes Good and Unhealthy to appear identical to users with deuteranopia (the most common form of colorblindness, affecting ~8% of males). See Section 6 for full colorblindness analysis and recommended alternatives.

---

### Issue 1.3 — The "Moderate" category spans an 26 µg/m³ range with no visual sub-gradation
**Severity: Important**

The current breakpoints:
```
Good:       0–9.0 µg/m³    (range: 9 µg/m³)
Moderate:   9.0–35.4 µg/m³ (range: 26.4 µg/m³)   ← 3× wider than Good
USG:        35.4–55.4 µg/m³ (range: 20 µg/m³)
```

A county at 10 µg/m³ (barely moderate, safe for most people) and a county at 34 µg/m³ (approaching the sensitive groups threshold) both display as the same yellow. This makes the scale accurate at category boundaries but misleading within the Moderate and Unhealthy bands, which are the most common conditions across most California counties on most days.

**Recommendation:** Consider adding a hover tooltip on county polygons that shows the exact PM2.5 value alongside the category label (this is already recommended in the UX audit). Users can then see the precise value rather than relying solely on the categorical color. If sub-gradation is desired, use a graduated fill opacity within each category (e.g., 0.45–0.65 for Moderate based on position within the range).

**Effort: Small** (tooltip already recommended) / **Medium** (opacity sub-gradation)

---

### Issue 1.4 — The breakpoints are scientifically defensible but worth documenting
**Severity: Nice to have**

The breakpoints in `pm25Color()` and `pm25BadgeClass()` correctly implement the **2024 EPA PM2.5 NAAQS revision** (updated February 2024, which lowered the Good/Moderate boundary from 12 to 9 µg/m³). This is current and correct. However:

- The info tooltip (layer control) does state these thresholds and their EPA provenance, which is good
- The legend on the map uses simplified notation: "Good (0–9)" without the µg/m³ unit in each row
- Nowhere does the product explain that the 2024 thresholds are *stricter* than what most AQI apps/sites still use — for users accustomed to other AQI sources, the data may appear more alarming than expected (a county they usually see as "Good" may now show as "Moderate")

**Recommendation:** Add a one-line footnote in the legend: *"Uses revised 2024 EPA PM2.5 thresholds."* This positions SmokeStory as scientifically current rather than appearing to "disagree" with other data sources.

**Effort: Small**

---

### Issue 1.5 — Sequential color scale choice is appropriate; use of a rainbow scheme is not
**Severity: Important**

The data is clearly sequential (more PM2.5 = worse health outcome), so a sequential color scheme is correct. However, the current multi-hue scale (green → yellow → orange → red → purple) is functionally a rainbow/spectral scheme. Rainbow color scales are well-documented in the visualization science literature as perceptually non-linear — the human eye does not perceive equal steps in PM2.5 as equal visual distances between these hues.

Additionally, the semantic associations break down: purple conventionally signals "cold" or "special" in Western contexts, not "extreme danger." The transition from red to purple for the two worst categories is perceptually counterintuitive — darker should mean worse for sequential hazard data, but dark purple does not feel categorically different from red to most viewers.

**Recommendation:** Adopt a sequential scale that is perceptually monotonic AND works under colorblindness constraints. The best option for this dark-themed map is a **light-to-dark single-hue or two-hue diverging-like sequential scale**:

Option A (EPA AirNow-adjacent, colorblind-friendly):
```
Good:          #00e0be  (teal/cyan)
Moderate:      #f5d800  (yellow)
USG:           #f5820a  (orange)
Unhealthy:     #d44315  (burnt orange-red)
Very Unhealthy:#8b0a50  (deep maroon-magenta)
Hazardous:     #4a0030  (near-black deep plum)
```

Option B (luminance-decreasing, strong colorblind contrast):
```
Good:          #fffb96  (pale yellow, high luminance)
Moderate:      #f6c83c  (golden yellow)
USG:           #e87722  (orange)
Unhealthy:     #c62b2b  (red)
Very Unhealthy:#7b2290  (purple, but high contrast with red)
Hazardous:     #300940  (near-black)
```

Both options eliminate the green → red problem that fails for red-green colorblindness.

**Effort: Small** (update 6 hex values in the `pm25Color()` function + legend swatches)

---

## 2. SMOKE PLUME VISUALIZATION

### Issue 2.1 — Smoke and PM2.5 layers use identical amber color
**Severity: Critical**

In `api/main.py` (map_smoke route) and the frontend style, smoke plumes are rendered as:
```js
fillColor: '#f97316',   // amber — SAME as the PM2.5 USG color
color: '#fb923c',       // lighter amber stroke
```

The PM2.5 USG county fill is also `#f97316`. When a USG county has smoke overhead — which is precisely when the data is most meaningful — the two layers merge visually into a single homogeneous amber region. The smoke polygon boundary is at `weight: 1, opacity: 0.7` and will be partially obscured by the county fill of the same color underneath.

On a dense smoke day like September 9, 2020, much of California's Central Valley would have both high PM2.5 (orange county fills) and HMS smoke polygons (also orange) stacked on each other, producing an unreadable orange blur.

**Recommendation:** Give smoke a distinctly different hue that reads as "atmospheric/aerial" rather than "ground-level measurement." Recommended approach:

```js
// Smoke plumes: blue-gray family — visually reads as "sky" or "haze"
fillColor: '#7ba7bc',   // steel blue
color: '#a8c5d4',       // lighter blue stroke
// Keep existing opacity-by-density logic (0.2/0.4/0.6)
```

This provides: (1) clear visual separation from the amber PM2.5 layer, (2) intuitive reading — blue-gray = atmospheric haze, orange = ground danger, (3) better colorblind performance (blue is preserved in all common colorblindness types).

Update the layer dot in the control from `#fb923c` to `#7ba7bc`, update the legend, and update the info tooltip color references.

**Effort: Small** (change 2 hex values in the frontend smoke style + layer dot)

---

### Issue 2.2 — Density differentiation relies solely on opacity; insufficient at light/medium levels
**Severity: Important**

The three density levels are:
```js
if (density includes 'heavy' || density === '3') return 0.6;   // fillOpacity
if (density includes 'medium' || density === '2') return 0.4;
return 0.2;  // light (default)
```

The difference between fillOpacity 0.2 and 0.4 over the CARTO dark basemap is subtle. Light smoke at 0.2 opacity is nearly invisible. At the same time, "light" HMS smoke still represents real atmospheric haze that correlates with air quality impacts. The visual signal underrepresents light smoke.

Additionally, the HMS density classification has only three levels (Light/Medium/Heavy), which maps to three opacity levels — but the opacity range (0.2–0.6) isn't spread evenly across the perceptual range. The JND (just noticeable difference) for opacity in semi-transparent fills is approximately 0.1–0.15; the difference between 0.2 and 0.4 may not be immediately obvious when viewing the full map.

**Recommendation:**
- Raise the floor: Light → 0.28, Medium → 0.45, Heavy → 0.65
- Add stroke width variation alongside opacity: Light → `weight: 0.5`, Medium → `weight: 1`, Heavy → `weight: 1.5` — stroke thickness provides a second perceptual channel beyond opacity

**Effort: Small**

---

### Issue 2.3 — Smoke polygon geometry is not clipped to California before serving
**Severity: Important**

`goes_hms.py` downloads the full HMS smoke shapefile for the given date — this is a nationwide dataset covering the contiguous US. The `get_smoke_polygons()` function returns all smoke polygons without geographic filtering. The frontend renders whatever geometry the API returns.

During major western wildfire events, the HMS shapefile will contain polygons covering the entire western US. The Leaflet `geoJSON()` layer will render all of them, including those crossing into Nevada, Oregon, and Arizona. This creates:
1. Performance overhead from rendering many non-California polygons
2. Visual confusion — smoke from Oregon fires will appear on a map described as "California Wildfire Smoke Intelligence"
3. Potential misattribution of smoke origins

**Recommendation:** In `goes_hms.py` or the `map_smoke` API route, clip to a California bounding box before returning:
```python
# Clip to California + buffer
CA_BBOX = (-124.5, 32.4, -113.9, 42.1)
gdf = gdf.cx[CA_BBOX[0]:CA_BBOX[2], CA_BBOX[1]:CA_BBOX[3]]
```

Or use a California state polygon for a more precise clip.

**Effort: Small** (add one `.cx[]` filter in the API route)

---

### Issue 2.4 — Smoke layer does NOT distinguish between satellite-detected smoke at altitude vs. ground-level impact
**Severity: Important**

The HMS smoke polygons show where NOAA analysts observed smoke in GOES satellite imagery. This is atmospheric smoke — it may be at 500m altitude (impacting ground-level air) or 8,000m altitude (not impacting ground). The info tooltip correctly notes this distinction, but the visual rendering treats all smoke as equally relevant to ground-level air quality.

This creates a systematic misleading: counties may appear covered by "smoke" (amber polygon) with relatively clean PM2.5 readings — because the smoke is high in the atmosphere and hasn't mixed down. The opposite is also true.

**Recommendation:** Surface the smoke-PM2.5 disconnect more visually. If a county has HMS smoke AND high PM2.5, show a stronger visual signal. If it has HMS smoke but low PM2.5, show the smoke more faintly (representing "atmospheric but not yet ground-level"). This requires a spatial join already available in `build_layer.py` (the `has_smoke` and `smoke_density` fields). The frontend could modulate smoke polygon opacity based on whether the underlying county has elevated PM2.5.

**Effort: Medium** (requires passing smoke-PM2.5 correlation to the frontend rendering logic)

---

## 3. FIRE MARKER DESIGN

### Issue 3.1 — FRP size bins have a ceiling at 10 MW that is orders of magnitude too low
**Severity: Important**

```js
const size = frp > 10 ? 26 : frp > 2 ? 18 : 12;
```

VIIRS SNPP FRP values for California wildfires during active burning:
- Camp Fire peak: ~40,000+ MW
- Dixie Fire peak: ~30,000+ MW
- Typical large fire: 1,000–15,000 MW
- Small vegetation fire: 2–50 MW
- Campfire: < 2 MW

The "large" threshold of 10 MW will classify nearly every significant wildfire as "large." A 10 MW fire is a small vegetation fire. A 40,000 MW major wildfire shows the same 26px icon. The size encoding is effectively meaningless for any map depicting wildfire events — it will always show the maximum size for all significant fires.

**Recommendation:** Use logarithmic FRP binning that reflects the actual distribution of wildfire FRP values:
```js
const size = frp > 1000 ? 28    // Major wildfire (> 1,000 MW)
           : frp > 100  ? 22    // Large fire (100–1,000 MW)
           : frp > 10   ? 16    // Moderate fire (10–100 MW)
           : frp > 1    ? 11    // Small fire (1–10 MW)
           :               7;   // Very small / campfire (< 1 MW)
```

This better reflects actual operational FRP distributions in California wildfire contexts.

**Effort: Small** (update 3 threshold values in frontend JS)

---

### Issue 3.2 — NRT fire data for recent dates pulls a multi-day window, not a single day
**Severity: Critical**

In `api/main.py` (lines 128–144):
```python
if days_ago <= 10:
    day_range = max(1, days_ago + 1)  # e.g., if 3 days ago: day_range=4
    df = get_active_fires(BBOX, day_range)
```

The FIRMS NRT API returns all fire detections within the last `day_range` days. If the user selects "3 days ago," the API fetches 4 days of fire data and displays all of it on the map as if it were fires from that single date. A fire that burned on Day 1 but was extinguished by Day 3 will appear on the map for Day 3.

For historic events like the Camp Fire (November 8, 2018), this doesn't apply (uses archive endpoint). But for any date within the last 10 days, the fire layer is systematically showing MORE fires than actually existed on that date — in some cases 4–10× more fire detections.

**Recommendation:** For the NRT endpoint, calculate the actual offset date and use the FIRMS area endpoint with a specific date rather than a day range. Or use `day_range=1` exclusively and switch to archive at day 2. If multi-day NRT must be used, add a prominent disclaimer on the fires layer: *"Showing fire detections from the past [N] days"* rather than the single selected date.

**Effort: Medium** — requires logic change in `api/main.py` NRT fire fetching, or adding date filter on the returned DataFrame.

---

### Issue 3.3 — Animated flame icons have a performance penalty at large fire counts
**Severity: Nice to have**

Each fire point renders as a CSS-animated `div` with a radial gradient, a pseudo-element with `filter: blur()`, and a cycling `transform` animation at 0.8–1.2s intervals. At low fire counts (< 50), this is fine. During active wildfire seasons (August–October), VIIRS may detect 500–2,000+ fire points in California's bounding box within a day. 500+ simultaneously-animating CSS elements with `filter: blur()` will cause significant browser paint cost and may drop to < 30fps on lower-end hardware.

The animation is also arguably misleading as a visualization: all fires animate at approximately the same rate regardless of FRP, implying similar dynamism. A 40,000 MW inferno and a 2 MW brush fire flicker at the same speed.

**Recommendation:**
1. Add a maximum fire point threshold: if count > 200, switch to static circle markers or `L.circleMarker()` with fill color based on FRP (red-to-yellow-to-white heat scale), with animation reserved for the top-N fires by FRP
2. Scale animation speed to FRP: higher FRP → faster flicker duration (already partially implemented via `flickerDurations` array cycling, but it's random rather than FRP-based)
3. Consider using `L.canvas()` renderer for fire points when count > 100 — dramatically improves performance for many point features

**Effort: Medium**

---

## 4. LAYER INTERACTION & OVERLAP

### Issue 4.1 — All three layers share the warm/orange color family, making simultaneous display illegible
**Severity: Critical**

When all three layers are active simultaneously — the intended default state — the color overlap creates visual noise that defeats the purpose of showing three distinct data sources:

| Layer | Color | Opacity |
|---|---|---|
| PM2.5 USG county | `#f97316` amber | 0.65 fill |
| Smoke plume (medium) | `#f97316` amber | 0.40 fill |
| Fire marker | yellow-red CSS gradient | full opacity |

A county in the "Unhealthy for Sensitive Groups" range with a medium smoke plume overhead and an active fire will display as a uniformly saturated orange-yellow zone. The three layers — each representing a fundamentally different measurement (ground sensor, satellite atmosphere, satellite thermal) — collapse into visual noise.

**Recommendation:** Implement a distinct visual language for each layer as a system:

| Layer | Proposed Color | Rationale |
|---|---|---|
| PM2.5 counties | Orange-red sequential (see Issue 1.5) | "Ground danger" — warm, urgent |
| Smoke plumes | Blue-gray/steel (`#7ba7bc`) | "Sky/atmospheric" — cool, diffuse |
| Fire points | White-core flame (keep existing CSS) | "Point source heat" — bright, discrete |

This three-way visual separation (warm ground / cool atmosphere / bright point) immediately communicates the multi-dimensional nature of the data.

**Effort: Small** (color changes as described in Issues 1.5 and 2.1)

---

### Issue 4.2 — Recommended layer z-order is correct; layer exclusivity is not needed
**Severity: Nice to have**

The current z-order (PM2.5 bottom → smoke middle → fires top) is correct from a cartographic standpoint. Fires should be visible on top; smoke represents areal coverage and should be below discrete fire points; PM2.5 counties provide geographic context at the base.

However, all three layers share the same Leaflet `addLayer/removeLayer` pattern without explicit `pane` assignment. Leaflet uses a single "overlayPane" for all GeoJSON layers by default, which means layer order is determined solely by add order and `bringToFront()` calls. This is fragile — a subsequent `addLayer` call for PM2.5 (e.g., on date change) will put it on top of smoke.

**Recommendation:** Assign Leaflet map panes explicitly:
```js
map.createPane('pm25Pane');    map.getPane('pm25Pane').style.zIndex = 400;
map.createPane('smokePPane');  map.getPane('smokePPane').style.zIndex = 450;
map.createPane('firesPPane');  map.getPane('firesPPane').style.zIndex = 500;

// In each L.geoJSON() call:
L.geoJSON(geojson, { pane: 'pm25Pane', ... })
```

**Effort: Small**

---

## 5. SCALE & RESOLUTION ISSUES

### Issue 5.1 — County-level aggregation masks within-county variability critical for wildfire events
**Severity: Important**

California's 58 counties range from 47 sq miles (San Francisco) to 20,000+ sq miles (San Bernardino — larger than Connecticut and Rhode Island combined). The county-level choropleth assigns one color to Inyo County (10,227 sq miles), which could have wildfire smoke at 300 µg/m³ in its northern half and pristine air at 3 µg/m³ in its southern Death Valley portion.

This is an inherent limitation of county-level aggregation, but it's worth communicating. For wildfire products used by journalists and public health professionals, sub-county spatial precision is often required.

**Recommendation:** Add to the legend footnote or the PM2.5 info tooltip: *"Data represents the [maximum/mean] reading from EPA monitors in each county. Counties without monitors appear as 'No data.' Sub-county spatial variation is not shown."* If resources allow, consider supplementing EPA AQS with PurpleAir sensor data (which has much denser spatial coverage, especially in populated areas) for counties where EPA monitor density is low.

**Effort: Small** (disclaimer text) / **Large** (PurpleAir integration)

---

### Issue 5.2 — Counties without EPA monitors display as "no data" but may have significant smoke
**Severity: Important**

Many rural California counties — precisely those most often in the path of major wildfire smoke — have few or zero EPA AQS FRM/FEM monitors. Alpine County has one or zero. Del Norte, Trinity, Modoc, and Plumas counties frequently have limited monitoring coverage.

The result is a systematic data gap: rural counties that bear disproportionate wildfire smoke burden appear as dark "no data" polygons on the map. This is epidemiologically and journalistically misleading — it implies clean air or unknown conditions, when the HMS smoke layer may be showing those same counties fully covered in heavy smoke.

**Recommendation:**
1. When a county has `pm25_mean == null` but `has_smoke == true` (from the spatial join in `build_layer.py`), apply a distinct visual treatment — a hatched/striped fill or a different color — to signal "no monitor data, but satellite smoke detected." The field `has_smoke` and `smoke_density` are already computed in `build_layer.py` for this purpose.
2. Add a legend entry: *"No EPA monitor data (smoke may still be present)"* with the appropriate pattern/color.

**Effort: Medium** — requires adding a hatched pattern as a Leaflet `fillPattern` plugin or SVG pattern, plus updating the legend.

---

### Issue 5.3 — EPA AQS parameter 88101 (FRM/FEM) excludes lower-cost continuous monitors
**Severity: Nice to have**

`epa_aqs.py` uses `"param": "88101"` — the FRM (Federal Reference Method) and FEM (Federal Equivalent Method) PM2.5 monitors. These are the gold standard for regulatory compliance but are expensive to operate and sparsely deployed. The EPA AQS also contains `"param": "88502"` (PM2.5 non-FRM/non-FEM, including lower-cost sensors that many agencies are now deploying).

Using only 88101 means the spatial coverage on any given day is limited to the ~80–120 regulatory monitors in California. Including 88502 would increase coverage, though with reduced measurement precision.

**Recommendation:** This is a data quality vs. coverage trade-off. For a public-facing journalism product, maintaining the 88101-only approach and clearly disclosing it is defensible. The more impactful improvement would be adding PurpleAir data as a supplementary source for counties lacking AQS coverage.

**Effort: Small** to evaluate / **Large** to implement PurpleAir integration

---

## 6. COLOR ACCESSIBILITY

### Full Colorblindness Analysis of the PM2.5 Scale

The current colors and their approximate appearance under the three main colorblindness types:

| Category | Hex | Normal | Deuteranopia (6% males) | Protanopia (2% males) | Tritanopia (0.01%) |
|---|---|---|---|---|---|
| Good | #22c55e | Bright green | Yellow-brown | Brownish | Teal-cyan |
| Moderate | #eab308 | Golden yellow | Yellow-brown | Yellow-orange | **Pink-red** |
| USG | #f97316 | Orange | Yellow-olive | **Yellow-orange** | **Pink-red** |
| Unhealthy | #ef4444 | Red | **Yellow-brown** ← SAME AS GOOD | Yellow-orange | **Pink-red** |
| Very Unhealthy | #a855f7 | Purple | Blue-gray | Blue | Pink |
| Hazardous | #7e22ce | Dark purple | Dark blue | Dark blue | Dark pink |

**Critical failures:**
- **Deuteranopia:** Good (#22c55e) and Unhealthy (#ef4444) appear nearly identical (both desaturate to yellow-brown). A user cannot distinguish the safest and most dangerous categories.
- **Protanopia:** Similar to deuteranopia — Moderate, USG, and Unhealthy appear as a similar yellow-orange range with no distinguishable gradient.
- **Both types:** The green start of the scale is the most problematic choice — green is specifically the color most affected by red-green colorblindness.

### Recommended Accessible Alternative

The following scale eliminates the green-red confusion while maintaining semantic intuition (bright = better, dark/intense = worse) and providing adequate contrast against the dark basemap:

```
Good:          #4ecdc4  (teal)             — "clear sky, clean"
Moderate:      #ffe66d  (pale yellow)      — "caution"
USG:           #f7a23c  (warm orange)      — "watch"
Unhealthy:     #c0392b  (deep red)         — "danger"
Very Unhealthy:#7d3c98  (violet-purple)    — "severe"
Hazardous:     #2c3e50  (near-black blue)  — "emergency"
```

Under deuteranopia:
- Teal (#4ecdc4) → teal-gray (distinct from all others)
- Yellow (#ffe66d) → yellow (preserved)
- Orange (#f7a23c) → yellow-orange (slightly different from yellow)
- Red (#c0392b) → yellow-brown (distinct from teal and dark)
- Purple (#7d3c98) → blue (distinct)
- Dark (#2c3e50) → near-black (distinct)

This provides 4–5 perceptually distinct categories even under deuteranopia.

**Alternatively**, the **viridis** colormap (blue-purple → teal → green → yellow) is specifically designed for perceptual uniformity and colorblind safety. While it requires inverting convention (dark = low, light = high rather than dark = worse), it has the advantage of being widely recognized in scientific contexts.

**Recommendation:** Adopt the teal-to-dark alternative above. Additionally, add pattern hatching or a white icon overlay on counties in the two highest categories (Very Unhealthy and Hazardous) as a redundant encoding channel that works regardless of color perception.

**Effort: Small** (6 hex value updates + legend swatches + info tooltip text)

---

## 7. LEGEND & LABELING

### Issue 7.1 — Legend lacks plain-language health impact statements
**Severity: Important**

The current legend:
```
PM2.5 µg/m³
● Good (0–9)
● Moderate (9–35)
...
```

A journalist or community member reading this legend needs to know what "Good" and "Hazardous" mean for their daily life, not just the AQI category name and number range. The technical unit (µg/m³) is unexplained.

**Recommendation:** Replace or augment the legend with a two-column design:

| Swatch | Category | What it means |
|---|---|---|
| ● | Good (0–9 µg/m³) | Safe for all |
| ● | Moderate (9–35) | Fine for most |
| ● | Sensitive Groups (35–55) | Limit outdoor time if vulnerable |
| ● | Unhealthy (55–150) | Everyone affected |
| ● | Very Unhealthy (150–250) | Avoid being outside |
| ● | Hazardous (250+) | Stay indoors |

The plain-language column can be small (0.62rem) below or beside the category name.

**Effort: Small**

---

### Issue 7.2 — No standalone legend for smoke density or fire intensity
**Severity: Important**

The layer control explains each layer via `ⓘ` info tooltip, but the map has no persistent legend for:
- Smoke density levels (light / medium / heavy opacity bands)
- Fire intensity sizing (small / medium / large flames = FRP tiers)

A user viewing the map for the first time has no way to know that a lighter-colored smoke polygon means less dense smoke, or that flame size encodes fire intensity, without clicking the `ⓘ` buttons. These are invisible affordances.

**Recommendation:** Extend the existing `#legend` panel with two additional sections below the PM2.5 scale:

**Smoke:**
```
◑ Light smoke   ◑ Medium smoke   ● Heavy smoke
```
(using filled circles of increasing size or opacity to represent the density gradient)

**Fire intensity:**
```
🔥 < 10 MW   🔥 10–100 MW   🔥 > 100 MW
```
(with scaled flame sizes matching the marker sizes on the map)

**Effort: Small**

---

### Issue 7.3 — Legend is positioned between map and panel; repositions based on panel state
**Severity: Nice to have**

```css
#legend {
    top: 70px;
    right: calc(var(--panel) + 20px);  /* moves when panel opens */
}
```

The legend moves when the county panel opens (because `--panel` is a fixed 380px offset). This is actually correct behavior — the legend shifts left to stay visible. But this means the legend's position is not stable, which can disorient users who are reading it while a county panel opens.

**Recommendation:** Pin the legend to `left: 20px; bottom: calc(190px + 20px)` (above the layer control, which already sits at `bottom: 28px; left: 20px`). This removes the dynamic repositioning and gives the left side of the map a clear control column (layer ctrl → legend → zoom), which is a conventional cartographic layout for interactive maps.

**Effort: Small**

---

## 8. DATA TRUST & TRANSPARENCY

### Issue 8.1 — No disclosure that narratives are AI-generated
**Severity: Critical**

The county narrative panel displays AI-generated text in an italic Cormorant Garamond serif — the visual language of authoritative journalism. There is no label indicating this is AI-generated content, no disclaimer about potential inaccuracies, and no indication that the narrative is synthesized from data rather than reported by a journalist.

The footer mentions "Claude AI" in small monospace text alongside data sources, but this is insufficient disclosure for a product that presents AI-generated text with the visual weight of editorial writing. Given ongoing public discourse about AI in newsrooms, this is both an ethical issue and a potential credibility risk.

**Recommendation:** Add a visible label immediately above or below the narrative text: *"AI-generated interpretation · Not editorial content"* or *"Generated by Claude AI based on EPA/NOAA data. May contain inaccuracies."* Use a slightly different typography treatment (e.g., monospace for the disclaimer) to visually distinguish it from the narrative text.

**Effort: Small**

---

### Issue 8.2 — NRT fire data is multi-day but displayed as single-date; no timestamp shown
**Severity: Critical**

As identified in Issue 3.2, the NRT fire endpoint returns data from a day range (e.g., 4 days of fire detections) displayed as if it were a single-day snapshot. Additionally, there is no data freshness timestamp anywhere in the map UI.

For any environmental journalism product, the provenance of time-sensitive data must be displayed. A user viewing "fires for January 6, 2026" needs to know: (1) is this data from 3 hours ago or 36 hours ago? (2) Is this showing fires that burned on that specific date only?

**Recommendation:**
1. Fix the NRT multi-day aggregation (Issue 3.2)
2. Add a "Data as of [timestamp]" indicator near the loading indicator or in the header. The FIRMS API response includes `acq_date` and `acq_time` per detection — use the most recent to construct a "last updated" timestamp for the fires layer
3. Similarly, the HMS smoke polygons have daily granularity but no timestamp indicating when the analyst product was generated. Add "HMS analysis date: [date]" to the smoke layer's info tooltip

**Effort: Medium**

---

### Issue 8.3 — SSL verification disabled on Census and county GeoJSON requests
**Severity: Important**

In `build_layer.py` (line 54):
```python
resp = requests.get(COUNTIES_URL, verify=False, timeout=120)
```
And in `api/main.py` (line 174):
```python
resp = requests.get(CA_COUNTIES_URL, verify=False, timeout=30)
```

`verify=False` disables SSL certificate verification. This means the app cannot detect if a man-in-the-middle attack is substituting malicious GeoJSON for the county boundaries. For a county boundary file used to spatially join PM2.5 readings, a tampered GeoJSON could cause misattributed data (County A's air quality shown for County B). For a public health product, this is a non-trivial concern.

**Recommendation:** Remove `verify=False` and properly configure SSL. If the issue is a corporate proxy or expired intermediate certificate, the fix is to provide the correct CA bundle via `verify='/path/to/ca-bundle.crt'`. As a fallback, download the Census shapefile once and bundle it with the application rather than fetching it at runtime.

**Effort: Small** (certificate fix) / **Medium** (bundle shapefile locally)

---

### Issue 8.4 — PM2.5 data limitations not communicated in the product UI
**Severity: Important**

Key EPA AQS limitations that users cannot know from the current UI:
- **Monitor coverage gaps:** Many rural counties appear as "No data" not because air is clean, but because no regulatory monitor exists
- **Measurement timing:** The EPA `dailyData/byState` endpoint returns the 24-hour daily average (midnight to midnight local time). Today's data may not be complete until the following morning
- **Measurement method:** Parameter 88101 is FRM/FEM only — the most accurate method, but sparsely deployed
- **Historical archive latency:** EPA AQS data for a given day becomes fully finalized and available in the API approximately 2–6 months after collection. "Recent historical" dates (within 60–90 days) may have incomplete data

**Recommendation:** Add an expandable "Data Notes" section to the layer info tooltips. For PM2.5 specifically:
*"Data from EPA regulatory monitors (FRM/FEM, parameter 88101). Counties without EPA monitors show 'No data.' Daily values are 24-hour averages; today's data may be preliminary. Monitor density varies by county — rural counties may have limited or no coverage. Source: EPA Air Quality System (AQS). Data finalization may lag by 2–6 months for recent dates."*

**Effort: Small** (text addition to existing tooltip)

---

### Issue 8.5 — HMS smoke polygons for current dates may reflect next-day data
**Severity: Nice to have**

The NOAA HMS smoke product is an analyst-derived product updated approximately once daily (typically by mid-afternoon Pacific time). When a user selects "today," the HMS data returned may be from the previous day's analysis cycle, or may be partial. The `goes_hms.py` module does not handle 404 errors distinctly from other errors — if today's HMS file hasn't been published yet, it will fail silently and the user sees no smoke layer with no explanation.

**Recommendation:** Add logic to try the previous day's HMS data when today's returns a 404, with a note in the UI: *"Smoke data from [yesterday's date] — today's analysis not yet available."* This is better than silently showing no smoke layer.

**Effort: Small**

---

## Priority Action Matrix

| Priority | Issue | Area | Effort |
|---|---|---|---|
| 🔴 Critical | 1.1 — Mean instead of max PM2.5 aggregation | Data | Small |
| 🔴 Critical | 3.2 — NRT fires shows multiple days as one date | Data | Medium |
| 🔴 Critical | 4.1 / 2.1 — Smoke + PM2.5 same amber color, unreadable | Viz | Small |
| 🔴 Critical | 6 — Green-red colorblind failure (Good = Unhealthy) | Accessibility | Small |
| 🔴 Critical | 8.1 — No AI-generated content disclosure | Trust | Small |
| 🟠 Important | 3.1 — FRP size bins ceiling too low (10 MW) | Viz | Small |
| 🟠 Important | 2.3 — HMS data not clipped to California | Data | Small |
| 🟠 Important | 5.2 — Rural counties with smoke show as "no data" | Data/Viz | Medium |
| 🟠 Important | 2.2 — Smoke density opacity range too narrow | Viz | Small |
| 🟠 Important | 1.5 — Rainbow scale is perceptually non-linear | Viz | Small |
| 🟠 Important | 7.1 — Legend lacks plain-language health impact | UX | Small |
| 🟠 Important | 7.2 — No persistent legend for smoke/fire layers | UX | Small |
| 🟠 Important | 8.2 — No data freshness timestamp on map | Trust | Medium |
| 🟠 Important | 8.3 — SSL verification disabled | Security | Small |
| 🟠 Important | 8.4 — PM2.5 data limitations not communicated | Trust | Small |
| 🟠 Important | 2.4 — Smoke altitude vs. ground impact not visually encoded | Viz | Medium |
| 🟠 Important | 4.2 — Leaflet panes not assigned; z-order is fragile | Code | Small |
| 🟡 Nice to have | 1.3 — Moderate category range too wide for single color | Viz | Small |
| 🟡 Nice to have | 1.4 — 2024 thresholds not flagged as different from older AQI apps | Trust | Small |
| 🟡 Nice to have | 3.3 — Flame animation performance at high fire counts | Perf | Medium |
| 🟡 Nice to have | 5.1 — County-level aggregation variability not disclosed | Trust | Small |
| 🟡 Nice to have | 5.3 — 88101-only excludes lower-cost sensors | Data | Large |
| 🟡 Nice to have | 7.3 — Legend repositions when panel opens | UX | Small |
| 🟡 Nice to have | 8.5 — HMS 404 should fall back to previous day | Data | Small |

---

## Recommended Sprint Breakdown

### Sprint 1 — Critical Data Integrity (1 day)

**These must be fixed before any public launch.**

1. **Fix PM2.5 aggregation**: change `.mean()` to `.max()` in `api/main.py` line 191
2. **Fix NRT fire multi-day accumulation**: add date filter or switch to `day_range=1` plus archive fallback
3. **Add AI narrative disclosure**: one-line label above/below the narrative text
4. **Clip HMS smoke to California**: add `.cx[]` filter in `map_smoke` API route

### Sprint 2 — Color System Overhaul (1–2 days)

**The single highest-impact visual improvement.**

1. **Adopt new PM2.5 color scale** (teal → yellow → orange → deep red → purple → near-black): update 6 hex values in `pm25Color()`, `pm25BadgeClass()`, and legend swatches
2. **Adopt new smoke layer color** (blue-gray `#7ba7bc`): update `fillColor` and `color` in smoke GeoJSON style + layer control dot
3. **Fix FRP size bins**: update threshold values (10 MW → 100/1000 MW bands)
4. **Assign Leaflet panes**: add `createPane()` calls to guarantee z-order

### Sprint 3 — Legend & Trust Layer (1 day)

1. Add plain-language health impact to legend rows
2. Add smoke density + fire intensity sub-legends
3. Add "Data Notes" to PM2.5 info tooltip
4. Add data freshness timestamp (fires: most recent `acq_date`; smoke: file date)
5. Add "2024 EPA thresholds" footnote to legend
6. Fix SSL verification (`verify=False` → proper CA bundle)

### Sprint 4 — Data Gap Visualization (2–3 days)

1. Visual treatment for counties with `has_smoke=true` but `pm25_mean=null` (hatched fill)
2. Add "no monitor data" legend entry
3. HMS 404 fallback to previous day with UI note
4. Fire animation performance optimization (canvas renderer above threshold)

---

## Appendix: Data Source Summary

| Source | Pipeline file | API endpoint | What it provides | Key limitation |
|---|---|---|---|---|
| EPA AQS | `epa_aqs.py` | `/map/pm25/06/{date}` | Ground-level PM2.5, 24h daily average | Sparse coverage; uses mean not max |
| NOAA HMS | `goes_hms.py` | `/map/smoke/{date}` | Atmospheric smoke polygons (3 density levels) | Altitude unknown; nationwide, not CA-clipped |
| NASA FIRMS/VIIRS | `viirs_fire.py` | `/map/fires/{date}` | Thermal fire detections with FRP | NRT is multi-day; FRP bins miscalibrated |
| Census TIGER | `build_layer.py` | (internal) | California county boundaries | SSL disabled; fetched at runtime |
| Click That Hood GeoJSON | `api/main.py` | (internal) | Alternative CA county boundaries | SSL disabled; external dependency |
