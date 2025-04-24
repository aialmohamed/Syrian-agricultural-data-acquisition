import ee
from utils.config_utils import ConfigUtils
from collections import defaultdict
from datetime import datetime
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
    def apply_scale_factors_landsat(self, img):
        opt_bands = img.select('SR_B.').multiply(0.0000275).add(-0.2)
        thermal_bands = img.select('ST_B.*').multiply(0.00341802).add(149.0)
        return img.addBands(opt_bands, None, True).addBands(
            thermal_bands, None, True)

    def _create_ndvi_landsat(self):
        collection = ee.ImageCollection(self._ndvi_landsat) \
            .filterDate(self._start_date, self._end_date) \
            .filterBounds(self._region) \
            .map(self.apply_scale_factors_landsat)

        if self._mode == "composite":
            image = collection.median().clip(self._region)
            return image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')

        elif self._mode == "timeseries":
            def add_ndvi(img):

                # Mask: bits 0 (Fill), 1 (Dilated Cloud), 3 (Cloud), 4 (Shadow)
                qa = img.select('QA_PIXEL')
                bits_to_mask = (1 << 0) | (1 << 1) |(1 << 2)| (1 << 3) | (1 << 4)
                qa_mask = qa.bitwiseAnd(bits_to_mask).eq(0)

                # Saturation mask from QA_RADSAT
                saturation_mask = img.select('QA_RADSAT').eq(0)
                ndvi = img.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
                ndvi = ndvi.updateMask(qa_mask).updateMask(saturation_mask)
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
        
    def reduce_monthly_ndvi(self,img):
        mean = img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=self._region.geometry(),
            scale=250,
            maxPixels=1e13
        )
        return ee.Feature(None, {
            "date": img.get('label'),
            "NDVI": mean.get('NDVI')
        })

    def reduce_ndvi_image(self,image):
        stat = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=self._region.geometry(),
            scale=250,
            maxPixels=1e13
        )
        return ee.Feature(None, {
            "NDVI": stat.get("NDVI"),
            "date": image.date().format("YYYY-MM-dd")
        })
    
    def aggregate_ndvi_by_date(self,feature_collection):
        """_summary_

        Args:
            feature_collection (_type_): _description_
        """
        features = feature_collection.getInfo()["features"]
        grouped = defaultdict(list)

        for f in features:
            props = f["properties"]
            date = props.get("date")
            ndvi = props.get("NDVI")  # use .get() to avoid KeyError
            if ndvi is not None and date is not None:
                grouped[date].append(ndvi)

        dates = []
        ndvi_values = []
        for date, values in grouped.items():
            dates.append(datetime.strptime(date, "%Y-%m-%d"))
            ndvi_values.append(sum(values) / len(values))

        return dates, ndvi_values
    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def satellite(self):
        return self._satellite

    @property
    def region(self):
        return self._region

    @property
    def mode(self):
        return self._mode