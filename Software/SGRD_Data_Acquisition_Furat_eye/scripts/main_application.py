


from pathlib import Path
import sys

import ee
import matplotlib.pyplot as plt



sys.path.append(str(Path(__file__).resolve().parent.parent))
from application import FurateyeCollectionLoader,FuratEyeStartup, FurateyeIndicatorApplier, FurateyeTimeseriesLoader, FuratEyeExporter,FurateyeSimpleChartingLoader
from core.map_image_manager import MapImageDataLoader,MapImageCreator

def main():
    base = FuratEyeStartup()
    base.setup_core_and_connect_api()
    available_satellites = base.load_available_satellites()
    available_regions = base.load_available_regions()
    region_model = base.region_model
    assest_loader = base.asset_loader
    
    
    print("Available Satellites:", available_satellites)
    print("Available Regions:", available_regions)
    print("Region Model:",type(region_model))
    # REGION : SECTOR_2_SUB_9_SOUTH_EAST
    value =base.region_ids.index("SYRIA_EAST_AOI")
    region_id = base.region_ids[value]
    #LADNSAT_8
    satellite_id = base.satellite_ids[2]
    sat_model = base.create_satellite_model(satellite_id)
    
    print("Region ID:", region_id)
    print("Satellite ID:", satellite_id)

    loader = FurateyeCollectionLoader(region_id=region_id,satellite_id=satellite_id,region_model=region_model,satellite_model=sat_model)
    collection = loader.load_raw_collection("2000-03-26", "2023-01-01")
    collection = loader.apply_cloud_masks_and_scale_to_collection()
    print(collection.size().getInfo())

    # Apply indicators see core.indicator_manager.indicator_registry for the available indicators
    #indicator_types = ["NDVI_LANDSAT_8", "NDSI_LANDSAT_8","NDVI_MODIS", "PRECIPITATION_UCSB", "NDVI_LANDSAT_7"]
    indicator_types = ["NDVI_MODIS"]
    indicator = FurateyeIndicatorApplier(indicators_type=indicator_types, collection=collection)
    #indicator_collections = indicator.apply_indicator_and_reduce(assest_loader,region_id)
    indicator_collections  = indicator.apply_indicators()
    #print("Collections after applying indicators:")
    #print("Reduced mean dict:", reduced.getInfo())
    #print(indicator_collections[0].first().getInfo())
    #print(indicator_collections[1].first().getInfo())
    ## load timeseries
    start_date = "2000-03-26"
    end_date = "2023-01-01"
    time_series_loader = FurateyeTimeseriesLoader(indicator_collections)
    time_series_by_date = time_series_loader.create_timeseries_by_date(start_date, end_date)
    time_series_monthly_ndvi = time_series_loader.load_timeseries_as_years(time_series_by_date[0])
    #time_series_monthly_ndsi = time_series_loader.load_timeseries_as_years(time_series_by_date[1])
    #print(time_series_monthly_ndvi.first().getInfo())
    #print(time_series_monthly_ndsi.size().getInfo())

    # Export the data
    Exporter = FuratEyeExporter(collection_to_Export=[time_series_monthly_ndvi], region_id=region_id, export_type="csv",export_scale=255,asset_loader=assest_loader)
    Exporter.export()
    #files are under /data/Indicator_region_id_start_date_end_date.csv
    #
    #files=["precipitation_SECTOR_2_MID_2000-01-01_2024-01-01.csv"]
    #chart_loader = FurateyeSimpleChartingLoader(files)
    
    #data = chart_loader.load_data()
    #chart_loader.plot_and_interpolate(data)
    #chart_loader.plot_indicators(data)

    # imageloader :
    # ['#ffffe5','#f7fcb9','#d9f0a3','#addd8e','#78c679','#41ab5d','#238443','#006837','#004529']

    image_loader =  MapImageDataLoader(time_series_collection=time_series_monthly_ndvi,
                                       region_name=region_id,
                                       indicator_name="NDVI",
                                      start_date=start_date,
                                      end_date=end_date,
                                      color_pallet= [
                                        'ffffff', 'ce7e45', 'df923d', 'f1b555', 'fcd163', '99b718', '74a901',
                                        '66a000', '529400', '3e8601', '207401', '056201', '004c00', '023b01',
                                        '012e01', '011d01', '011301'
                                    ],
                                     assets_loader=assest_loader)
    
    image_loader._prepare_output_folder()
    image_creator = MapImageCreator(image_loader)
    image_creator.create_map_image()
    image_creator.generate_gif()

if __name__ == "__main__":
    main()