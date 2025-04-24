import ee
import matplotlib.pyplot as plt
import calendar
import plotly.graph_objs as go
from utils.ndvi_utils import NDVIUtils
class NdviChartingUtils:
    """
    A class to handle charting utilities.
    """

    def __init__(self,ndvi_collection,year):
        self.year = year
        self.months = months = ee.List.sequence(1, 12)
        self._ndvi_collection = ndvi_collection
        self.monthly_collection = None
        self.date,self.ndvi_vals = None, None            
        self.region_path = self._ndvi_collection.region.getInfo()['id']
        self.region_name = self.region_path.split('/')[-1]

    def monthly_median(self,month):
        
        month = ee.Number(month)
        year = ee.Number(self.year)
        start = ee.Date.fromYMD(self.year, month, 1)
        end = start.advance(1, 'month')

        filtered = self._ndvi_collection.create_ndvi_data().filterDate(start, end)
        median = filtered.median()

        return median.set({
            'month': month,
            'year': year,
            'label': start.format('YYYY-MM-dd')
        })
    def generate_monthly_collection(self):
        self.monthly_collection = ee.ImageCollection(
            self.months.map(lambda m: self.monthly_median(m))
        )
        return self.monthly_collection
    
    def get_aggregated_collection_by_date(self,reduced_fc):
        """
        Aggregates NDVI values and dates from a reduced feature collection and stores them in class attributes.
        """
        self.date , self.ndvi_vals = self._ndvi_collection.aggregate_ndvi_by_date(reduced_fc)

    def plot_multi_year_ndvi(self, start_year, end_year):
        """
        Plot interactive multi-year NDVI trends with months on x-axis and one line per year (clickable legend).
        if the start_year == end_year, it will plot the NDVI for that year only.
        Args:
            start_year (int): Start year for NDVI data.
            end_year (int): End year for NDVI data.
        """
        traces = []

        for year in range(start_year, end_year + 1):
            print(f"Processing year {year}...")

            ndvi = NDVIUtils(
                satellite=self._ndvi_collection.satellite,
                start_date=f"{year}-01-01",
                end_date=f"{year}-12-31",
                region=self._ndvi_collection.region,
                mode=self._ndvi_collection.mode
            )


            temp = NdviChartingUtils(ndvi, year)
            temp.generate_monthly_collection()
            reduced_fc = temp.monthly_collection.map(lambda img: ndvi.reduce_monthly_ndvi(img))
            temp.get_aggregated_collection_by_date(reduced_fc)

            # Create NDVI values per month
            month_ndvi = [None]*12
            for date, ndvi_val in zip(temp.date, temp.ndvi_vals):
                month = date.month
                month_ndvi[month - 1] = ndvi_val

            trace = go.Scatter(
                x=[calendar.month_abbr[m] for m in range(1, 13)],
                y=month_ndvi,
                mode='lines+markers',
                name=str(year),
                visible=True
            )
            traces.append(trace)

        layout = go.Layout(
            title=f'Monthly NDVI Trends ({self.region_name}, {start_year}–{end_year})',
            xaxis=dict(title='Month'),
            yaxis=dict(title='NDVI'),
            legend=dict(title='Year'),
            hovermode='x unified'
        )

        fig = go.Figure(data=traces, layout=layout)
        fig.show()

