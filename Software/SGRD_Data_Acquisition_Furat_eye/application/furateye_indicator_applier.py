
import ee
from typing import List
from core.indicator_manager.indicator_factory import IndicatorFactory
from core.indicator_manager.indicator_registry import INDICATOR_REGISTRY
class FurateyeIndicatorApplier:
    """
    This class is responsible for applying the Furateye indicator to the data.
    """

    def __init__(self, indicators_type: List[str], collection: ee.ImageCollection):
        self.collection = collection
        self.indicators_type = indicators_type

    def apply_indicators(self) -> List[ee.ImageCollection]:
        """
        Apply the Furateye indicator/s to the data.
        """
        collections : List[ee.ImageCollection]= []
        for indicator in self.indicators_type:
            if indicator not in list(INDICATOR_REGISTRY.keys()):
                raise ValueError(f"Indicator {indicator} is not registered.")
            else:
                # apply the indicator
                indicator_factory = IndicatorFactory.create(indicator, self.collection)
                temp_collection = indicator_factory.compute()
                collections.append(temp_collection)
        return collections
    def apply_indicator_for_different_collection(self, indicator: List[str],collection: ee.ImageCollection) -> ee.ImageCollection:
        """
        Apply the Furateye indicators to new  data collection.
        if the data is not from the same satellite, then add the different collection and apply the indicator
        """
        collections : List[ee.ImageCollection]= []
        for indicator in self.indicators_type:
            if indicator not in list(INDICATOR_REGISTRY.keys()):
                raise ValueError(f"Indicator {indicator} is not registered.")
            else:
                # apply the indicator
                indicator_factory = IndicatorFactory.create(indicator, collection)
                temp_collection = indicator_factory.compute()
                collections.append(temp_collection)
        return collections
    def apply_indicator_and_reduce(self,assest_loader,region_id):
        """
        Apply the Furateye indicator/s to the data.
        """
        geometry = assest_loader.load_feature_collection(region_id).geometry()
        collections : List[ee.ImageCollection]= []
        for indicator in self.indicators_type:
            if indicator not in list(INDICATOR_REGISTRY.keys()):
                raise ValueError(f"Indicator {indicator} is not registered.")
            else:
                # apply the indicator
                indicator_factory = IndicatorFactory.create(indicator, self.collection)
                temp_collection = indicator_factory.reduce(geometry)
                collections.append(temp_collection)
        return collections
