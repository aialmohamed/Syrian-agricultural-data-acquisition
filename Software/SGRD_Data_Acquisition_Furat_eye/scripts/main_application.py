


from pathlib import Path
import sys


sys.path.append(str(Path(__file__).resolve().parent.parent))
from application.furateye_startup import SgrdDataAcquisitionStartup


def main():
    base = SgrdDataAcquisitionStartup()
    base.setup_core_and_connect_api()
    available_satellites = base.load_available_satellites()
    available_regions = base.load_available_regions()
    print("Available Satellites:", available_satellites)
    print("Available Regions:", available_regions)


if __name__ == "__main__":
    main()