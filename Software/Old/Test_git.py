import ee
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
from utils.gee_utils import GEEUtils
from utils.ndvi_utils import NDVIUtils
from utils.paths import Paths
# Set up output
output_dir = "NDVI_GIF_Frames"
os.makedirs(output_dir, exist_ok=True)

# Authenticate
geeUtlis = GEEUtils()
geeUtlis.authenticate()
paths = Paths()
font_path = paths.font_path
arial = os.path.join(font_path, "ARIAL.TTF")

region_fc = ee.featurecollection.FeatureCollection(
    geeUtlis.get_area_asset("SECTOR_2_SUB_4_MID_WEST")
)

# Create NDVI data
ndvi = NDVIUtils("LANDSAT", "2019-01-01", "2019-12-31", region_fc, mode="timeseries")
ndvi_collection = ndvi.create_ndvi_data()

# Visualization parameters
vis_params = {
    'min': 0,
    'max': 1,
    'palette': [
        'ffffff', 'ce7e45', 'df923d', 'f1b555', 'fcd163', '99b718', '74a901',
        '66a000', '529400', '3e8601', '207401', '056201', '004c00', '023b01',
        '012e01', '011d01', '011301'
    ],
    'bands':['NDVI']
}

# Group by month and create median composites
def monthly_median(month):
    month = ee.Number(month)
    filtered = ndvi_collection.filter(ee.Filter.calendarRange(month, month, 'month'))
    median = filtered.median()
    return median.set({
        'month': month,
        'label': ee.Date.fromYMD(2019, month, 1).format('YYYY-MM')
    })

months = ee.List.sequence(1, 12)
monthly_collection = ee.ImageCollection(months.map(monthly_median))

# Create GIF frames
images = []
monthly_list = monthly_collection.toList(monthly_collection.size())
count = monthly_collection.size().getInfo()

for i in range(count):
    img = ee.Image(monthly_list.get(i))
    date_label = img.get('label').getInfo()
    
    # Clip + visualize
    img_clipped = img.clip(region_fc)
    url = img_clipped.visualize(**vis_params).getThumbURL({
        'region': region_fc.geometry(),
        'dimensions': 512,
        'format': 'png'
    })

    response = requests.get(url)
    if response.status_code == 200:
        img_data = Image.open(BytesIO(response.content)).convert("RGBA")

        # Draw timestamp
        draw = ImageDraw.Draw(img_data)
        font = ImageFont.truetype(arial, 20)
        draw.text((20, 20), date_label, fill="white", font=font)

        # Save PNG
        img_path = os.path.join(output_dir, f"{date_label}.png")
        img_data.save(img_path)
        images.append(img_data)
        print(f"Saved frame: {img_path}")
    else:
        print(f"Failed to get image for {date_label}")

# Save animated GIF
gif_path = "ndvi_timeseries.gif"
images[0].save(gif_path, save_all=True, append_images=images[1:], duration=500, loop=0,disposal=2)
print(f"GIF saved: {gif_path}")
