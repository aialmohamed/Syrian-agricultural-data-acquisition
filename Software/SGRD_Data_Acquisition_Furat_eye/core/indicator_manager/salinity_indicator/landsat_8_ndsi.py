import ee
from core.indicator_manager.base_indicator import BaseIndicator



# https://www.indexdatabase.de/db/i-single.php?id=57

class Landsat8NDSI(BaseIndicator):
    def compute(self) -> ee.ImageCollection:
        def calculate_ndsi(img):
            ndsi = img.normalizedDifference(["SR_B6", "SR_B7"]).rename("NDSI")
            return ndsi.copyProperties(img, ["system:time_start"])
        return self._collection.map(calculate_ndsi)