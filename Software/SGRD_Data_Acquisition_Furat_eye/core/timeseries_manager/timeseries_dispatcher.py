import ee

from core.timeseries_manager.time_series_processors import TimeSeriesAnomaly ,TimeSeriesMonthly ,TimeSeriesSeasonal ,TimeSeriesYearly


class TimeSeriesDispatcher:
    """
    Dispatcher class for handling time series data.
    """
    def __init__(self, timeseries_collection: ee.ImageCollection):
        """
        Initialize the TimeSeriesDispatcher with an ImageCollection.

        Args:
            timeseries_collection (ee.ImageCollection): The ImageCollection to be managed.
        """
        self._timeseries_collection = timeseries_collection
    def dispatch(self, mode: str, **kwargs):
        """
        Dispatch to the appropriate time series processor based on the mode.
        
        Args:
            mode (str): One of 'monthly', 'seasonal', 'anomaly', 'yearly'.
            kwargs: Additional arguments to pass to the processor.
        
        Returns:
            Any: Result from the time series processor.
        """
        mode = mode.lower()
        
        if mode == "monthly":
            processor = TimeSeriesMonthly(self._timeseries_collection)
        elif mode == "seasonal":
            processor = TimeSeriesSeasonal(self._timeseries_collection)
        elif mode == "anomaly":
            processor = TimeSeriesAnomaly(self._timeseries_collection)
        elif mode == "yearly":
            processor = TimeSeriesYearly(self._timeseries_collection)
        else:
            raise ValueError(f"Unknown dispatch mode: {mode}")

        return processor.process(**kwargs)
        