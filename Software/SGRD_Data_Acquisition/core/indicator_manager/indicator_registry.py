from core.indicator_manager.base_indicator import BaseIndicator
from core.indicator_manager.ndvi_indicator.ladnsat_8_ndvi import Landsat8Ndvi


INDICATOR_REGISTRY: dict[str, type[BaseIndicator]] = {
    "NDVI_LANDSAT_8": Landsat8Ndvi,
    #"NDVI_MODIS": ModisNdvi,
}