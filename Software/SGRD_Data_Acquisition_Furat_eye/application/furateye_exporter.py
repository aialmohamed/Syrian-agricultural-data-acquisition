



from typing import List

import ee

from core.export_manager.export_dispatcher import ExportDispatcher
from core.export_manager.export_loader import ExportLoader
from core.export_manager.export_writter import ExportWriter


class FuratEyeExporter:
    def __init__(self, collection_to_Export : List[ee.ImageCollection], region_id: str, export_type: str, export_scale: int,asset_loader):
        """
        Initialize the FuratEyeExporter with the collection to export, region ID, export type, and scale.
        Args:
            collection_to_Export (List[ee.ImageCollection]): The collection to export.
            region_id (str): The ID of the region to export.
            export_type (str): The type of export (e.g., 'csv', 'json').
            export_scale (int): The scale for the export.
            asset_loader: The asset loader to use for exporting.
        """
        self.collection_to_Export = collection_to_Export
        self.region_id = region_id
        self.export_type = export_type
        self.export_scale = export_scale
        self.asset_loader = asset_loader
        self.geometry = self.asset_loader.load_feature_collection(self.region_id).geometry()
    def export(self):
        """
        Export the collection to the specified format.
        Returns:
            dict: A dictionary containing the export information.
        """
        if self.export_type == None:
            self.export_type = "csv"
        for collection in self.collection_to_Export:
            export_loader = ExportLoader(data=collection,export_type= self.export_type,export_region=self.geometry, export_scale=self.export_scale, export_region_id=self.region_id)
            payload = export_loader.load()
            dispatcher = ExportDispatcher(payload)
            formatted_data = dispatcher.dispatch()
            writer = ExportWriter(formatted_data)
            writer.save()
            
