import ee

from core.indicator_manager.base_indicator import BaseIndicator


class Landsat8Ndvi(BaseIndicator):
    def compute(self) -> ee.ImageCollection:
        def calculate_ndvi(img):
            ndvi = img.normalizedDifference(["SR_B5", "SR_B4"]).rename("NDVI")
            return ndvi.copyProperties(img, ["system:time_start"])
        return self._collection.map(calculate_ndvi)
    def reduce(self, geometry: ee.Geometry, scale: int = 250) -> ee.FeatureCollection:
        ndvi_col = self.compute()

        def reduce_image(img):
            mean = img.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=scale,
                maxPixels=1e13
            )
            return ee.Feature(None, {
                "date": ee.Date(img.get("system:time_start")).format("YYYY-MM-dd"),
                "NDVI": mean.get("NDVI")
            })

        return ee.FeatureCollection(ndvi_col.map(reduce_image))
