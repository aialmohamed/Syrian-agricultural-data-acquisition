from pathlib import Path
import sys




sys.path.append(str(Path(__file__).resolve().parent.parent))


from core.api_manager.api_connecter import ApiConnecter
from core.assets_manager.assets_region_loader import AssetsRegionLoader
from core.config_manager.config_dispatcher import ConfigDispatcher
from core.config_manager.config_loader import ConfigLoader
from core.config_manager.config_models import universal_factory
from core.api_manager.api_gee_loader import ApiGeeLoader

class SgrdDataAcquisitionStartup:
    """
    This class is responsible for starting the data acquisition process.
    It initializes the necessary components and starts the data acquisition.
    """

    def __init__(self): # type: ignore
        """
        Initializes the SgrdDataAcquisitionStartup class.
        :param satellites: List of satellite names to be used for data acquisition.
        """
        self.cfg = ConfigLoader()
        self.dispatcher = ConfigDispatcher(self.cfg)
        self.project_info = self.dispatcher.get_project_settings()
        self.project_model = universal_factory.from_config({"project": self.project_info })
        self.api_connecter = None
        self.region_info = self.dispatcher.get_region_settings()
        self.region_model = universal_factory.from_config({"parent": self.region_info})
        self.asset_loader = AssetsRegionLoader(self.region_model)
        self.region_ids = list(self.region_model.regions.keys())
        self.satellite_info = self.dispatcher.get_satellite_settings()
        self.satellite_ids = list(self.satellite_info.keys())

        

    def setup_core_and_connect_api(self):
        """
        Sets up the core 
        """
        self.api_connecter = ApiConnecter(self.project_model)
        self.api_connecter.authenticate_and_Initialize()
        self.api_connecter.check_engine_status()

    def load_available_satellites(self):
        """
        Loads the available satellites from the configuration.
        :return: List of available satellites.
        """
        return self.satellite_ids
    def load_available_regions(self):
        """
        Loads the available regions from the configuration.
        :return: List of available regions.
        """
        return self.region_ids
