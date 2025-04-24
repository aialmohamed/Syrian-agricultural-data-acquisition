import sys
from pathlib import Path


# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.config_manager.config_models import ProjectInfo, SatelliteInfo, RegionAssets, ConfigModel, universal_factory
from core.config_manager import ConfigLoader, ConfigDispatcher
from core.api_manager.api_connecter import ApiConnecter

def main():
    cfg = ConfigLoader()
    dispatcher = ConfigDispatcher(cfg)
    projet_info = dispatcher.get_project_settings()
    project_model = universal_factory.from_config({"project": projet_info})

    api_connecter = ApiConnecter(project_model)
    api_connecter.authenticate_and_initialise()
    api_connecter.check_engine_status()

    #print("All Configurations:", configurations_path.all())
if __name__ == "__main__":
    main()