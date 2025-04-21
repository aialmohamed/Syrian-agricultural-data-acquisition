import ee
from utils.config_utils import ConfigUtils

class NDVIUtils:
    def __init__(self, satellite: str, start_date: str, end_date: str, region: ee.FeatureCollection, mode: str = "composite"):
        self.project_cfg = ConfigUtils()
        self._satellite = satellite.upper()
        self._start_date = start_date
        self._end_date = end_date
        self._region = region
        self._mode = mode.lower()

        self._ndvi_landsat = self.project_cfg.ndvi_landsat
        self._ndvi_modis = self.project_cfg.ndvi_modis

    def create_ndvi_data(self):
        if self._satellite == "LANDSAT":
            return self._create_ndvi_landsat()
        elif self._satellite == "MODIS":
            return self._create_ndvi_modis()
        else:
            raise ValueError(f"Unsupported satellite: {self._satellite}")
        



    def _create_ndvi_landsat(self):
        collection = ee.ImageCollection(self._ndvi_landsat) \
            .filterDate(self._start_date, self._end_date) \
            .filterBounds(self._region) \
            .sort('CLOUD_COVER')

        if self._mode == "composite":
            image = collection.median().clip(self._region)
            return image.normalizedDifference(['B5', 'B4']).rename('NDVI')

        elif self._mode == "timeseries":
            def add_ndvi(img):
                # clear the clouds :
                scored = ee.Algorithms.Landsat.simpleCloudScore(img)
                mask = scored.select(['cloud']).lte(20)
                masked = img.updateMask(mask)

                ndvi = masked.normalizedDifference(['B5', 'B4']).rename('NDVI')
                return ndvi.set('system:time_start', img.get('system:time_start'))
            return collection.map(add_ndvi).sort('system:time_start')

        else:
            raise ValueError(f"Unsupported mode: {self._mode}")

    def _create_ndvi_modis(self):
        collection = ee.ImageCollection(self._ndvi_modis) \
            .filterDate(self._start_date, self._end_date) \
            .filterBounds(self._region)

        if self._mode == "composite":
            image = collection.median().clip(self._region)
            return image.select('NDVI').multiply(0.0001).rename('NDVI')

        elif self._mode == "timeseries":
            def scale_ndvi(img):
                return img.select('NDVI').multiply(0.0001).rename('NDVI') \
                          .set('system:time_start', img.get('system:time_start'))
            return collection.map(scale_ndvi).sort('system:time_start')

        else:
            raise ValueError(f"Unsupported mode: {self._mode}")
