import ee
import folium
import webbrowser
from utils.gee_utils import GEEUtils
from utils.ndvi_utils import NDVIUtils
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime


def aggregate_ndvi_by_date(feature_collection):
    features = feature_collection.getInfo()["features"]

    grouped = defaultdict(list)
    
    for f in features:
        date = f["properties"]["date"]
        ndvi = f["properties"]["NDVI"]
        if ndvi is not None:
            grouped[date].append(ndvi)

    dates = []
    ndvi_values = []
    for date, values in grouped.items():
        dates.append(datetime.strptime(date, "%Y-%m-%d"))
        ndvi_values.append(sum(values) / len(values))

    return dates, ndvi_values

def reduce_ndvi(img):
    stat = img.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region_fc.geometry(),
        scale=250,
        maxPixels=1e13
    )
    return ee.Feature(None, {
        "NDVI": stat.get("NDVI"),
        "date": img.date().format("YYYY-MM-dd")
    })

geeUtlis = GEEUtils()
geeUtlis.authenticate()

region_fc  = ee.featurecollection.FeatureCollection(geeUtlis.get_area_asset("SECTOR_2_SUB_4_MID_WEST"))
ndvi = NDVIUtils("LANDSAT", "2013-01-01", "2013-12-31", region_fc, mode="timeseries")
# Create image collection (with NDVI band)
ndvi_collection = ndvi.create_ndvi_data()

# First reduce each image in the collection into a single NDVI value and date
reduced_fc = ndvi_collection.map(reduce_ndvi)

# Now aggregate the result (correct shape now)
dates, ndvi_vals = aggregate_ndvi_by_date(reduced_fc)

print("NDVI Collection:", reduced_fc.getInfo())
# Plot it


plt.figure(figsize=(12, 6))
plt.plot(dates, ndvi_vals, marker='o', color='green')
plt.title("NDVI Time Series (SECTOR_2_SUB_4_MID_WEST, 2018)")
plt.xlabel("Date")
plt.ylabel("NDVI")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



