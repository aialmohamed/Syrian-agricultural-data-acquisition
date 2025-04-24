from core.indicator_manager.indicator_registry import INDICATOR_REGISTRY
from core.indicator_manager.base_indicator import BaseIndicator
import ee

class IndicatorFactory:
    @staticmethod
    def create(key: str, collection: ee.ImageCollection) -> BaseIndicator:
        if key not in INDICATOR_REGISTRY:
            raise ValueError(f"❌ Unknown indicator key: {key}")
        return INDICATOR_REGISTRY[key](collection)