



import ee
from core.indicator_manager.base_indicator import BaseIndicator


class UcsbPrecipitation(BaseIndicator):
    def compute(self) -> ee.ImageCollection:
        def calculate_precipitation(img):
            return img.select("precipitation").copyProperties(img, img.propertyNames())
        return self._collection.map(calculate_precipitation)