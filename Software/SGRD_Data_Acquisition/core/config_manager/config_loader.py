from core.paths_manager.configurations_path import ConfigurationsPath

import yaml
from typing import Any
class ConfigLoader:
    """
    A class to load configuration files.
    """

    def __init__(self):
        """
        Initialize the ConfigLoader with a configuration file.

        :param config_file: Path to the configuration file.
        """
        self.config_path = ConfigurationsPath()
        self._config_cache = {}
         

    def load(self,key : str) -> dict[str,Any]:
        """
        Load the configuration file.

        :return: Loaded configuration : dict
        :raises FileNotFoundError: If the configuration file does not exist.
        """
        if key not in self.config_path.all():
            raise KeyError(
                f"Config key '{key}' not found. Available keys: {list(self._config_paths.keys())}"
            )
        if key not in self._config_cache:
            path = self.config_path.get(key)
            with open(path, "r", encoding="utf-8") as file:
                self._config_cache[key] = yaml.safe_load(file)
        return self._config_cache[key]
    
    def reload(self, key: str) -> dict[str, Any]:
        """
        Force reload the config from disk, bypassing cache.
        """
        if key not in self.config_path.all():
            raise KeyError(
                f"Config key '{key}' not found. Available keys: {list(self.config_path.all().keys())}"
            )

        path = self.config_path.get(key)
        with open(path, "r", encoding="utf-8") as f:
            self._config_cache[key] = yaml.safe_load(f)

        return self._config_cache[key]

    def keys(self) -> list[str]:
        return list(self.config_path.all().keys())
    
    def suggest_keys(self, partial: str) -> list[str]:
        return [k for k in self._config_paths if partial in k]