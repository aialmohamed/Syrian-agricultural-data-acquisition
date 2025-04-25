

import ee
class TimeSeriesMonthly:
    """
    Class for processing monthly time series data.
    """
    def __init__(self, timeseries_collection):
        """
        Initialize the TimeSeriesMonthly with an ImageCollection.

        Args:
            timeseries_collection (ee.ImageCollection): The ImageCollection to be managed.
        """
        self._timeseries_collection = timeseries_collection

    def process(self, **kwargs) -> ee.ImageCollection:
        """
        Groups images by month and computes the mean image for each month.

        Args:
            kwargs: Additional arguments for processing.

        Returns:
            ee.ImageCollection: Processed ImageCollection.
        """
        # Implement the monthly processing logic here

        # filter images by month
        def monthly_mean(month):
            filtered_collection = self._timeseries_collection.filter(ee.Filter.calendarRange(month,month,'month'))
            return filtered_collection.mean().set('month', month)
        months = ee.List.sequence(1, 12)
        monthly_means = months.map(lambda month: monthly_mean(month))
        return ee.ImageCollection.fromImages(monthly_means)