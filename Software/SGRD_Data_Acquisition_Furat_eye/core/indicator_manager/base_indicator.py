from abc import ABC, abstractmethod
import ee

class BaseIndicator(ABC):
    """
    Base class for all indicators.
    """

    def __init__(self, collection: ee.ImageCollection):
        self._collection = collection

    @abstractmethod
    def compute(self) -> ee.ImageCollection:
        """
        Compute the indicator.
        """
        pass
    def reduce(self, geometry: ee.Geometry, scale: int = 250) -> ee.FeatureCollection:
        """
        Optional: Reduce the computed indicator over a region.
        Default is to raise error unless overridden.
        """
        raise NotImplementedError("This indicator does not support reduction.")
    def composite(self, method="median") -> ee.Image:
        """
        Generate a composite image from the computed collection.
        Supported methods: 'median', 'mean', 'mosaic', etc.
        """
        computed = self.compute()
        if method == "median":
            return computed.median()
        elif method == "mean":
            return computed.mean()
        elif method == "mosaic":
            return computed.mosaic()
        else:
            raise ValueError(f"Unsupported composite method: {method}")