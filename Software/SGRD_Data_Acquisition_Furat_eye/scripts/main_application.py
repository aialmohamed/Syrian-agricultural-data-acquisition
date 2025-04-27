


from pathlib import Path
import sys



sys.path.append(str(Path(__file__).resolve().parent.parent))
from application import FurateyeCollectionLoader,FuratEyeStartup, FurateyeIndicatorApplier, FurateyeTimeseriesLoader, FuratEyeExporter,FurateyeSimpleChartingLoader
from core.map_image_manager.map_image_data_loader import MapImageDataLoader

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
    region_id = base.region_ids[17]
    #LADNSAT_8
    satellite_id = base.satellite_ids[0]
    sat_model = base.create_satellite_model(satellite_id)
    print("Region ID:", region_id)
    print("Satellite ID:", satellite_id)

    loader = FurateyeCollectionLoader(region_id=region_id,satellite_id=satellite_id,region_model=region_model,satellite_model=sat_model)
    collection = loader.load_raw_collection("2020-01-01", "2022-12-31")
    collection = loader.apply_cloud_masks_and_scale_to_collection()
    print(collection.size().getInfo())
    # Apply indicators see core.indicator_manager.indicator_registry for the available indicators
    indicator_types = ["NDVI_LANDSAT_8", "NDSI_LANDSAT_8"]
    indicator = FurateyeIndicatorApplier(indicators_type=indicator_types, collection=collection)
    indicator_collections = indicator.apply_indicators()
    print("Collections after applying indicators:")
    #print(indicator_collections[0].first().getInfo())
    #print(indicator_collections[1].first().getInfo())
    ## load timeseries
    start_date = "2020-01-01"
    end_date = "2021-12-31"
    time_series_loader = FurateyeTimeseriesLoader(indicator_collections)
    time_series_by_date = time_series_loader.create_timeseries_by_date(start_date, end_date)
    time_series_monthly_ndvi = time_series_loader.load_timeseries_as_months(time_series_by_date[0])
    time_series_monthly_ndsi = time_series_loader.load_timeseries_as_months(time_series_by_date[1])
    print(time_series_monthly_ndvi.size().getInfo())
    print(time_series_monthly_ndsi.size().getInfo())

    # Export the data
    Exporter = FuratEyeExporter(collection_to_Export=[time_series_monthly_ndvi, time_series_monthly_ndsi], region_id=region_id, export_type="csv",export_scale=255,asset_loader=assest_loader)
    #Exporter.export()
    #files are under /data/Indicator_region_id_start_date_end_date.csv
    #
    #files=["NDVI_SYRIA_2020-01-01_2020-12-02.csv","NDSI_SYRIA_2020-01-01_2020-12-02.csv"]
    #chart_loader = FurateyeSimpleChartingLoader(files)
    
    #data = chart_loader.load_data()
    #chart_loader.plot_and_interpolate(data)
    #chart_loader.plot_indicators(data)

    # imageloader :
    image_loader =  MapImageDataLoader(time_series_collection=time_series_monthly_ndsi,
                                       region_name=region_id,
                                       indicator_name="NDSI",
                                       start_date=start_date,
                                       end_date=end_date,
                                       visualization_params=None)
    #image_loader._prepare_output_folder()
if __name__ == "__main__":
    main()