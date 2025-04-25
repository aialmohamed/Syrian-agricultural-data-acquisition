import unittest
import ee
import sys
from pathlib import Path
from datetime import datetime, timezone
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from core.timeseries_manager.timeseries_loader import TimeSeriesLoader
class TestTimeSeriesLoaderIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        project_Id = "sgrd-smart-farming"
        # Real Earth Engine initialization
        ee.Initialize(project=project_Id)

        # Using real MODIS NDVI ImageCollection
        cls.collection = ee.ImageCollection("MODIS/061/MOD13Q1")
        cls.loader = TimeSeriesLoader(cls.collection)

    def test_filter_by_year_actual_data(self):
        year = 2020
        filtered = self.loader.filter_by_year(year)

        size = filtered.size().getInfo()  # Get the actual number of images
        print(f"Images in {year}: {size}")

        # Check that it returned something
        self.assertGreater(size, 0)

        # Check that all images are within 2020
        def check_date(img):
            date = ee.Date(img.get("system:time_start")).get("year")
            return ee.Number(date).eq(year)

        all_in_year = filtered.map(lambda img: img.set("in_year", check_date(img)))
        all_in_year_list = all_in_year.aggregate_array("in_year").getInfo()

        self.assertTrue(all(all_in_year_list))

    def test_sort_by_time_order(self):
        sorted_collection = self.loader.sort_by_time()
        list_of_dates = sorted_collection.aggregate_array("system:time_start").getInfo()

        dates = [datetime.fromtimestamp(d / 1000, tz=timezone.utc) for d in list_of_dates]
        # Verify chronological order
        self.assertEqual(dates, sorted(dates))

    def test_filter_and_sort_by_year(self):
        year = 2018
        filtered_sorted = self.loader.filter_and_sort_by_year(year)
        size = filtered_sorted.size().getInfo()
        print(f"Filtered and sorted images in {year}: {size}")
        self.assertGreater(size, 0)
        # Check that all images are within 2018
        def check_date(img):
            date = ee.Date(img.get("system:time_start")).get("year")
            return ee.Number(date).eq(year)
        all_in_year = filtered_sorted.map(lambda img: img.set("in_year", check_date(img)))
        all_in_year_list = all_in_year.aggregate_array("in_year").getInfo()
        self.assertTrue(all(all_in_year_list))
        # Check that the collection is sorted
        list_of_dates = filtered_sorted.aggregate_array("system:time_start").getInfo()
        dates = [datetime.fromtimestamp(d / 1000, tz=timezone.utc) for d in list_of_dates]
        self.assertEqual(dates, sorted(dates))
        
        # Check that the first image is from the start of the year
        first_image_date = ee.Date(filtered_sorted.first().get("system:time_start")).getInfo()
        first_image_timestamp = first_image_date["value"]
        first_image_year = datetime.fromtimestamp(first_image_timestamp / 1000, tz=timezone.utc).year
        self.assertEqual(first_image_year, year)
    def test_filter_and_sorted_by_date(self):
        start_date = "2020-01-01"
        end_date = "2020-12-31"
        filtered_sorted = self.loader.filter_and_sorted_by_date(start_date, end_date)
        size = filtered_sorted.size().getInfo()
        print(f"Filtered and sorted images from {start_date} to {end_date}: {size}")
        self.assertGreater(size, 0)
        # Check that all images are within the date range
        def check_date(img):
            date_millis = ee.Date(img.get("system:time_start")).millis()
            start_millis = ee.Date(start_date).millis()
            end_millis = ee.Date(end_date).millis()
            return date_millis.gte(start_millis).And(date_millis.lte(end_millis))
        all_in_range = filtered_sorted.map(lambda img: img.set("in_range", check_date(img)))
        all_in_range_list = all_in_range.aggregate_array("in_range").getInfo()
        self.assertTrue(all(all_in_range_list))
        # Check that the collection is sorted
        list_of_dates = filtered_sorted.aggregate_array("system:time_start").getInfo()
        dates = [datetime.fromtimestamp(d / 1000, tz=timezone.utc) for d in list_of_dates]
        self.assertEqual(dates, sorted(dates))


if __name__ == "__main__":
    unittest.main()
