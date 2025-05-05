

from pathlib import Path
import sys

import ee
import matplotlib.pyplot as plt



sys.path.append(str(Path(__file__).resolve().parent.parent))

from application.furateye_simple_charting_loader import FurateyeSimpleChartingLoader


def main():
    files=["NDVI_SYRIA_EAST_AOI_2000-01-01_2022-01-01.csv"]
    chart_loader = FurateyeSimpleChartingLoader(files)
    
    data = chart_loader.load_data()
    #chart_loader.plot_and_interpolate(data)
    chart_loader.plot_indicators(data)


if __name__ == "__main__":
    main()