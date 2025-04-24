from core.assets_manager.assets_region_loader import AssetsRegionLoader
from core.config_manager.config_models.region_model import RegionAssets
from core.config_manager.config_models.satellites_model import SatelliteInfo
import ee

class ApiGeeLoader:
    def __init__(self,start_date: str,end_date : str,region_model : RegionAssets,satellite_model : SatelliteInfo):
        self._region_model = region_model
        self._satellite_model = satellite_model
        self._start_date = start_date
        self._end_date = end_date
        self._collection = None
        self._region_loader = AssetsRegionLoader(self._region_model)
    


    def build_collection(self,region_id: str) -> ee.ImageCollection:
        if region_id not in self._region_model.regions:
            raise ValueError(f"Region ID '{region_id}' not found in the region model.")
        dataset_id = self._satellite_model.dataset_id
        geometry = self._region_loader.load_geometry(region_id)

        self._collection = (
            ee.ImageCollection(dataset_id)
            .filterDate(self._start_date, self._end_date)
            .filterBounds(geometry)
        )
        return self._collection
    