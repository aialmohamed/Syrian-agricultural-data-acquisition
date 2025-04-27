class ExportLoader:
    """
    Class to load export data (either time series or composite data).
    """

    def __init__(self, data, export_region, export_type="csv", export_scale=255, export_region_id= None):
        self.data = data
        self.export_region = export_region
        self.export_type = export_type
        self.export_scale = export_scale
        self._region_id = export_region_id

    def _extract_region_id(self):
        try:
            if self.export_source:
                info = self.export_source.getInfo()
                if "id" in info:
                    return info["id"].split("/")[-1]
            return "custom_region"
        except Exception as e:
            print(f"⚠️ Could not extract region ID: {e}")
            return "unknown_region"

    def load(self):
        return {
            "data": self.data,
            "region": self.export_region,
            "type": self.export_type,
            "scale": self.export_scale,
            "region_id": self._region_id
        }
