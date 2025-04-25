import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent))






from core.charting_manager.charting_data_loader import ChartingDataLoader
from core.charting_manager.charting_data_plotter import ChartingDataPlotter
from core.export_manager.export_writter import ExportWriter
from core.export_manager.export_dispatcher import ExportDispatcher
from core.export_manager.export_loader import ExportLoader
from core.timeseries_manager.timeseries_dispatcher import TimeSeriesDispatcher
from core.timeseries_manager.timeseries_loader import TimeSeriesLoader
from core.collection_manager.collection_filtering import CollectionFiltering
from core.indicator_manager.indicator_factory import IndicatorFactory
from core.api_manager.api_gee_loader import ApiGeeLoader
from core.assets_manager.assets_region_loader import AssetsRegionLoader
from core.api_manager.api_connecter import ApiConnecter
from core.config_manager.config_dispatcher import ConfigDispatcher
from core.config_manager.config_loader import ConfigLoader
from core.config_manager.config_models import universal_factory







def main():
    cfg = ConfigLoader()
    dispatcher = ConfigDispatcher(cfg)
    project_info = dispatcher.get_project_settings()
    project_model = universal_factory.from_config({"project": project_info})
    satellite_info = dispatcher.get_satellite_settings()
    landsat = universal_factory.from_config({"satellites": satellite_info["LANDSAT_8"]})
    region_info = dispatcher.get_region_settings()
    region_model = universal_factory.from_config({"parent": region_info})
    api_connecter = ApiConnecter(project_model)
    api_connecter.authenticate_and_Initialize()
    api_connecter.check_engine_status()
    loader = AssetsRegionLoader(region_model)
    region_ids = list(region_model.regions.keys())
    #print("Region IDs:", region_ids)
    #SECTOR_2_SUB_9_SOUTH_EAST ( Der ezzor city)
    der_ezzor = region_ids[17]
    fc = loader.load_feature_collection(der_ezzor)
    geom = fc.geometry()
    loader = ApiGeeLoader("2020-01-01", "2022-12-31", region_model, landsat)

    
    collection = loader.build_collection(der_ezzor)
    filtered_collection = CollectionFiltering(collection, landsat).apply()
    scaled_collection_landsat = CollectionFiltering(filtered_collection, landsat).apply_scaling()
    indicator_ndvi = IndicatorFactory.create("NDVI_LANDSAT_8", scaled_collection_landsat)
    indicator_ndsi = IndicatorFactory.create("NDSI_LANDSAT_8", scaled_collection_landsat)
    ndsi_result = indicator_ndsi.compute()
    ndvi_result = indicator_ndvi.compute()

    time_series_ndsi = TimeSeriesLoader(ndsi_result)
    time_series_ndsi_sorted_and_filtered = time_series_ndsi.filter_and_sort_by_year(2020)
    time_serires_dispatcher_ndsi = TimeSeriesDispatcher(time_series_ndsi_sorted_and_filtered)
    timeseries_monthly_ndsi = time_serires_dispatcher_ndsi.dispatch("monthly")

    time_series_ndvi = TimeSeriesLoader(ndvi_result)
    time_series_ndvi_sorted_and_filtered = time_series_ndvi.filter_and_sort_by_year(2020)
    time_serires_dispatcher_ndvi = TimeSeriesDispatcher(time_series_ndvi_sorted_and_filtered)
    timeseries_monthly_ndvi = time_serires_dispatcher_ndvi.dispatch("monthly")
    # Exporting the results
    export_loader_ndsi = ExportLoader(timeseries_monthly_ndsi, geom, export_type="csv", export_source=fc)
    payload_ndsi = export_loader_ndsi.load()

    dispatcher_ndsi = ExportDispatcher(payload_ndsi)
    formatted_data_ndsi = dispatcher_ndsi.dispatch()
    #writter_ndsi = ExportWriter(formatted_data_ndsi)
    #writter_ndsi.save()

    export_loader_ndvi = ExportLoader(timeseries_monthly_ndvi, geom, export_type="csv", export_source=fc)
    payload_ndvi = export_loader_ndvi.load()
    dispatcher_ndvi = ExportDispatcher(payload_ndvi)
    formatted_data_ndvi = dispatcher_ndvi.dispatch()
    #writter_ndvi = ExportWriter(formatted_data_ndvi)
    #writter_ndvi.save()

    # Plotting the results
    #charting_data_loader = ChartingDataLoader()
    #charting_data_ndsi = charting_data_loader.load_data("NDSI_SECTOR_2_SUB_9_SOUTH_EAST_2020-01-08_2020-12-09.csv")
    #charting_data_ndvi = charting_data_loader.load_data("NDVI_SECTOR_2_SUB_9_SOUTH_EAST_2020-01-08_2020-12-09.csv")
    #charting_data_plotter_ndsi = ChartingDataPlotter(charting_data_ndsi)
    #charting_data_plotter_ndvi = ChartingDataPlotter(charting_data_ndvi)

    #charting_data_plotter_ndsi.plot_indicators()
    #charting_data_plotter_ndvi.plot_indicators()
    # Load the data
    charting_data_loader = ChartingDataLoader()
    ndsi_data = charting_data_loader.load_data("NDSI_SECTOR_2_SUB_9_SOUTH_EAST_2020-01-08_2020-12-09.csv")
    ndvi_data = charting_data_loader.load_data("NDVI_SECTOR_2_SUB_9_SOUTH_EAST_2020-01-08_2020-12-09.csv")

    # Individual plots (if needed)
    #ChartingDataPlotter(ndsi_data).plot_indicators()
    #ChartingDataPlotter(ndvi_data).plot_indicators()

    # Combined plot
    ChartingDataPlotter.plot_combined_indicators(
        ndsi_data, ndvi_data,
        label1="NDSI",
        label2="NDVI",
        title="NDSI and NDVI Comparison over Time"
    )



if __name__ == "__main__":
    main()