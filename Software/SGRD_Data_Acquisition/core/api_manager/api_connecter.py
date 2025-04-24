from core.config_manager.config_models.project_info_model import ProjectInfo
import ee

class ApiConnecter:
    def __init__(self, project_info :ProjectInfo):
        self._project_info = project_info
        self._project_id = project_info.ID
    
    def authenticate_and_initialise(self):
        """
        Authenticate and initialize Earth Engine.
        """
        try:
            ee.Initialize(project=self._project_id)
            print("🌍 Earth Engine already initialized.")
        except Exception:
            print("🔑 Authenticating Earth Engine...")
            ee.Authenticate()
            ee.Initialize(project=self._project_id)
    def check_engine_status(self):
        test_asset = f"projects/{self._project_id}/assets/Areas/{'SYRIA_EAST_AOI'}"
        try:
            asset_info = ee.data.getAsset(test_asset)
            print("✅ Earth Engine asset is reachable.")
        except Exception as e:
            print("❌ Earth Engine asset test failed:", e)