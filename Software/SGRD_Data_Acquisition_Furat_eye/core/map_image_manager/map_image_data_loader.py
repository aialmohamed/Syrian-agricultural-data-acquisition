from typing import List
import ee
from pathlib import Path
import os
from core.paths_manager.system_paths import SystemPaths
class MapImageDataLoader:
    def __init__(self, 
                 time_series_collection: ee.ImageCollection,
                 region_name: str,
                 indicator_name: str,
                 start_date: str,
                 end_date: str,
                 visualization_params: dict = None,
                 region_geometry: ee.Geometry = None):
        """
        Initializes the MapImageDataLoader with a time series collection and settings.
        
        :param time_series_collection: ee.ImageCollection containing the time series data.
        :param region_name: Name of the region (e.g., 'SYRIA').
        :param indicator_name: Name of the indicator (e.g., 'NDVI').
        :param start_date: Start date string (e.g., '2020-01-01').
        :param end_date: End date string (e.g., '2020-12-31').
        :param visualization_params: Optional dictionary for visualization.
        """
        self.time_series_collection = time_series_collection
        self.visualization_params = visualization_params or {}
        self.region_name = region_name
        self.indicator_name = indicator_name
        self.start_date = start_date
        self.end_date = end_date
        


        self.system_paths = SystemPaths()
        self.fonts = self.system_paths.fonts_path
        self.arial = os.path.join(self.fonts, "ARIAL.TTF")
        # Create the folder structure
        self.output_folder = self._prepare_output_folder()

    def _prepare_output_folder(self):
        """
        Creates the folder structure: images/REGION/INDICATOR/STARTDATE_ENDDATE/
        """
        base_path = self.system_paths.image_path

        output_folder = base_path / self.region_name / self.indicator_name / f"{self.start_date}_{self.end_date}"
        
        output_folder.mkdir(parents=True, exist_ok=True)

        return output_folder

    def load_map_image(self) ->List[ee.ImageCollection]:
        """
        Placeholder for loading and exporting map images.
        """
        image_list = self.time_series_collection.toList(self.time_series_collection.size())
        return image_list
