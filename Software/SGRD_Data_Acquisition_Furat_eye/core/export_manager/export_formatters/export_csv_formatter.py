import ee

class ExportCSVFormatter:
    def __init__(self, payload: dict):
        self.data = payload["data"]
        self.region = payload["region"]
        self.scale = payload["scale"]
        self.region_id = payload.get("region_id", "region")  

    def format(self):
        if isinstance(self.data, ee.Image):
            reduced = self.data.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=self.region.geometry(),
                scale=self.scale,
                maxPixels=1e13
            )
            return [{"date": "composite", "region_id": self.region_id, **reduced.getInfo()}]

        elif isinstance(self.data, ee.ImageCollection):
            def reducer(img):
                mean = img.reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=self.region,
                    scale=self.scale,
                    maxPixels=1e13
                )
                date = ee.Date(img.get("system:time_start")).format("YYYY-MM-dd")
                return ee.Feature(None, mean.set("date", date).set("region_id", self.region_id)) 

            features = self.data.map(reducer)
            feature_list = features.toList(features.size())
            feature_info = feature_list.map(lambda f: ee.Feature(f).toDictionary())
            return feature_info.getInfo()

        else:
            raise TypeError("Unsupported data type: must be ee.Image or ee.ImageCollection")
