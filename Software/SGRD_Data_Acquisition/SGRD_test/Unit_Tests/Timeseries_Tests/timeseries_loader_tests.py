import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path
import ee
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from core.timeseries_manager.timeseries_loader import TimeSeriesLoader

class TestTimeSeriesLoader(unittest.TestCase):
    def setUp(self):
        # Mock data 
        self.mock_collection = MagicMock(spec=ee.ImageCollection)
        self.loader = TimeSeriesLoader(self.mock_collection)
    
    def test_sort_vy_time(self):

        sorted_collection = MagicMock()
        self.mock_collection.sort.return_value = sorted_collection

        result = self.loader.sort_by_time()

        #Assert
        self.mock_collection.sort.assert_called_once_with("system:time_start")
        self.assertEqual(result, sorted_collection)
    @patch("core.timeserise_manager.timeseris_load.ee.Date")
    def test_filter_by_year(self, mock_ee_date):
        year = 2020
        start_date = MagicMock()
        end_date = MagicMock()

        mock_ee_date.return_value = start_date
        start_date.advance.return_value = end_date

        filtered_collection = MagicMock()
        self.mock_collection.filterDate.return_value = filtered_collection

        result = self.loader.filter_by_year(year)

        mock_ee_date.assert_called_once_with("2020-01-01")
        start_date.advance.assert_called_once_with(1, 'year')
        self.mock_collection.filterDate.assert_called_once_with(start_date, end_date)
        self.assertEqual(result, filtered_collection)
    @patch("core.timeserise_manager.timeseris_load.ee.Date")
    def test_filter_and_sort_by_year(self, mock_ee_date):
        year = 2020
        start_date = MagicMock()
        end_date = MagicMock()

        mock_ee_date.return_value = start_date
        start_date.advance.return_value = end_date

        filtered_collection = MagicMock()
        sorted_collection = MagicMock()

        self.mock_collection.filterDate.return_value = filtered_collection
        filtered_collection.sort.return_value = sorted_collection

        result = self.loader.filter_and_sort_by_year(year)

        mock_ee_date.assert_called_once_with("2020-01-01")
        start_date.advance.assert_called_once_with(1, 'year')
        self.mock_collection.filterDate.assert_called_once_with(start_date, end_date)
        filtered_collection.sort.assert_called_once_with("system:time_start")
        self.assertEqual(result, sorted_collection)
    @patch("core.timeserise_manager.timeseris_load.ee.Date")
    def test_filter_and_sorted_by_date(self, mock_ee_date):
        start_date = "2020-01-01"
        end_date = "2020-12-31"

        start = MagicMock()
        end = MagicMock()

        # Return `start` on first call, `end` on second
        mock_ee_date.side_effect = [start, end]
        filtered_collection = MagicMock()
        sorted_collection = MagicMock()

        # Set up the chain: filterDate → sort → final result
        self.mock_collection.filterDate.return_value = filtered_collection
        filtered_collection.sort.return_value = sorted_collection

        result = self.loader.filter_and_sorted_by_date(start_date, end_date)

        mock_ee_date.assert_any_call(start_date)
        mock_ee_date.assert_any_call(end_date)
        self.mock_collection.filterDate.assert_called_once_with(start, end)
        filtered_collection.sort.assert_called_once_with("system:time_start")
        self.assertEqual(result, sorted_collection)

if __name__ == "__main__":
    unittest.main()
