import rasterio
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from config import NIGHTLIGHTS_DIR, HQ_DIR, DATA_PROCESSED

def load_hq():
    hq = pd.read_csv(HQ_DIR / "sp500_hq.csv")
    return gpd.GeoDataFrame(
        hq,
        geometry=gpd.points_from_xy(hq.lon, hq.lat),
        crs="EPSG:4326"
    )

def extract_radiance(path, pts):
    with rasterio.open(path) as src:
        pts_proj = pts.to_crs(src.crs)
        coords = [(x, y) for x, y in zip(pts_proj.geometry.x, pts_proj.geometry.y)]
        rad = [val[0] for val in src.sample(coords)]
    return rad

def build_lights_panel():
    pts = load_hq()
    rows = []

    for tif in sorted(NIGHTLIGHTS_DIR.glob("*.tif")):
        filename = tif.name
        year = filename[14:18]
        month = filename[18:20]
        date = pd.to_datetime(f"{year}-{month}-01")

        pts["date"] = date
        pts["light_level"] = extract_radiance(tif, pts)

        rows.append(pts.copy())

    df = pd.concat(rows)
    df["light_change"] = df.groupby("ticker")["light_level"].pct_change()

    DATA_PROCESSED.mkdir(exist_ok=True)
    df.to_csv(DATA_PROCESSED / "lights_panel.csv", index=False)

if __name__ == "__main__":
    build_lights_panel()

