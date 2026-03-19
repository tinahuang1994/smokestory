import io
import json
import os
import tempfile
import traceback
import requests
import geopandas as gpd
import pandas as pd
from shapely.geometry import box

from pipeline.epa_aqs import get_pm25_readings
from pipeline.goes_hms import get_smoke_polygons
from pipeline.viirs_fire import get_active_fires

COUNTIES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "counties.geojson")
COUNTIES_URL = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_county_5m.zip"
BACKUP_URL = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"


def _cache(gdf):
    """Save GDF to cache file, ignoring errors."""
    try:
        os.makedirs(os.path.dirname(COUNTIES_PATH), exist_ok=True)
        gdf.to_file(COUNTIES_PATH, driver="GeoJSON")
        print(f"[counties] Cached to {COUNTIES_PATH}")
    except Exception as e:
        print(f"[counties] Cache write failed (non-fatal): {e}")


def _load_counties():
    # ── Step 1: local cache ───────────────────────────────────
    if os.path.exists(COUNTIES_PATH):
        print(f"[counties] Loading from cache: {COUNTIES_PATH}")
        try:
            return gpd.read_file(COUNTIES_PATH)
        except Exception as e:
            print(f"[counties] Cache read failed, will re-download: {e}")

    # ── Step 2: Census shapefile via requests (SSL verify=False) ──
    print(f"[counties] Downloading from Census: {COUNTIES_URL}")
    try:
        resp = requests.get(COUNTIES_URL, verify=False, timeout=120)
        resp.raise_for_status()
        print(f"[counties] Downloaded {len(resp.content) // 1024} KB")
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            tmp.write(resp.content)
            tmp_path = tmp.name
        gdf = gpd.read_file(f"zip://{tmp_path}")
        os.unlink(tmp_path)
        _cache(gdf)
        print(f"[counties] Census download succeeded ({len(gdf)} counties)")
        return gdf
    except Exception as e:
        print(f"[counties] Census download (requests) failed: {e}")
        traceback.print_exc()

    # ── Step 3: geopandas direct read with SSL disabled ───────
    print("[counties] Retrying via geopandas direct read (SSL disabled)...")
    try:
        os.environ.setdefault("CURL_CA_BUNDLE", "")
        os.environ.setdefault("REQUESTS_CA_BUNDLE", "")
        gdf = gpd.read_file(COUNTIES_URL)
        _cache(gdf)
        print(f"[counties] GeoPandas direct read succeeded ({len(gdf)} counties)")
        return gdf
    except Exception as e:
        print(f"[counties] GeoPandas direct read failed: {e}")
        traceback.print_exc()

    # ── Step 4: backup GeoJSON from GitHub (Plotly dataset) ───
    print(f"[counties] Trying backup URL: {BACKUP_URL}")
    try:
        resp = requests.get(BACKUP_URL, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        # Adapt schema: each feature has id="06037", properties.name="Los Angeles County"
        for feat in data.get("features", []):
            fips = str(feat.get("id", "")).zfill(5)
            props = feat.setdefault("properties", {})
            props["STATEFP"]  = fips[:2]
            props["COUNTYFP"] = fips[2:]
            props["GEOID"]    = fips
            props["NAME"]     = props.get("name", "").removesuffix(" County").strip()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as tmp:
            json.dump(data, tmp)
            tmp_path = tmp.name
        gdf = gpd.read_file(tmp_path)
        os.unlink(tmp_path)
        _cache(gdf)
        print(f"[counties] Backup download succeeded ({len(gdf)} counties)")
        return gdf
    except Exception as e:
        print(f"[counties] Backup download failed: {e}")
        traceback.print_exc()

    # ── Step 5: hardcoded California bounding-box fallback ────
    print("[counties] ALL DOWNLOADS FAILED — using hardcoded California fallback")
    # (name, COUNTYFP, GEOID, minx, miny, maxx, maxy)
    CA_COUNTIES = [
        ("Los Angeles",    "037", "06037", -118.95, 33.70, -117.65, 34.82),
        ("San Diego",      "073", "06073", -117.60, 32.53, -116.08, 33.51),
        ("Orange",         "059", "06059", -118.12, 33.38, -117.41, 33.95),
        ("Riverside",      "065", "06065", -117.67, 33.51, -114.44, 34.08),
        ("San Bernardino", "071", "06071", -117.67, 34.08, -114.13, 35.81),
        ("Santa Clara",    "085", "06085", -122.20, 36.89, -121.21, 37.48),
        ("Alameda",        "001", "06001", -122.37, 37.45, -121.47, 37.91),
        ("Sacramento",     "067", "06067", -121.86, 38.02, -121.03, 38.74),
        ("Fresno",         "019", "06019", -120.53, 36.16, -119.20, 37.58),
        ("Kern",           "029", "06029", -119.59, 34.92, -117.63, 35.79),
        ("Ventura",        "111", "06111", -119.44, 34.05, -118.63, 34.62),
        ("San Francisco",  "075", "06075", -122.51, 37.70, -122.36, 37.83),
        ("Contra Costa",   "013", "06013", -122.42, 37.72, -121.55, 38.09),
        ("Shasta",         "089", "06089", -122.50, 40.35, -121.33, 41.18),
        ("Butte",          "007", "06007", -122.06, 39.52, -121.22, 40.15),
        ("Sonoma",         "097", "06097", -123.53, 38.16, -122.35, 38.86),
        ("Napa",           "055", "06055", -122.64, 38.18, -122.10, 38.86),
        ("Tuolumne",       "109", "06109", -120.65, 37.69, -119.52, 38.43),
        ("Nevada",         "057", "06057", -121.31, 39.07, -120.00, 39.47),
        ("Plumas",         "063", "06063", -121.42, 39.79, -120.07, 40.43),
        ("Mendocino",      "045", "06045", -124.11, 38.77, -122.75, 39.80),
        ("Trinity",        "105", "06105", -123.53, 40.07, -122.38, 41.18),
        ("Siskiyou",       "093", "06093", -122.93, 41.18, -121.33, 42.00),
        ("Humboldt",       "023", "06023", -124.41, 40.00, -123.40, 41.47),
        ("Del Norte",      "015", "06015", -124.21, 41.47, -123.54, 41.99),
        ("Modoc",          "049", "06049", -121.33, 41.18, -120.00, 42.00),
        ("Lassen",         "035", "06035", -121.33, 40.15, -120.00, 41.18),
        ("Tehama",         "103", "06103", -123.00, 39.79, -121.33, 40.43),
        ("Glenn",          "021", "06021", -122.75, 39.52, -122.06, 40.15),
        ("Colusa",         "011", "06011", -122.68, 38.74, -121.86, 39.52),
        ("Lake",           "033", "06033", -123.00, 38.74, -122.06, 39.52),
        ("Yolo",           "113", "06113", -122.37, 38.50, -121.60, 38.74),
        ("Solano",         "095", "06095", -122.42, 38.03, -121.60, 38.50),
        ("Marin",          "041", "06041", -123.00, 37.83, -122.35, 38.18),
        ("San Mateo",      "081", "06081", -122.52, 37.45, -122.10, 37.71),
        ("Santa Cruz",     "087", "06087", -122.31, 36.85, -121.58, 37.28),
        ("Monterey",       "053", "06053", -122.07, 35.79, -120.21, 36.92),
        ("San Luis Obispo","079", "06079", -121.33, 34.79, -119.47, 35.79),
        ("Santa Barbara",  "083", "06083", -120.65, 34.39, -118.95, 34.92),
        ("San Benito",     "069", "06069", -121.58, 36.29, -120.60, 37.01),
        ("Stanislaus",     "099", "06099", -121.00, 37.23, -120.11, 37.74),
        ("San Joaquin",    "077", "06077", -121.58, 37.48, -121.00, 38.08),
        ("Merced",         "047", "06047", -121.00, 37.07, -120.03, 37.50),
        ("Madera",         "039", "06039", -120.53, 36.77, -119.20, 37.58),
        ("Kings",          "031", "06031", -120.21, 35.79, -119.20, 36.60),
        ("Tulare",         "107", "06107", -119.59, 35.79, -118.13, 36.77),
        ("Inyo",           "027", "06027", -118.44, 35.51, -114.13, 37.52),
        ("Mono",           "051", "06051", -119.65, 37.52, -118.22, 38.43),
        ("Alpine",         "003", "06003", -120.07, 38.43, -119.52, 38.90),
        ("El Dorado",      "017", "06017", -120.98, 38.53, -119.98, 39.07),
        ("Placer",         "061", "06061", -121.47, 38.74, -120.51, 39.32),
        ("Sutter",         "101", "06101", -121.86, 38.73, -121.47, 39.16),
        ("Yuba",           "115", "06115", -121.47, 39.08, -121.00, 39.47),
        ("Calaveras",      "009", "06009", -120.65, 37.95, -120.07, 38.43),
        ("Amador",         "005", "06005", -121.00, 38.25, -120.51, 38.61),
        ("Mariposa",       "043", "06043", -120.07, 37.37, -119.19, 37.98),
        ("Imperial",       "025", "06025", -116.08, 32.52, -114.44, 33.51),
    ]
    rows = [
        {
            "STATEFP": "06", "COUNTYFP": cfp, "GEOID": geoid, "NAME": name,
            "geometry": box(minx, miny, maxx, maxy),
        }
        for name, cfp, geoid, minx, miny, maxx, maxy in CA_COUNTIES
    ]
    gdf = gpd.GeoDataFrame(rows, crs="EPSG:4326")
    print(f"[counties] Hardcoded fallback: {len(gdf)} California counties")
    return gdf


def build_county_layer(state_code, date):
    print(f"Fetching PM2.5 readings for state {state_code} on {date}...")
    readings = get_pm25_readings(state_code, date, date)
    pm25_by_county = {}
    if readings:
        df_pm25 = pd.DataFrame(readings)
        if "county_code" in df_pm25.columns and "arithmetic_mean" in df_pm25.columns:
            pm25_by_county = (
                df_pm25.groupby("county_code")["arithmetic_mean"]
                .mean()
                .to_dict()
            )

    print(f"Fetching smoke polygons for {date}...")
    smoke_gdf = get_smoke_polygons(date)

    print("Loading county boundaries...")
    counties = _load_counties()
    counties = counties[counties["STATEFP"] == state_code].copy()
    counties = counties.to_crs(epsg=4326)

    results = []

    if smoke_gdf is not None and not smoke_gdf.empty:
        smoke_gdf = smoke_gdf.to_crs(epsg=4326)
        print("Spatial joining counties with smoke polygons...")
        joined = gpd.sjoin(counties, smoke_gdf, how="left", predicate="intersects")
        density_col = next(
            (c for c in smoke_gdf.columns if "density" in c.lower() or "smoke" in c.lower()),
            None,
        )
        for _, row in joined.drop_duplicates(subset="GEOID").iterrows():
            county_code = row.get("COUNTYFP", "")
            results.append({
                "county_name": row.get("NAME", ""),
                "state": state_code,
                "pm25_mean": pm25_by_county.get(county_code),
                "smoke_density": row.get(density_col) if density_col else None,
                "has_smoke": not pd.isna(row.get("index_right")) if "index_right" in row else False,
            })
    else:
        print("No smoke data available; returning counties without smoke info.")
        for _, row in counties.iterrows():
            county_code = row.get("COUNTYFP", "")
            results.append({
                "county_name": row.get("NAME", ""),
                "state": state_code,
                "pm25_mean": pm25_by_county.get(county_code),
                "smoke_density": None,
                "has_smoke": False,
            })

    print(f"Done. Returning {len(results)} county records.")
    return results


if __name__ == "__main__":
    results = build_county_layer("06", "20250109")
    filtered = [r for r in results if r["has_smoke"] and r["pm25_mean"] is not None]
    filtered.sort(key=lambda r: r["pm25_mean"], reverse=True)
    for r in filtered[:5]:
        print(r)
