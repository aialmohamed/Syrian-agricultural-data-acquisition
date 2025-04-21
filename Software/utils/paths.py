import os

class Paths:
    def __init__(self):
        # /Software/utils/paths.py ➜ go up two levels to /Project_Pilot_and_Main_Docs/
        self._software_path = os.path.dirname(os.path.abspath(__file__))  # .../utils
        self._root = os.path.abspath(os.path.join(self._software_path, "..", ".."))
        
        self._folium_path = os.path.join(self._root, 'Folium_out')
        self._config_path = os.path.join(self._root, 'Software', 'Config')
        self._project_config_path = os.path.join(self._config_path, 'project_configs.yaml')
        self._assets_config_path = os.path.join(self._config_path, 'assets_configs.yaml')
        self._satellite_config_path = os.path.join(self._config_path, 'satellite_configs.yaml')

    @property
    def folium_path(self):
        return self._folium_path

    @property
    def root(self):
        return self._root

    @property
    def software_path(self):
        return self._software_path

    @property
    def config_path(self):
        return self._config_path

    @property
    def project_config_path(self):
        return self._project_config_path
    @property
    def assets_config_path(self):
        return self._assets_config_path
    @property
    def satellite_config_path(self):
        return self._satellite_config_path
