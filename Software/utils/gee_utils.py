import ee 
from utils.config_utils import ConfigUtils

class GEEUtils:
    def __init__(self):

        self.project_cfg = ConfigUtils()
        self.asset_names = self.project_cfg.asset_names
        self.project_id = self.project_cfg.project_id

    def  authenticate(self):
        """
        Authenticate with Google Earth Engine.
        """
        ee.Authenticate()
        ee.Initialize(project=self.project_id)
        print(f"Authenticated with project ID: {self.project_id}")

    def get_area_asset(self, name):
        """
        Get the asset path for a specific area.
        :param name: Name of the area.
        :return: Asset path.
        """
        if name not in self.asset_names:
            raise ValueError(f"Asset name '{name}' not found in configuration.")
    
        return f"{self.project_cfg.asset_parent}{name}"

    
    
        