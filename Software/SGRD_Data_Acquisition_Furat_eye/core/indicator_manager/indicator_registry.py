from core.indicator_manager.base_indicator import BaseIndicator
from core.indicator_manager.vegetation_indicator.ladnsat_8_ndvi import Landsat8Ndvi
from core.indicator_manager.vegetation_indicator.modis_ndvi import ModisNdvi
from core.indicator_manager.salinity_indicator.landsat_8_ndsi import Landsat8NDSI
from core.indicator_manager.vegetation_indicator.landsat_7_ndvi import Landsat7Ndvi
from core.indicator_manager.precipitation_indicator.ucsb_precipitation import UcsbPrecipitation


INDICATOR_REGISTRY: dict[str, type[BaseIndicator]] = {
    "NDVI_LANDSAT_8": Landsat8Ndvi,
    "NDVI_MODIS": ModisNdvi,
    "NDSI_LANDSAT_8":Landsat8NDSI,
    "PRECIPITATION_UCSB": UcsbPrecipitation,
    "NDVI_LANDSAT_7": Landsat7Ndvi,
}