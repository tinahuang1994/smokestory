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
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from pipeline.build_layer import build_county_layer, COUNTIES_PATH
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

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class ChatRequest(BaseModel):
    question: str
    county_data: dict


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/county/{state_code}/{county_name}/{date}")
async def get_county(state_code: str, county_name: str, date: str):
    counties = build_county_layer(state_code, date)
    match = next(
        (c for c in counties if c["county_name"].lower() == county_name.lower()),
        None,
    )
    if match is None:
        raise HTTPException(status_code=404, detail=f"County '{county_name}' not found")
    narrative = generate_narrative(match, date=date)
    return {**match, "narrative": narrative}


@app.get("/top-stories/{date}")
async def top_stories(date: str):
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

Answer in plain English, keeping your response concise and accessible."""

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


@app.get("/map/pm25/06/{date}")
async def map_pm25(date: str):
    if not os.path.exists(COUNTIES_PATH):
        return Response(content=json.dumps(EMPTY_FC), media_type="application/json")
    counties = build_county_layer("06", date)
    pm25_lookup = {r["county_name"]: r for r in counties}
    gdf = gpd.read_file(COUNTIES_PATH)
    gdf = gdf[gdf["STATEFP"] == "06"].copy()
    gdf["pm25_mean"] = gdf["NAME"].map(lambda n: pm25_lookup.get(n, {}).get("pm25_mean"))
    gdf["smoke_density"] = gdf["NAME"].map(lambda n: pm25_lookup.get(n, {}).get("smoke_density"))
    gdf["has_smoke"] = gdf["NAME"].map(lambda n: pm25_lookup.get(n, {}).get("has_smoke", False))
    gdf["county_name"] = gdf["NAME"]
    return Response(content=gdf[["county_name", "pm25_mean", "smoke_density", "has_smoke", "geometry"]].to_json(), media_type="application/json")


# To run:
# uvicorn api.main:app --reload
