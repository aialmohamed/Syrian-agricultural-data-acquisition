

from core.export_manager.export_formatters import ExportGeoJSONFormatter ,ExportCSVFormatter



class ExportDispatcher:
    """
    The ExportDispatcher class is responsible for managing the export process.
    It handles the export of data to various formats and destinations.
    """

    def __init__(self, export_payload:dict):
        """
        Initialize the ExportDispatcher with the export payload.

        Args:
            export_payload (dict): The payload containing export parameters.
        """
        self.payload = export_payload

    def dispatch(self):
        export_type = self.payload.get("type")
        if export_type == "csv":
            formatter = ExportCSVFormatter(self.payload)
        elif export_type == "geojson":
            raise NotImplementedError("GeoJSON export is not implemented yet.")
        elif export_type == "database":
            raise NotImplementedError("Database export is not implemented yet.")
        else:
            raise ValueError(f"Unknown export type: {export_type}")
        return formatter.format()