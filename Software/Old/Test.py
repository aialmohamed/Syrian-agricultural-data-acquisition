import ee
import folium
import webbrowser
from utils.gee_utils import GEEUtils
from utils.ndvi_utils import NDVIUtils
from utils.ndvi_charting_utils import NdviChartingUtils

# Authenticate Earth Engine
geeUtlis = GEEUtils()
geeUtlis.authenticate()

# Load region and setup NDVI utils
region_fc  = ee.featurecollection.FeatureCollection(geeUtlis.get_area_asset("SYRIA_EAST_AOI"))
ndvi = NDVIUtils("LANDSAT", "2019-01-01", "2019-12-31", region_fc, mode="timeseries")

# Setup charting utils
chart_utils = NdviChartingUtils(ndvi, 2019)

# Run the full workflow and plot
chart_utils.plot_multi_year_ndvi(2018, 2018)