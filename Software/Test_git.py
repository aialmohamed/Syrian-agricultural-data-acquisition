import ee
import requests
from PIL import Image
from io import BytesIO
import os
from utils.gee_utils import GEEUtils
from utils.ndvi_utils import NDVIUtils

# Output directory
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

output_dir = "NDVI_GIF_Frames"
os.makedirs(output_dir, exist_ok=True)
geeUtlis = GEEUtils()
geeUtlis.authenticate()

region_fc  = ee.featurecollection.FeatureCollection(geeUtlis.get_area_asset("SECTOR_1_SUB_1_NORTH_WEST"))
ndvi = NDVIUtils("LANDSAT", "2022-01-01", "2023-12-31", region_fc, mode="timeseries")
# Create image collection (with NDVI band)
ndvi_collection = ndvi.create_ndvi_data()

# First reduce each image in the collection into a single NDVI value and date
reduced_fc = ndvi_collection.map(reduce_ndvi)

# Create NDVI time series images
ndvi_collection = ndvi.create_ndvi_data()

# Visualization parameters
vis_params = {
    'min': 0,
    'max': 1,
    'palette': [
    'ffffff', 'ce7e45', 'df923d', 'f1b555', 'fcd163', '99b718', '74a901',
    '66a000', '529400', '3e8601', '207401', '056201', '004c00', '023b01',
    '012e01', '011d01', '011301'
]
}

# Download and store PNGs
images = []
ndvi_collection_list = ndvi_collection.toList(ndvi_collection.size())
count = ndvi_collection.size().getInfo()

for i in range(count):
    img = ee.Image(ndvi_collection_list.get(i))
    date_str = ee.Date(img.get('system:time_start')).format("YYYY-MM-dd").getInfo()
    
    # Get thumbnail URL
    url = img.visualize(**vis_params).getThumbURL({
        'region': region_fc.geometry(),
        'dimensions': 512,
        'format': 'png'
    })
    
    response = requests.get(url)
    if response.status_code == 200:
        img_data = Image.open(BytesIO(response.content))
        img_path = os.path.join(output_dir, f"{date_str}.png")
        img_data.save(img_path)
        images.append(img_data)
        print(f"Saved frame: {img_path}")
    else:
        print(f"Failed to get image for {date_str}")

# Create GIF
gif_path = "ndvi_timeseries.gif"
images[0].save(gif_path, save_all=True, append_images=images[1:], duration=100, loop=0)
print(f"GIF saved: {gif_path}")
