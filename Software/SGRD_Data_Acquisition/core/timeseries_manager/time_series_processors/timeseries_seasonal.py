import ee

class TimeSeriesSeasonal:
    """
    Class for processing seasonal time series data.
    """

    def __init__(self, timeseries_collection: ee.ImageCollection):
        """
        Initialize with an ImageCollection.
        """
        self._timeseries_collection = timeseries_collection

    def process(self, **kwargs) -> ee.ImageCollection:
        """
        Groups images by season and computes the mean image for each season.
        
        Returns:
            ee.ImageCollection: Seasonal mean composites.
        """
        seasons = [
            ["Winter", 12, 2],
            ["Spring", 3, 5],
            ["Summer", 6, 8],
            ["Fall", 9, 11],
        ]

        def seasonal_mean(season):
            season = ee.List(season)
            name = season.get(0)
            start_month = ee.Number(season.get(1))
            end_month = ee.Number(season.get(2))

            # Define filters
            def get_winter():
                return self._timeseries_collection.filter(
                    ee.Filter.Or(
                        ee.Filter.calendarRange(start_month, 12, "month"),
                        ee.Filter.calendarRange(1, end_month, "month")
                    )
                )

            def get_normal():
                return self._timeseries_collection.filter(
                    ee.Filter.calendarRange(start_month, end_month, "month")
                )

            # Pick filtered collection
            filtered = ee.ImageCollection(
                ee.Algorithms.If(start_month.gt(end_month), get_winter(), get_normal())
            )

            # Get earliest timestamp inside the If
            def get_timestamp():
                return filtered.sort("system:time_start").first().get("system:time_start")

            timestamp = ee.Algorithms.If(filtered.size().gt(0), get_timestamp(), ee.Date("2000-01-01").millis())

            # Create mean image and assign timestamp + season label
            mean_image = filtered.mean().set("season", name)
            return mean_image.set("system:time_start", timestamp)

        seasonal_images = ee.List(seasons).map(
            lambda season: ee.Image(seasonal_mean(season))
        )

        return ee.ImageCollection.fromImages(seasonal_images)