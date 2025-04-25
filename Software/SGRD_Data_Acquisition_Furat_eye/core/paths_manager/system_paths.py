from pathlib import Path

class SystemPaths:
    def __init__(self, root_path: Path = None):
        self._root = root_path or Path(__file__).resolve().parents[2]

        # Private attributes
        self._config_dir = self._root / "config"
        self._core_dir = self._root / "core"
        self._scripts_dir = self._root / "scripts"
        self._ui_dir = self._root / "ui"
        self._tests_dir = self._root / "SGRD_test"
        self._cli_patch_dir = self._root / "cli_patch"
        self._data_path_dir = self._root / "data"

        self._requirements_file = self._root / "requirements.txt"

    # Read-only properties
    @property
    def root(self): return self._root

    @property
    def config_dir(self): return self._config_dir

    @property
    def core_dir(self): return self._core_dir

    @property
    def scripts_dir(self): return self._scripts_dir

    @property
    def ui_dir(self): return self._ui_dir

    @property
    def tests_dir(self): return self._tests_dir

    @property
    def cli_patch_dir(self): return self._cli_patch_dir

    @property
    def requirements_file(self): return self._requirements_file

    @property
    def assets_config(self): return self._assets_config

    @property
    def project_config(self): return self._project_config

    @property
    def satellite_config(self): return self._satellite_config
    @property
    def data_path(self): return self._data_path_dir

    def __repr__(self):
        return f"<SystemPaths root={self.root}>"
