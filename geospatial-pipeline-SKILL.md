# Skill: Geospatial Data Pipeline

A reference for building multi-source geospatial data pipelines that fetch from government APIs, perform spatial joins, and serve GeoJSON to a Leaflet frontend. Derived from the SmokeStory wildfire smoke tracker project.

---

## 1. Project Structure

```
project/
├── pipeline/
│   ├── epa_aqs.py        # EPA Air Quality System (PM2.5 readings)
│   ├── goes_hms.py       # NOAA HMS smoke polygon shapefiles
│   ├── viirs_fire.py     # NASA FIRMS fire detection CSV
│   └── build_layer.py    # Spatial join + county layer assembly
├── api/
│   └── main.py           # FastAPI: serves GeoJSON endpoints + frontend
├── frontend/
│   └── index.html        # Leaflet map + dynamic API_BASE
└── data/
    └── counties.geojson  # Optional local cache (non-blocking if missing)
```

Each data source is isolated in its own module with a single public function. `build_layer.py` orchestrates them.

---

## 2. Fetching EPA AQS (PM2.5 Readings)

**API**: `https://aqs.epa.gov/data/api/dailyData/byState`
**Auth**: Email + key as query params (from `.env`)
**Param code**: `88101` = PM2.5

```python
# pipeline/epa_aqs.py
import os, requests
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EPA_AQS_EMAIL")
KEY   = os.getenv("EPA_AQS_KEY")

def get_pm25_readings(state_code, start_date, end_date):
    """Returns list of dicts with keys: county_code, county, arithmetic_mean, ..."""
    url = "https://aqs.epa.gov/data/api/dailyData/byState"
    params = {
        "email": EMAIL, "key": KEY,
        "param": "88101",          # PM2.5 parameter code
        "bdate": start_date,       # YYYYMMDD
        "edate": end_date,
        "state": state_code,       # e.g. "06" for California
    }
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json().get("Data", [])
    except requests.RequestException as e:
        print(f"Error fetching PM2.5 data: {e}")
        return []
```

**Key patterns:**
- Dates are `YYYYMMDD` strings (e.g. `"20240901"`)
- State codes are zero-padded FIPS: `"06"` = California
- Response is `{"Data": [...], "Header": [...]}` — always use `.get("Data", [])`
- No SSL issues on this endpoint (unlike Census)

---

## 3. Fetching NOAA HMS Smoke Polygons

**Source**: NOAA/NESDIS Hazard Mapping System
**Format**: Zipped Shapefile downloaded via HTTP
**URL pattern**: `https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/Shapefile/{year}/{month}/hms_smoke{date}.zip`

```python
# pipeline/goes_hms.py
import io, tempfile, zipfile, requests
import geopandas as gpd

def get_smoke_polygons(date):
    """Returns GeoDataFrame of smoke polygons, or None on error. date = YYYYMMDD."""
    year, month = date[:4], date[4:6]
    url = (
        f"https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/Shapefile"
        f"/{year}/{month}/hms_smoke{date}.zip"
    )
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error downloading HMS smoke data: {e}")
        return None

    # Stream zip into memory → extract to temp dir → read with GeoPandas
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
            zf.extractall(tmpdir)
        gdf = gpd.read_file(tmpdir)  # GeoPandas auto-finds .shp inside dir

    return gdf
```

**Key patterns:**
- Use `io.BytesIO(r.content)` to handle the zip in-memory (no temp file needed for the zip)
- Use `tempfile.TemporaryDirectory()` as context manager — auto-cleaned on exit
- `gpd.read_file(tmpdir)` with a directory auto-discovers the `.shp` file inside
- Returns `None` (not empty GDF) on network failure — always guard with `if gdf is not None`
- Smoke density column name varies: check for `"density"`, `"Density"`, or `"DENSITY"` at runtime

---

## 4. Fetching NASA FIRMS Fire Detections

**Source**: NASA Fire Information for Resource Management System
**Auth**: Map key from `.env` as URL path segment
**Format**: CSV response (not JSON)

```python
# pipeline/viirs_fire.py
import io, os, requests, pandas as pd
from dotenv import load_dotenv

load_dotenv()
MAP_KEY = os.getenv("FIRMS_MAP_KEY")

def get_active_fires(bbox, day_range):
    """
    bbox: "-124.4,32.5,-114.1,42.0"  (minLon,minLat,maxLon,maxLat)
    day_range: int, 1–10 for NRT; use archive endpoint for historical
    Returns DataFrame with columns: latitude, longitude, frp, bright_ti4, acq_date, ...
    """
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/VIIRS_SNPP_NRT/{bbox}/{day_range}"
    try:
        r = requests.get(url)
        r.raise_for_status()
        return pd.read_csv(io.StringIO(r.text))
    except requests.RequestException as e:
        print(f"Error fetching FIRMS fire data: {e}")
        return None
```

**NRT vs Archive:**
```python
# In the API endpoint, switch based on how old the date is:
from datetime import datetime, date as date_type

requested = datetime.strptime(date, "%Y%m%d").date()
days_ago = (date_type.today() - requested).days

if days_ago <= 10:
    # Near-Real-Time endpoint
    df = get_active_fires(BBOX, max(1, days_ago + 1))
else:
    # Archive endpoint — different product code (VIIRS_SNPP_SP) + explicit date
    archive_date = requested.strftime("%Y-%m-%d")
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/VIIRS_SNPP_SP/{BBOX}/1/{archive_date}"
    resp = requests.get(url)
    df = pd.read_csv(io.StringIO(resp.text))
```

**Key patterns:**
- NRT product: `VIIRS_SNPP_NRT` | Archive product: `VIIRS_SNPP_SP`
- Map key is a path segment, not a query param
- Response is plain CSV — use `pd.read_csv(io.StringIO(r.text))`
- NRT window is ≤10 days; always check `days_ago` before choosing endpoint

---

## 5. GeoPandas Spatial Join Pattern

```python
# pipeline/build_layer.py — core pattern for county × smoke join

import geopandas as gpd, pandas as pd

def build_county_layer(state_code, date):
    # 1. Load + filter county boundaries
    counties = _load_counties()                         # returns GeoDataFrame
    counties = counties[counties["STATEFP"] == state_code].copy()
    counties = counties.to_crs(epsg=4326)               # ensure WGS84

    # 2. Get smoke polygons
    smoke_gdf = get_smoke_polygons(date)
    if smoke_gdf is not None:
        smoke_gdf = smoke_gdf.to_crs(epsg=4326)

        # 3. Left spatial join: each county gets attributes of intersecting smoke polygon
        joined = gpd.sjoin(counties, smoke_gdf, how="left", predicate="intersects")

        # 4. Deduplicate — a county may intersect multiple smoke polygons
        for _, row in joined.drop_duplicates(subset="GEOID").iterrows():
            has_smoke = not pd.isna(row.get("index_right"))
            ...
```

**Rules:**
- Always call `.to_crs(epsg=4326)` on both GDFs before joining — CRS mismatch silently produces wrong results
- Use `how="left"` to keep all counties (including those with no smoke)
- Always `drop_duplicates(subset="GEOID")` after sjoin — a county intersecting N smoke polygons produces N rows
- `"index_right"` being NaN means no match (no smoke) in a left join
- Discover column names at runtime: `next((c for c in gdf.columns if "density" in c.lower()), None)`

---

## 6. SSL Fix for Government URLs

Several government data sources (.gov, NOAA, Census) have SSL certificate issues in server environments. The pattern:

```python
# Strategy 1: requests with verify=False (most reliable)
resp = requests.get(url, verify=False, timeout=120)

# Strategy 2: Disable SSL env vars for geopandas.read_file()
os.environ.setdefault("CURL_CA_BUNDLE", "")
os.environ.setdefault("REQUESTS_CA_BUNDLE", "")
gdf = gpd.read_file(url)
```

**Multi-fallback pattern for critical data (county boundaries):**
```python
def _load_counties():
    # 1. Local cache (fastest, works offline)
    if os.path.exists(COUNTIES_PATH):
        try:
            return gpd.read_file(COUNTIES_PATH)
        except Exception:
            pass  # corrupt cache — continue to download

    # 2. Primary URL with SSL disabled
    try:
        resp = requests.get(CENSUS_URL, verify=False, timeout=120)
        resp.raise_for_status()
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            tmp.write(resp.content)
        gdf = gpd.read_file(f"zip://{tmp.name}")
        os.unlink(tmp.name)
        gdf.to_file(COUNTIES_PATH, driver="GeoJSON")  # update cache
        return gdf
    except Exception:
        pass

    # 3. Backup GitHub static GeoJSON (no SSL issues)
    try:
        resp = requests.get(GITHUB_BACKUP_URL, timeout=60)
        data = resp.json()
        # normalize schema if needed ...
        return gpd.read_file(json_tempfile)
    except Exception:
        pass

    # 4. Hardcoded bounding-box fallback (never fails)
    from shapely.geometry import box
    rows = [{"NAME": "Los Angeles", "GEOID": "06037", "geometry": box(-118.95, 33.70, -117.65, 34.82)}, ...]
    return gpd.GeoDataFrame(rows, crs="EPSG:4326")
```

**Key patterns:**
- `verify=False` suppresses the SSL error; add `timeout` to avoid hangs
- Always have a non-.gov backup URL (GitHub raw, CDN)
- Hardcoded bounding boxes as absolute last resort — keeps the app functional
- Cache to local file after first successful download; catch and ignore cache write failures

---

## 7. Deployment-Safe Data Fetching (URL not File Cache)

In serverless/ephemeral deployments (Render, Railway, Fly.io), the filesystem is read-only or wiped between deploys. Always fetch from URLs at runtime; treat local file cache as optional acceleration.

**Pattern:**
```python
# api/main.py — fetch county GeoJSON from static URL, not from disk
CA_COUNTIES_URL = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/california-counties.geojson"

@app.get("/map/pm25/06/{date}")
async def map_pm25(date: str):
    # Primary data source: always a URL fetch
    resp = requests.get(CA_COUNTIES_URL, verify=False, timeout=30)
    resp.raise_for_status()
    geojson = resp.json()

    # Enrich with PM2.5 data fetched live from EPA API
    readings = get_pm25_readings("06", date, date)
    ...
    return Response(content=json.dumps(geojson), media_type="application/json")
```

**Rules:**
- Never hardcode paths to files that won't exist on the deployment host
- Static reference data (county boundaries, etc.) should come from a public CDN or GitHub raw URL
- Local file cache (`data/counties.geojson`) is an optimization, not a requirement — always have a URL fallback
- Use `os.path.exists()` before any file read; wrap in try/except

---

## 8. GeoJSON to Leaflet Pattern

**Backend** — convert GeoPandas GDF or manual features to GeoJSON:
```python
from fastapi.responses import JSONResponse, Response
import json

# From GeoDataFrame
return JSONResponse(content=json.loads(gdf.to_json()))

# From manually constructed features (fire points)
features = []
for _, row in df.iterrows():
    features.append({
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},  # [lon, lat] order!
        "properties": {"frp": row.get("frp"), "brightness": row.get("bright_ti4")},
    })
return JSONResponse(content={"type": "FeatureCollection", "features": features})

# Empty fallback (never 500 on missing data)
EMPTY_FC = {"type": "FeatureCollection", "features": []}
return JSONResponse(content=EMPTY_FC)
```

**Frontend** — Leaflet rendering:
```javascript
// Polygon layer (smoke, county choropleth)
const layer = L.geoJSON(geojson, {
  style: feat => ({
    fillColor: colorScale(feat.properties.pm25_mean),
    fillOpacity: feat.properties.pm25_mean != null ? 0.65 : 0.18,
    color: '#04040a',
    weight: 0.6,
  }),
  onEachFeature: (feat, lyr) => {
    lyr.on('click', () => openPanel(feat.properties));
    lyr.on('mouseover', function() { this.setStyle({ weight: 2, color: '#f97316' }); });
    lyr.on('mouseout',  function() { layer.resetStyle(this); });  // layer.resetStyle, not lyr
  },
}).addTo(map);

// Point layer (fire detections) — custom icon via pointToLayer
const layer = L.geoJSON(geojson, {
  pointToLayer: (feat, latlng) => {
    const size = feat.properties.frp > 10 ? 26 : 12;
    return L.marker(latlng, {
      icon: L.divIcon({ html: `<div class="flame" style="width:${size}px"></div>`, iconSize: [size, size] })
    });
  },
}).addTo(map);
```

**Key patterns:**
- GeoJSON coordinates are always `[longitude, latitude]` (lon first)
- `layer.resetStyle(lyr)` (not `lyr.resetStyle()`) to undo hover styles
- Return `EMPTY_FC` instead of 500 when data is unavailable — prevents frontend crashes
- Check `geojson.features.length === 0` before adding layer to avoid empty renders

---

## 9. Dynamic API_BASE for Local vs Production

```javascript
// frontend/index.html — top of <script> block
const API = (window.location.hostname === 'localhost' ||
             window.location.hostname === '127.0.0.1')
            ? 'http://127.0.0.1:8000'   // local dev: explicit host
            : '';                         // production: same-origin (relative URLs)

// Usage throughout — all fetch calls use template literal
const res = await fetch(`${API}/map/pm25/06/${date}`);
const res = await fetch(`${API}/county/06/${name}/${date}`);
```

**Why this works:**
- In production (Render, Railway, etc.), the frontend is served by the same FastAPI app via `StaticFiles`, so relative URLs (`/map/pm25/...`) work perfectly
- In local dev, the Vite/live-server frontend runs on a different port than FastAPI (8000), so the full URL is needed
- No environment variable injection into HTML required — pure runtime detection

**FastAPI static file serving:**
```python
# api/main.py
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))
```

---

## 10. Environment Variables

```bash
# .env
EPA_AQS_EMAIL=your@email.com
EPA_AQS_KEY=your_epa_key
FIRMS_MAP_KEY=your_nasa_firms_key
ANTHROPIC_API_KEY=sk-ant-...
```

```python
# Load at module level in each pipeline file
from dotenv import load_dotenv
load_dotenv()
EMAIL = os.getenv("EPA_AQS_EMAIL")
```

**Deployment (Render/Railway):** Set the same keys as environment variables in the dashboard. `load_dotenv()` is a no-op when the vars are already in the environment, so the same code works in both contexts.

---

## 11. FastAPI App Structure

```python
# api/main.py — minimal production-ready skeleton
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles, FileResponse
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Mount frontend (only if directory exists — safe for API-only deploys)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/health")
async def health():
    return {"status": "ok"}

# Port from env var — required for Render/Railway/Fly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

**Deployment requirement**: Always bind to `0.0.0.0` and read `PORT` from environment. Platforms inject `PORT` at runtime; `127.0.0.1` will cause health check failures.

---

## Quick Reference

| Data Source | URL Pattern | Auth | Format | SSL Issue |
|---|---|---|---|---|
| EPA AQS | `aqs.epa.gov/data/api/dailyData/byState` | email+key query params | JSON `{"Data":[...]}` | No |
| NOAA HMS | `satepsanone.nesdis.noaa.gov/.../hms_smoke{date}.zip` | None | Zipped Shapefile | Sometimes |
| NASA FIRMS NRT | `firms.modaps.eosdis.nasa.gov/api/area/csv/{key}/VIIRS_SNPP_NRT/{bbox}/{days}` | Key in URL path | CSV | No |
| NASA FIRMS Archive | `firms.modaps.eosdis.nasa.gov/api/area/csv/{key}/VIIRS_SNPP_SP/{bbox}/1/{date}` | Key in URL path | CSV | No |
| Census TIGER | `www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_county_5m.zip` | None | Zipped Shapefile | Yes — use `verify=False` |

| Task | Pattern |
|---|---|
| Read zip shapefile from URL | `requests.get` → `io.BytesIO` → `zipfile.ZipFile` → `tempfile.TemporaryDirectory` → `gpd.read_file(tmpdir)` |
| Read CSV from URL | `requests.get` → `pd.read_csv(io.StringIO(r.text))` |
| Spatial join | `gpd.sjoin(left, right, how="left", predicate="intersects")` then `drop_duplicates` |
| Convert GDF to GeoJSON | `json.loads(gdf.to_json())` |
| SSL bypass | `requests.get(url, verify=False)` or set `CURL_CA_BUNDLE=""` |
| Dynamic API base | `window.location.hostname === 'localhost' ? 'http://127.0.0.1:8000' : ''` |
