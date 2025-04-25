import ee
from datetime import datetime

class TimeSeriesLoader:
    def __init__(self, indicator_data : ee.ImageCollection):
        self._indicator_data = indicator_data

    def sort_by_time(self) -> ee.ImageCollection:
        """
        Sort the ImageCollection by time.
        Returns:
            ee.ImageCollection: Sorted ImageCollection.
        """
        return self._indicator_data.sort("system:time_start")
    def filter_by_year(self,year : int) -> ee.ImageCollection:
        start = ee.Date(f"{year}-01-01")
        end = start.advance(1,'year')
        return self._indicator_data.filterDate(start, end)
    def filter_and_sort_by_year(self,year : int) -> ee.ImageCollection:
        """
        Filter the ImageCollection by year and sort it by time.
        Args:
            year (int): Year to filter by.
        Returns:
            ee.ImageCollection: Filtered and sorted ImageCollection.
        """
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"

        if not self.verify_collection_time_in_timeseries_time_range(start_date, end_date):
            raise ValueError(f"The requested year {year} is out of range for this dataset ( check the api loader in your code). time range from api loader is {self._get_collection_date_range()}")
        
        return self.filter_by_year(year).sort("system:time_start")
    def filter_and_sorted_by_date(self, start_date: str, end_date: str) -> ee.ImageCollection:
        """
        Filter the ImageCollection by date range.
        Args:
            start_date (str): Start date in the format 'YYYY-MM-DD'.
            end_date (str): End date in the format 'YYYY-MM-DD'.
        Returns:
            ee.ImageCollection: Filtered and sorted ImageCollection.
        """
        if not self.verify_collection_time_in_timeseries_time_range(start_date, end_date):
            raise ValueError(f"The requested range {start_date} to {end_date} is outside the collection's available range( check the api loader in your code). time range from api loader is {self._get_collection_date_range()}")
        

        start = ee.Date(start_date)
        end = ee.Date(end_date)
        return self._indicator_data.filterDate(start, end).sort("system:time_start")
    def _get_collection_date_range(self) -> tuple[str, str]:
        """
        Returns the actual available date range of the image collection.

        Returns:
            (start_date_str, end_date_str) in "YYYY-MM-DD" format
        """
        start = ee.Date(self._indicator_data.sort("system:time_start").first().get("system:time_start")).format("YYYY-MM-dd")
        end = ee.Date(self._indicator_data.sort("system:time_start", False).first().get("system:time_start")).format("YYYY-MM-dd")

        return start.getInfo(), end.getInfo()
    
    def verify_collection_time_in_timeseries_time_range(self, start_date: str, end_date: str) -> bool:
        """
        Check if the requested date range is inside the collection's available time range.
        
        Args:
            start_date (str): Start date (e.g. '2015-01-01')
            end_date (str): End date (e.g. '2023-12-31')

        Returns:
            bool: True if requested range is valid; False otherwise.
        """


        collection_start, collection_end = self._get_collection_date_range()
        collection_start_dt = datetime.strptime(collection_start, "%Y-%m-%d")
        collection_end_dt = datetime.strptime(collection_end, "%Y-%m-%d")
        requested_start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        requested_end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        return requested_end_dt >= collection_start_dt and requested_start_dt <= collection_end_dt