import os
import tempfile
import requests
import geopandas as gpd
import pandas as pd

from pipeline.epa_aqs import get_pm25_readings
from pipeline.goes_hms import get_smoke_polygons
from pipeline.viirs_fire import get_active_fires

COUNTIES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "counties.geojson")
COUNTIES_URL = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_county_5m.zip"


def _load_counties():
    if os.path.exists(COUNTIES_PATH):
        print("Loading counties from cache...")
        return gpd.read_file(COUNTIES_PATH)
    print("Downloading US county boundaries...")
    response = requests.get(COUNTIES_URL, verify=False)
    response.raise_for_status()
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name
    gdf = gpd.read_file(f"zip://{tmp_path}")
    os.unlink(tmp_path)
    os.makedirs(os.path.dirname(COUNTIES_PATH), exist_ok=True)
    gdf.to_file(COUNTIES_PATH, driver="GeoJSON")
    print("Counties cached to data/counties.geojson")
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
