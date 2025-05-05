from typing import List
import ee
from pathlib import Path
import os
from core.paths_manager.system_paths import SystemPaths

class MapImageDataLoader:
    # TODO : this class needs to fix the visualization parameters so they are stored in config file and loaded later for use
    def __init__(self, 
                 time_series_collection: ee.ImageCollection,
                 region_name: str,
                 indicator_name: str,
                 start_date: str,
                 end_date: str,
                 color_pallet: List[str]= None,
                 assets_loader: object = None,):
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

        self.color_pallet = color_pallet
        self.region_name = region_name
        self.indicator_name = indicator_name
        self.start_date = start_date
        self.end_date = end_date
        self.assets_loader = assets_loader
        self.region_geometry = self.assets_loader.load_geometry(region_name) 

        self.max_visualization = 1
        self.min_visualization = 0
        self.visualization_params = self._set_visualization_params()
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
    def _set_visualization_params(self):
        """
        Sets the visualization parameters for the map image.
        """
        params = {
            'min': 0,
            'max': 1,
            'palette': self.color_pallet,
            'bands': ['NDVI']
        }
        return params

    def _compute_min_value(self) -> float:
            """
            Computes the minimum value of the time series collection.
            """
            min_value = self.time_series_collection.reduce(ee.Reducer.min()) \
                .reduceRegion(
                    reducer=ee.Reducer.min(),
                    geometry=self.region_geometry,
                    scale=30,
                    bestEffort=True,
                    maxPixels=1e13
                ).getInfo()

            # Assuming single band
            min= list(min_value.values())[0]
            self.min_visualization = min
            return self.min_visualization

    def _compute_max_value(self) -> float:
        """
        Computes the maximum value of the time series collection.
        """
        max_value = self.time_series_collection.reduce(ee.Reducer.max()) \
            .reduceRegion(
                reducer=ee.Reducer.max(),
                geometry=self.region_geometry,
                scale=30,
                bestEffort=True,
                maxPixels=1e13
            ).getInfo()

        # Assuming single band
        max = list(max_value.values())[0]
        self.max_visualization = max
        return self.max_visualization