



import csv
from typing import List

from core.charting_manager.charting_data_loader import ChartingDataLoader
from core.charting_manager.charting_data_plotter import ChartingDataPlotter


class FurateyeSimpleChartingLoader:
    """
    This class is responsible for loading the FuratEye Simple Charting data.
    """

    def __init__(self, files: List[str]):
        self.files = files

    def load_data(self) -> List[dict]:
        """
        Load the FuratEye Simple Charting data.
        """
        data = []
        charting_data_loader = ChartingDataLoader()
        for file in self.files:
            file_data = charting_data_loader.load_data(file)
            data.extend(file_data)
        return data
    def plot_indicators(self,data: List[dict]):
        """
        Plot the indicators using the loaded data.
        """
        plotter = ChartingDataPlotter(data)
        plotter.plot_indicators()
    def plot_and_interpolate(self,data: List[dict]):
        """
        Plot and interpolate the data.
        """
        plotter = ChartingDataPlotter(data)
        plotter.plot_and_interpolate()