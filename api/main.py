import os
import io
import json
import math
import requests
import anthropic
import pandas as pd
from datetime import datetime, date as date_type
import geopandas as gpd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from pipeline.build_layer import build_county_layer, COUNTIES_PATH
from pipeline.epa_aqs import get_pm25_readings
from pipeline.goes_hms import get_smoke_polygons
from pipeline.viirs_fire import get_active_fires
from pipeline.news import get_news_headlines
from narrative.generator import generate_narrative

load_dotenv()

app = FastAPI(title="SmokeStory")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def validate_date(date_str: str):
    try:
        d = datetime.strptime(date_str, "%Y%m%d").date()
    except ValueError:
        raise HTTPException(status_code=400,
            detail="Invalid date format. Use YYYYMMDD (e.g. 20250109).")
    if d < date_type(2005, 8, 1):
        raise HTTPException(status_code=400,
            detail="No data available before August 2005. HMS smoke data begins August 2005.")
    if d > date_type.today():
        raise HTTPException(status_code=400,
            detail="Cannot request future dates.")
    return d


def check_data_quality(county_data):
    pm25 = county_data.get("pm25_mean")
    has_smoke = county_data.get("has_smoke") or False

    if has_smoke and pm25 is not None and pm25 < 15:
        return "⚠️ Data quality notice: Smoke is detected over this county but PM2.5 readings are unusually low. EPA monitors sometimes go offline during major fire events due to evacuations or power outages, producing misleadingly low readings. This data may not reflect actual conditions. Cross-reference with AirNow.gov for this date."
    if has_smoke and pm25 is None:
        return "⚠️ No ground monitor data available for this county on this date. Smoke is present per satellite data. Check AirNow.gov for historical air quality information."
    return None


class ChatRequest(BaseModel):
    question: str
    county_data: dict


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/county/{state_code}/{county_name}/{date}")
async def get_county(state_code: str, county_name: str, date: str):
    validate_date(date)
    counties = build_county_layer(state_code, date)
    match = next(
        (c for c in counties if c["county_name"].lower() == county_name.lower()),
        None,
    )
    if match is None:
        raise HTTPException(status_code=404, detail=f"County '{county_name}' not found")
    warning = check_data_quality(match)
    match["data_quality_warning"] = warning
    narrative = generate_narrative(match, date=date)
    return {**match, "narrative": narrative}


@app.get("/top-stories/{date}")
async def top_stories(date: str):
    validate_date(date)
    counties = build_county_layer("06", date)
    filtered = [c for c in counties if c["has_smoke"] and c["pm25_mean"] is not None]
    filtered.sort(key=lambda c: c["pm25_mean"], reverse=True)
    results = []
    for county in filtered[:3]:
        narrative = generate_narrative(county, date=date)
        results.append({**county, "narrative": narrative})
    return results


@app.post("/chat")
async def chat(body: ChatRequest):
    county = body.county_data
    prompt = f"""You are a helpful air quality assistant for SmokeStory.

County context:
- County: {county.get("county_name")}, state FIPS {county.get("state")}
- Smoke present: {county.get("has_smoke")}
- Smoke density: {county.get("smoke_density")}
- PM2.5 mean: {county.get("pm25_mean")}

User question: {body.question}

Answer in plain English, keeping your response concise and accessible.

Always end your response with this line on its own:
For medical advice, consult your doctor or local health authority. For current air quality, visit AirNow.gov."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return {"answer": message.content[0].text}


@app.get("/news/{county_name}/{date}")
async def news(county_name: str, date: str):
    headlines = get_news_headlines(county_name, date)
    return {"headlines": headlines}


EMPTY_FC = {"type": "FeatureCollection", "features": []}


@app.get("/map/smoke/{date}")
async def map_smoke(date: str):
    gdf = get_smoke_polygons(date)
    if gdf is None or gdf.empty:
        return JSONResponse(content=EMPTY_FC)
    return JSONResponse(content=json.loads(gdf.to_json()))


FIRMS_KEY = os.getenv("FIRMS_MAP_KEY")
BBOX = "-124.4,32.5,-114.1,42.0"


@app.get("/map/fires/{date}")
async def map_fires(date: str):
    requested = datetime.strptime(date, "%Y%m%d").date()
    days_ago = (date_type.today() - requested).days

    if days_ago <= 10:
        day_range = max(1, days_ago + 1)
        df = get_active_fires(BBOX, day_range)
    else:
        # Archive endpoint for historical dates
        archive_date = requested.strftime("%Y-%m-%d")
        url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{FIRMS_KEY}/VIIRS_SNPP_SP/{BBOX}/1/{archive_date}"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            df = pd.read_csv(io.StringIO(resp.text))
        except Exception as e:
            print(f"Error fetching archive fire data: {e}")
            return JSONResponse(content=EMPTY_FC)

    if df is None or df.empty:
        return JSONResponse(content=EMPTY_FC)

    features = []
    for _, row in df.iterrows():
        try:
            lat = float(row["latitude"])
            lon = float(row["longitude"])
        except (KeyError, ValueError):
            continue
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {
                "frp": row.get("frp"),
                "brightness": row.get("bright_ti4") or row.get("brightness"),
            },
        })
    return JSONResponse(content={"type": "FeatureCollection", "features": features})


CA_COUNTIES_URL = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/california-counties.geojson"


@app.get("/map/pm25/06/{date}")
async def map_pm25(date: str):
    # 1. Fetch California county boundaries from GitHub static GeoJSON
    try:
        resp = requests.get(CA_COUNTIES_URL, verify=False, timeout=30)
        resp.raise_for_status()
        geojson = resp.json()
        features = geojson.get("features", [])
        print(f"[map_pm25] Loaded {len(features)} California county features")
    except Exception as e:
        print(f"[map_pm25] County GeoJSON fetch failed: {e}")
        return Response(content=json.dumps(EMPTY_FC), media_type="application/json")

    # 2. Fetch PM2.5 readings and build a lowercase name → pm25_mean lookup
    readings = get_pm25_readings("06", date, date)
    pm25_by_name = {}
    if readings:
        df = pd.DataFrame(readings)
        if "county" in df.columns and "arithmetic_mean" in df.columns:
            pm25_by_name = (
                df.groupby(df["county"].str.lower())["arithmetic_mean"]
                .mean()
                .to_dict()
            )
    print(f"[map_pm25] PM2.5 data for {len(pm25_by_name)} counties on {date}")

    # 3. Merge PM2.5 into each feature by case-insensitive name match
    matched = 0
    for feat in features:
        props = feat.setdefault("properties", {})
        name = props.get("name", "")
        props["county_name"] = name
        pm25 = pm25_by_name.get(name.lower())
        props["pm25_mean"] = pm25
        props["smoke_density"] = None
        props["has_smoke"] = False
        if pm25 is not None:
            matched += 1
    print(f"[map_pm25] Matched PM2.5 data for {matched}/{len(features)} counties")

    return Response(content=json.dumps(geojson), media_type="application/json")


# To run:
# uvicorn api.main:app --reload

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
