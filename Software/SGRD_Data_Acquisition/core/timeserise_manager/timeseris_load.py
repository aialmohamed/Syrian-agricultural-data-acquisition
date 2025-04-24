



import ee


class TimeSeriesLoader:
    def __init__(self, indicator_data : ee.ImageCollection):
        self._indicator_data = indicator_data

    def sort_by_time(self) -> ee.ImageCollection:
        """
        Sort the ImageCollection by time.
        """
        return self._indicator_data.sort("system:time_start")
    def filter_by_year(self,year : int) -> ee.ImageCollection:
        start = ee.Date(f"{year}-01-01")
        end = start.advance(1,'year')
        return self._indicator_data.filterDate(start, end)
    def group_by_monthly_median(self) -> ee.ImageCollection:

        months = ee.List.sequence(1, 12)
        def monthly_median(month,year):
            start = ee.Date.fromYMD(year,ee.Number(month),1)
            end = start.advance(1,'month')
            filtered  = self._indicator_data.filterDate(start, end)
            median = filtered.median().set('month', month)
            return median
        return ee.ImageCollection(months.map(monthly_median))