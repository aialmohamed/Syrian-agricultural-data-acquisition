from core.paths_manager.system_paths import SystemPaths
from pathlib import Path

class ConfigurationsPath:
    def __init__(self):
        self._config_root = SystemPaths().config_dir
        self._configs = {
            str(p.relative_to(self._config_root).with_suffix("")).replace("\\", "/"): p
            for p in self._config_root.rglob("*.yaml")
        }

    def get(self, key: str) -> Path:
        try:
            return self._configs[key]
        except KeyError:
            raise KeyError(f"Config key '{key}' not found. Available keys: {list(self._configs.keys())}")
    
    def show_available_keys(self):
        print("\n🗂️   Available configuration keys:")
        for key in self.all():
            print(" -", key)

    def all(self) -> dict:
        return self._configs

    @property
    def project_config(self) -> Path:
        return self.get("general/project_configurations")

    @property
    def satellite_config(self) -> Path:
        return self.get("satellites/satellites_configurations")

    @property
    def region_config(self) -> Path:
        return self.get("assets/region/region_configurations")
