import yaml
from utils.paths import Paths

class ConfigUtils:
    def __init__(self):
        self.paths = Paths()
        with open(self.paths.project_config_path, 'r') as f:
            self._project_data = yaml.safe_load(f)
        with open(self.paths.assets_config_path, 'r') as f:
            self._assets_data = yaml.safe_load(f)
        with open(self.paths.satellite_config_path, 'r') as f:
            self._satellite_data = yaml.safe_load(f)
        self._assets = self._assets_data["Assets"]
        self._asset_parent = self._assets[0]["parent"]
        self._asset_names = self._assets[1:] 

    
    @property
    def project_id(self):
        return self._project_data["Project"]["ID"]
    @property
    def project_name(self):
        return self._project_data["Project"]["Name"]
    @property
    def project_description(self):
        return self._project_data["Project"]["Description"]
    @property
    def asset_parent(self):
        return self._asset_parent

    @property
    def asset_names(self):
        return self._asset_names
    @property
    def ndvi_landsat(self):
        return self._satellite_data["NDVI"]["LANDSAT"]
    @property
    def ndvi_modis(self):
        return self._satellite_data["NDVI"]["MODIS"]