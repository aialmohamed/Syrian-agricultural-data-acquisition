

from core.api_manager.api_gee_loader import ApiGeeLoader
from core.collection_manager.collection_filtering import CollectionFiltering
from core.config_manager.config_models.region_model import RegionAssets
from core.config_manager.config_models.satellites_model import SatelliteInfo


class FurateyeCollectionLoader:
    """
    This class is responsible for loading the Furateye collection.
    """

    def __init__(self, region_id: str, satellite_id: str,region_model: RegionAssets,satellite_model : SatelliteInfo):
        """
        Initializes the FurateyeCollectionLoader with the path to the collection.
        :param region_id: The ID of the region.
        :param satellite_id: The ID of the satellite.
        :param region_model: The region model.
        """
        self.region_id = region_id
        self.satellite_id = satellite_id
        self.satellite_model = satellite_model
        self.region_model = region_model
        self.collection = None
        self.filtered_collection = None
    def load_raw_collection(self,start_date: str, end_date: str):
        """
        Loads the collection for the given region and satellite.
        :param start_date: The start date of the collection.
        :param end_date: The end date of the collection.
        :return: The loaded collection.
        """

        loader = ApiGeeLoader(start_date, end_date, self.region_model, self.satellite_model)
        self.collection = loader.build_collection(self.region_id)

        return self.collection
    def apply_cloud_masks_and_scale_to_collection(self):
        """
        Applies cloud masks to the collection.
        :return: The collection with cloud masks applied.
        """
        if self.collection is None:
            raise ValueError("Collection not loaded. Please load the collection first.")
        # Apply cloud masks to the collection
        # This is a placeholder for the actual implementation
        # You can replace this with your own logic
        collection = CollectionFiltering(self.collection,self.satellite_model).apply()
        self.filtered_collection = CollectionFiltering(collection,self.satellite_model).apply_scaling()
        
        return self.filtered_collection

