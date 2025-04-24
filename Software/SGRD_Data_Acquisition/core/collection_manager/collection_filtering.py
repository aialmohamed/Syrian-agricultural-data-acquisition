import ee

from core.config_manager.config_models.satellites_model import SatelliteInfo


class CollectionFiltering:
    def __init__ (self,raw_collection :ee.ImageCollection,satellite_model: SatelliteInfo):
        self._collection = raw_collection
        self._model = satellite_model
    
    def apply(self) -> ee.ImageCollection:
        """
        Apply relevant filters like cloud/shadow masks based on the satellite sensor.
        """
        sensor = self._model.sensor
        if "MODIS" in sensor:
            return self._apply_modis_filters()
        elif "OLI/TIRS" in sensor or "LANDSAT" in sensor:
            return self._apply_landsat_filters()
        else:
            print(f"⚠️ No masking rules defined for sensor: {sensor}")
            return self._collection  # Return as-is
    
    def _apply_landsat_filters(self) -> ee.ImageCollection:
        """
        Apply cloud and shadow masking for Landsat 8 and 9.
        """
        bands = self._model.bands
        cloud_band  = bands["cloud_mask"]
        saturation_band  = bands.get("saturation_mask")

        def mask_landsat(img) -> ee.ImageCollection:
            """
            Apply cloud and saturation masking to Landsat images.
            """
            qa = img.select(cloud_band)
            # Mask: bits 0 (Fill), 1 (Dilated Cloud),2 (Cirrus), 3 (Cloud), 4 (Shadow)
            bits_to_mask = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4)
            cloud_shadow_mask = qa.bitwiseAnd(bits_to_mask).eq(0)
            if saturation_band:
                sat_mask = img.select(saturation_band).eq(0)
                combined_mask = cloud_shadow_mask.And(sat_mask)
            else:
                combined_mask = cloud_shadow_mask
            return img.updateMask(combined_mask)
        return self._collection.map(mask_landsat)
    def _apply_modis_filters(self) -> ee.ImageCollection:
        """
        Apply QA-based filtering for MODIS using SummaryQA.
        Keeps only pixels with SummaryQA == 0 (best quality).
        """
        qa_band = self._model.bands.get("qa", "SummaryQA")

        def mask_modis(image):
            qa = image.select(qa_band)
            good_quality_mask = qa.eq(0)
            return image.updateMask(good_quality_mask)

        return self._collection.map(mask_modis)
    def apply_scaling(self) -> ee.ImageCollection:
        sensor = self._model.sensor
        if "MODIS" in sensor:
            return self._apply_modis_scaling()
        elif "OLI/TIRS" in sensor or "LANDSAT" in sensor:
            return self._apply_landsat_scaling()
        return self._collection
    
    def _apply_landsat_scaling(self) -> ee.ImageCollection:
        """
        Apply scaling factors for Landsat 8
        """
        factors = self._model.scale_factors
        optical = factors["optical"]
        thermal = factors.get("thermal")
        def scale_image(img):
            opt_bands  = img.select("SR_B.").multiply(optical["multiplier"]).add(optical["offset"])
            if thermal:
                thermal_bands = img.select("ST_B.*").multiply(thermal["multiplier"]).add(thermal["offset"])
                return img.addBands(opt_bands, overwrite=True).addBands(thermal_bands, overwrite=True)
            return img.addBands(opt_bands, overwrite=True)
        return self._collection.map(scale_image)
    def _apply_modis_scaling(self) -> ee.ImageCollection:
        scale = self._model.scale_factor

        def scale_ndvi(img):
            return img.select("NDVI").multiply(scale).rename("NDVI") \
                    .set("system:time_start", img.get("system:time_start"))

        return self._collection.map(scale_ndvi)