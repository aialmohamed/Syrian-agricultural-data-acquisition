

import ee
class TimeSeriesYearly:
    """
    Class for processing yearly time series data.
    """

    def __init__(self, timeseries_collection):
        """
        Initialize the TimeSeriesYearly with an ImageCollection.

        Args:
            timeseries_collection (ee.ImageCollection): The ImageCollection to be managed.
        """
        self._timeseries_collection = timeseries_collection

    def process(self, **kwargs) -> ee.ImageCollection:
        """
        Process the time series data to extract yearly statistics.

        Args:
            kwargs: Additional arguments for processing.

        Returns:
            ee.ImageCollection: Processed yearly statistics.
        """
        # get years :
        years  = self._timeseries_collection.aggregate_array("system:time_start").map(lambda date: ee.Date(date).get("year")).distinct()

        def yearly_mean(year):
            year = ee.Number(year)
            filtered = self._timeseries_collection.filter(ee.Filter.calendarRange(year,year,"year"))
            mean = filtered.mean().set("year",year)
            return mean
        yearly_images = years.map(lambda year:yearly_mean(year))
        return ee.ImageCollection.fromImages(yearly_images)
