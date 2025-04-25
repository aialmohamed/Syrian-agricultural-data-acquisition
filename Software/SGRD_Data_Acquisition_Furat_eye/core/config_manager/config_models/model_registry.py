from .project_info_model import ProjectInfo
from .satellites_model import SatelliteInfo
from .region_model import RegionAssets


MODEL_REGISTRY ={
    "project": ProjectInfo,
    "satellites": SatelliteInfo,
    "parent": RegionAssets,
}