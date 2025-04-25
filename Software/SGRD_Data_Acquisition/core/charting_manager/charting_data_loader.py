import os
import csv
from typing import List, Dict

from core.paths_manager.system_paths import SystemPaths


class ChartingDataLoader:
    """
    This class is responsible for loading charting data.
    """

    def __init__(self):
        """
        Initialize the ChartingDataLoader with the system paths.
        """
        paths = SystemPaths()
        self.data_path = paths.data_path

    def load_data(self,file_name: str) -> List[Dict]:
        """
        Load data from the data source.
        """
        data = []
        file_path = os.path.join(self.data_path, file_name)
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data