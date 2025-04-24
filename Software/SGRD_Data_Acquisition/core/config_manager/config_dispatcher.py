from core.config_manager.config_loader import ConfigLoader
from typing import Any



class ConfigDispatcher:
    def __init__(self, loader: ConfigLoader):
        """
        Initialize the ConfigDispatcher with a ConfigLoader instance.

        :param loader: An instance of ConfigLoader.
        """
        self._loader = loader

    def get_project_settings(self) -> dict[str, Any]:
        """
        Get project settings from the configuration.

        :return: Project settings as a dictionary.
        """
        cfg = self._loader.load("general/project_configurations")
        return cfg.get("project", {})
    def get_satellite_settings(self) -> dict[str, Any]:
        """
        Get satellite settings from the configuration.
        :return: Satellite settings as a dictionary.
        """
        cfg = self._loader.load("satellites/satellites_configurations")
        return cfg.get("satellites", {})
    
    def get_region_settings(self) -> dict[str, Any]:
        """
        Get region settings from the configuration.
        :return: Region settings as a dictionary.
        """
        cfg = self._loader.load("assets/region/region_configurations")
        return cfg["assets"]
    
    def print_available_keys(self):
        print("\n🔑 Available Config Keys:")
        for k in self._loader.keys():
            print(f" - {k}")

