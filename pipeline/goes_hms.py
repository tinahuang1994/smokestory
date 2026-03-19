import io
import tempfile
import zipfile
import requests
import geopandas as gpd


def get_smoke_polygons(date):
    year = date[:4]
    month = date[4:6]
    url = (
        f"https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/Shapefile"
        f"/{year}/{month}/hms_smoke{date}.zip"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error downloading HMS smoke data: {e}")
        return None

    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            zf.extractall(tmpdir)
        gdf = gpd.read_file(tmpdir)

    return gdf


if __name__ == "__main__":
    gdf = get_smoke_polygons("20240901")
    if gdf is not None:
        print(gdf.shape)
        print(gdf.head(3))
