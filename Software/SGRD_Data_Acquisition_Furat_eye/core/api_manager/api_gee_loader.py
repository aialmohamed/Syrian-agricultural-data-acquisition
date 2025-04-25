from core.assets_manager.assets_region_loader import AssetsRegionLoader
from core.config_manager.config_models.region_model import RegionAssets
from core.config_manager.config_models.satellites_model import SatelliteInfo
import ee
from datetime import datetime
class ApiGeeLoader:
    def __init__(self,start_date: str,end_date : str,region_model : RegionAssets,satellite_model : SatelliteInfo):
        self._region_model = region_model
        self._satellite_model = satellite_model
        self._start_date = start_date
        self._end_date = end_date
        self._collection = None
        self._region_loader = AssetsRegionLoader(self._region_model)
    


    def build_collection(self, region_id: str) -> ee.ImageCollection:
        """
        Build and validate an ImageCollection for a region.
        """
        if region_id not in self._region_model.regions:
            raise ValueError(f"Region ID '{region_id}' not found in the region model.")
        
        dataset_id = self._satellite_model.dataset_id
        geometry = self._region_loader.load_geometry(region_id)

        # Get actual collection time range for this region and dataset
        collection_start, collection_end = self._get_collection_date_range(dataset_id, geometry)

        # Convert to Python datetime for comparison
        user_start = datetime.strptime(self._start_date, "%Y-%m-%d")
        user_end = datetime.strptime(self._end_date, "%Y-%m-%d")
        collection_start_dt = datetime.strptime(collection_start, "%Y-%m-%d")
        collection_end_dt = datetime.strptime(collection_end, "%Y-%m-%d")

        # Validate the requested range
        if user_start < collection_start_dt or user_end > collection_end_dt:
            raise ValueError(
                f"Requested date range {self._start_date} to {self._end_date} "
                f"is out of bounds for dataset {dataset_id} in region '{region_id}'.\n"
                f"Available range: {collection_start} to {collection_end}."
            )

        # Safe to build collection
        self._collection = (
            ee.ImageCollection(dataset_id)
            .filterDate(self._start_date, self._end_date)
            .filterBounds(geometry)
        )
        return self._collection
    def _get_collection_date_range(self, dataset_id: str, region_geom: ee.Geometry) -> tuple[str, str]:
        """
        Get the start and end dates available in the dataset over the specified region.
        """
        collection = ee.ImageCollection(dataset_id).filterBounds(region_geom)
        start = ee.Date(collection.sort("system:time_start").first().get("system:time_start")).format("YYYY-MM-dd")
        end = ee.Date(collection.sort("system:time_start", False).first().get("system:time_start")).format("YYYY-MM-dd")
        return start.getInfo(), end.getInfo()
    
    