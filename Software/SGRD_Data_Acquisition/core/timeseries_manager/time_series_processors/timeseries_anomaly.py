
import ee


class TimeSeriesAnomaly:
    """
    Class for processing time series data to detect anomalies.
    """
    def __init__(self, timeseries_collection):
        """
        Initialize the TimeSeriesAnomaly with an ImageCollection.

        Args:
            timeseries_collection (ee.ImageCollection): The ImageCollection to be managed.
        """
        self._timeseries_collection = timeseries_collection
    def process(self, **kwargs) -> ee.ImageCollection:
        """
        Process the time series to detect anomalies using z-score.

        Args:
            kwargs:
                - threshold (float): Z-score threshold to consider a value an anomaly. Default is 3.

        Returns:
            ee.ImageCollection: Collection of anomaly-detected images.
        """
        threshold = kwargs.get("threshold", 3)
        mean = self._timeseries_collection.mean()
        std_dev = self._timeseries_collection.reduce(ee.Reducer.stdDev())
        def compute_z_score(image):
            z = image.subtract(mean).divide(std_dev).rename("z_score")
            anomaly = z.abs().gt(threshold).rename("anomaly_mask")
            return image.addBands(z).addBands(anomaly).copyProperties(image, ["system:time_start"])
        
        return self._timeseries_collection.map(compute_z_score)