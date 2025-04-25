


from pathlib import Path
import sys


sys.path.append(str(Path(__file__).resolve().parent.parent))
from application import FurateyeCollectionLoader,FuratEyeStartup



def main():
    base = FuratEyeStartup()
    base.setup_core_and_connect_api()
    available_satellites = base.load_available_satellites()
    available_regions = base.load_available_regions()
    region_model = base.region_model
    
    print("Available Satellites:", available_satellites)
    print("Available Regions:", available_regions)
    print("Region Model:",type(region_model))
    region_id = base.region_ids[17]
    satellite_id = base.satellite_ids[1]
    sat_model = base.create_satellite_model(satellite_id)
    print("Region ID:", region_id)
    print("Satellite ID:", satellite_id)

    loader = FurateyeCollectionLoader(region_id=region_id,satellite_id=satellite_id,region_model=region_model,satellite_model=sat_model)
    collection = loader.load_raw_collection("2020-01-01", "2022-12-31")
    collection = loader.apply_cloud_masks_and_scale_to_collection()
    print(collection.size().getInfo())

    


if __name__ == "__main__":
    main()