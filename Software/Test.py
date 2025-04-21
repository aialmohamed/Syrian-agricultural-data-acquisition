import ee
import folium
import webbrowser
import os
from utils.gee_utils import GEEUtils






geeUtlis = GEEUtils()
geeUtlis.authenticate()

aoi = ee.featurecollection.FeatureCollection(geeUtlis.get_area_asset("SECTOR_2_SUB_4_MID_WEST"))
print(aoi.limit(1).getInfo())