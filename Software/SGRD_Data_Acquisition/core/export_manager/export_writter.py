import csv
import json
import os

class ExportWriter:
    def __init__(self, formatted_data, export_type="csv"):
        self.data = formatted_data
        self.type = export_type
        self.output_dir = "data"

        if not self.data:
            raise ValueError("Cannot write empty data.")

        os.makedirs(self.output_dir, exist_ok=True)
        self.filename = self._generate_filename()

    def _generate_filename(self):
        # Get indicator band names (everything except 'date' and 'region_id')
        indicators = [k for k in self.data[0].keys() if k not in ("date", "region_id")]
        indicator_str = "_".join(indicators)

        # Get region_id if present
        region_id = self.data[0].get("region_id", "region")

        # Get date range
        dates = [row["date"] for row in self.data if "date" in row]
        dates.sort()
        start_date = dates[0]
        end_date = dates[-1]

        # Build filename
        base_name = f"{indicator_str}_{region_id}_{start_date}_{end_date}.{self.type}"
        return os.path.join(self.output_dir, base_name)

    def save(self):
        if self.type == "csv":
            keys = self.data[0].keys()
            with open(self.filename, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.data)
        elif self.type == "geojson":
            with open(self.filename, "w") as f:
                json.dump(self.data, f, indent=2)
        else:
            raise ValueError("Unsupported export format")

        print(f"✅ Saved to: {self.filename}")
