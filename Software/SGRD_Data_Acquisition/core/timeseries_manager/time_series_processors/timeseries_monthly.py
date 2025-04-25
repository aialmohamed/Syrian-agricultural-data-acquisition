

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
        Automatically sets system:time_start based on earliest image in that month.

        Returns:
            ee.ImageCollection: Monthly mean images with timestamps.
        """
        def monthly_mean(month):
            month = ee.Number(month)

            # Filter original collection by month
            filtered = self._timeseries_collection.filter(
                ee.Filter.calendarRange(month, month, "month")
            )

            # Get earliest system:time_start in that month
            first = filtered.sort("system:time_start").first()
            timestamp = first.get("system:time_start")

            # Compute monthly mean and set real timestamp
            mean_image = filtered.mean().set("month", month)
            return mean_image.set("system:time_start", timestamp)

        months = ee.List.sequence(1, 12)
        monthly_means = months.map(lambda m: monthly_mean(m))

        return ee.ImageCollection.fromImages(monthly_means)