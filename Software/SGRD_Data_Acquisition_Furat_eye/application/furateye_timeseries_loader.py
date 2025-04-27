

from typing import List
import ee

from core.timeseries_manager.timeseries_dispatcher import TimeSeriesDispatcher
from core.timeseries_manager.timeseries_loader import TimeSeriesLoader


class FurateyeTimeseriesLoader:
    """
    Class to load timeseries data from a FuraEye file.
    """

    def __init__(self, collection : List[ee.ImageCollection]):
        """
        Initialize the loader with the collection and date range.

        Args:
            collection (ee.ImageCollection): The image collection to load data from.
        """
        self.collection = collection
        self.loader = [TimeSeriesLoader(collection) for collection in self.collection]


    def create_timeseries_by_year(self,year : int) -> List[ee.ImageCollection]:
        """
        create a timeseries for a specific year.
        Args:
            year (int): The year to load data for.
        Returns:
            ee.ImageCollection: The loaded data for the specified year.
        """
        time_series_by_year = []
        for loader in self.loader:
            time_series_by_year.append(loader.filter_and_sort_by_year(year))
        return time_series_by_year

    def create_timeseries_by_date(self,start_date: str, end_date: str) -> List[ee.ImageCollection]:
        """
        create a timeseries for a specific date range.
        Args:
            start_date (str): Start date in the format 'YYYY-MM-DD'.
            end_date (str): End date in the format 'YYYY-MM-DD'.
        Returns:
            ee.ImageCollection: The loaded data for the specified date range.

        """
        time_series_by_date = []
        for loader in self.loader:
            time_series_by_date.append(loader.filter_and_sorted_by_date(start_date, end_date))
        return time_series_by_date
    
    def load_timeseries_as_months(self, time_series_collection: ee.ImageCollection) -> ee.ImageCollection:
        """
        Load the timeseries data as monthly data.
        Returns:
            ee.ImageCollection: The loaded monthly data.
        """
        dispatcher = TimeSeriesDispatcher(time_series_collection)
        timeseries_monthly = dispatcher.dispatch("monthly")
        return timeseries_monthly
    def load_timeseries_as_seasonal(self,time_series_collection: ee.ImageCollection) -> ee.ImageCollection:
        """
        Load the timeseries data as seasonal data.
        Returns:
            ee.ImageCollection: The loaded seasonal data.
        """
        dispatcher = TimeSeriesDispatcher(time_series_collection)
        timeseries_seasonal = dispatcher.dispatch("seasonal")
        return timeseries_seasonal
    def load_timeseries_as_anomaly(self,time_series_collection: ee.ImageCollection ) -> ee.ImageCollection:
        """
        Load the timeseries data as anomaly data.
        Returns:
            ee.ImageCollection: The loaded anomaly data.
        """
        dispatcher = TimeSeriesDispatcher(time_series_collection)
        timeseries_anomaly = dispatcher.dispatch("anomaly")
        return timeseries_anomaly
    def load_timeseries_as_years(self,time_series_collection: ee.ImageCollection) -> ee.ImageCollection:
        """
        Load the timeseries data as yearly data.
        Returns:
            ee.ImageCollection: The loaded yearly data.
        """
        dispatcher = TimeSeriesDispatcher(time_series_collection)
        timeseries_yearly = dispatcher.dispatch("yearly")
        return timeseries_yearly