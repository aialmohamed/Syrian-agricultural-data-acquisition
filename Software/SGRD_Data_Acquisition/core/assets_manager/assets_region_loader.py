import ee
from core.config_manager.config_models.region_model import RegionAssets


class AssetsRegionLoader:
    def __init__(self,region_assets: RegionAssets):
        self._region_assets = region_assets
        self._region_parent = region_assets.parent

    def load_geometry(self, region_id: str) -> ee.Geometry:
        if region_id not in self._region_assets.regions:
            raise ValueError(f"❌ Region ID '{region_id}' not found in region assets.")
        path = "/".join([self._region_parent.rstrip("/"), region_id])
        return ee.FeatureCollection(path).geometry()
    
    def load_feature_collection(self,region_id : str) -> ee.FeatureCollection:
        if region_id not in self._region_assets.regions:
            raise ValueError(f"❌ Region ID '{region_id}' not found in region assets.")
        path = "/".join([self._region_parent.rstrip("/"), region_id])
        return ee.FeatureCollection(path)
