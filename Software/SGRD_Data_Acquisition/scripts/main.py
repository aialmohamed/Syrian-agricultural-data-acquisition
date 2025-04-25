import sys
from pathlib import Path
import ee
import matplotlib.pyplot as plt
import pandas as pd







# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.collection_manager.collection_filtering import CollectionFiltering
from core.config_manager.config_models import ProjectInfo, SatelliteInfo, RegionAssets, ConfigModel, universal_factory
from core.config_manager import ConfigLoader, ConfigDispatcher
from core.api_manager import ApiConnecter , ApiGeeLoader
from core.assets_manager.assets_region_loader import AssetsRegionLoader
from core.indicator_manager.indicator_factory import IndicatorFactory
from core.timeseries_manager import TimeSeriesLoader, TimeSeriesDispatcher

def main():
    cfg = ConfigLoader()
    dispatcher = ConfigDispatcher(cfg)
    project_info = dispatcher.get_project_settings()
    project_model = universal_factory.from_config({"project": project_info})
    satellite_info = dispatcher.get_satellite_settings()
    landsat = universal_factory.from_config({"satellites": satellite_info["LANDSAT_8"]})
    modsi = universal_factory.from_config({"satellites": satellite_info["MODIS"]})
    region_info = dispatcher.get_region_settings()
    region_model = universal_factory.from_config({"parent": region_info})
    api_connecter = ApiConnecter(project_model)
    api_connecter.authenticate_and_Initialize()
    api_connecter.check_engine_status()

    loader = AssetsRegionLoader(region_model)
    region_ids = list(region_model.regions.keys())
   # print("Region IDs:", region_ids)
    geom = loader.load_geometry(region_ids[7])
   # print(geom.getInfo())

    loader = ApiGeeLoader("2020-01-01", "2022-12-31", region_model, landsat)


    collection = loader.build_collection(region_ids[7])
    print("Collection:", collection.size().getInfo())

    filtered_collection = CollectionFiltering(collection, landsat).apply()
    print("Filtered Collection Size:", filtered_collection.size().getInfo())


    loader_modis = ApiGeeLoader("2020-01-01", "2020-12-31", region_model, modsi)


    collection_modis = loader_modis.build_collection(region_ids[7])
    info = collection_modis.getInfo()
    print("Collection keys:", info.keys())
    print("Number of images:", len(info["features"]))
    print("First image properties:", info["features"][1]["properties"])
    filtered_collection_modis = CollectionFiltering(collection_modis, modsi).apply()
    info = filtered_collection_modis.getInfo()
    print("Collection keys:", info.keys())
    print("Number of images:", len(info["features"]))
    print("First image properties:", info["features"][1]["properties"])
    print("Filtered Collection MODIS Size:", filtered_collection_modis.size().getInfo())

    ## applay sacling 
    scaled_collection_landsat = CollectionFiltering(filtered_collection, landsat).apply_scaling()
    print("Scaled Collection Size:", scaled_collection_landsat.size().getInfo())

    indicator = IndicatorFactory.create("NDVI_LANDSAT_8", scaled_collection_landsat)
    ndvi_result = indicator.compute()
    print("NDVI Result Size:", ndvi_result.size().getInfo())
    reduced = indicator.reduce(geom,512)
    print("Reduced NDVI Result Size:", reduced.size().getInfo())
    scaled_collection_modis = CollectionFiltering(filtered_collection_modis, modsi).apply_scaling()


    indicator_modis = IndicatorFactory.create("NDVI_MODIS", scaled_collection_modis)
    ndvi_result_modis = indicator_modis.compute()
    composite_modis = indicator.composite(method="mosaic")
    print("NDVI Result MODIS Size:", ndvi_result_modis.size().getInfo())
    reduced_modis = indicator_modis.reduce(geom, 512)
    print("Reduced NDVI Result MODIS Size:", reduced_modis.size().getInfo())
    print("Composite MODIS Size:", composite_modis.getInfo())

    # create time series
    time_series_landsat = TimeSeriesLoader(ndvi_result)
    time_series_landsat_sorted_and_filtered = time_series_landsat.filter_and_sort_by_year(2020)
    print("Time Series Landsat Size:", time_series_landsat_sorted_and_filtered.size().getInfo())

    timeseries_dispatcher = TimeSeriesDispatcher(time_series_landsat_sorted_and_filtered)
    timeseries_monthly = timeseries_dispatcher.dispatch("monthly")
    print("Time Series Monthly Size:", timeseries_monthly.size().getInfo())
    timeseries_seasonal = timeseries_dispatcher.dispatch("seasonal")
    print("Time Series Seasonal Size:", timeseries_seasonal.size().getInfo())
    timeseries_anomaly = timeseries_dispatcher.dispatch("anomaly",threshold=2.0)
    print("Time Series Anomaly Size:", timeseries_anomaly.size().getInfo())
    img = timeseries_anomaly.first()
    print(img.bandNames().getInfo())


    ## create data over two years :
    time_series_landsat_2years = TimeSeriesLoader(ndvi_result)
    time_series_landsat_sorted_and_filtered_2years = time_series_landsat_2years.filter_and_sorted_by_date("2020-01-01", "2021-12-31")
    print("Time Series Landsat 2 Years Size:", time_series_landsat_sorted_and_filtered_2years.size().getInfo())
    timeseries_dispatcher_2years = TimeSeriesDispatcher(time_series_landsat_sorted_and_filtered_2years)
    timeseries_monthly_2years = timeseries_dispatcher_2years.dispatch("yearly")
    print("Time Series Monthly 2 Years Size:", timeseries_monthly_2years.size().getInfo())




    #print("All Configurations:", configurations_path.all())
if __name__ == "__main__":
    main()