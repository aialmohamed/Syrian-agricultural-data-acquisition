

from io import BytesIO
import os
import ee
import requests
from core.map_image_manager import map_image_data_loader
from PIL import Image, ImageDraw, ImageFont

class MapImageCreator:
    def __init__(self, map_loader: map_image_data_loader):
        self.map_loader = map_loader
    def create_map_image(self):
        """
        Creates a map image using the MapImageDataLoader.
        """
        #sector_geometry = self._load_sector_geometry_from_subsector(self.map_loader.region_name)
        #print(f"Sector Geometry: {sector_geometry.getInfo()}")
        colorizedVis = {
                    'min': 0,
                    'max': 1,
                    'palette': [
                        'ffffff', 'ce7e45', 'df923d', 'f1b555', 'fcd163', '99b718', '74a901',
                        '66a000', '529400', '3e8601', '207401', '056201', '004c00', '023b01',
                        '012e01', '011d01', '011301'
                    ],
                };
        collection= self.map_loader.load_map_image()
        count = collection.size().getInfo()
        for i in range(count):
            current_image = ee.Image(collection.get(i))
            timestamp = current_image.get('system:time_start')
            date_label = ee.Date(timestamp).format('YYYY-MM-dd').getInfo()
            current_image_clipped = current_image.clip(self.map_loader.region_geometry)
            url = current_image_clipped.visualize(**self.map_loader.visualization_params).getThumbUrl({
                'region': self.map_loader.region_geometry,
                'dimensions': 512,
                'format': 'png',
            })
            response = requests.get(url)
            if response.status_code == 200:
                current_image_data = Image.open(BytesIO(response.content)).convert("RGBA")

                # add Timestamp
                draw = ImageDraw.Draw(current_image_data)
                font = ImageFont.truetype(self.map_loader.arial, 20)
                draw.text((10, 10), date_label, font=font,fill= "Black")

                #save image :
                img_path = os.path.join(self.map_loader.output_folder, f"{self.map_loader.indicator_name}_{date_label}.png")
                current_image_data.save(img_path)
                print(f"Image saved at {img_path}")
            else:
                print(f"Failed to retrieve image for date {date_label}. Status code: {response.status_code}")

    def _load_sector_geometry_from_subsector(self, subsector_id: str) -> ee.Geometry:
        """
        Given a subsector ID, find the correct sector full name and load its geometry.
        Example:
            Input: 'SECTOR_2_SUB_8_SOUTH_MID'
            Matching Sector: 'SECTOR_2_MID'
        """
        parts = subsector_id.split('_')
        if len(parts) < 2:
            raise ValueError(f"❌ Invalid subsector ID format: {subsector_id}")
        
        sector_id_base = "_".join(parts[0:2])  # SECTOR_2

        # Search for matching full sector ID in assets
        matched_sector_id = None
        for region_key in self.map_loader.assets_loader._region_assets.regions.keys():
            if region_key.startswith(sector_id_base) and not '_SUB_' in region_key:
                matched_sector_id = region_key
                break

        if matched_sector_id is None:
            raise ValueError(f"❌ No matching sector found for base ID '{sector_id_base}' in assets.")

        return self.map_loader.assets_loader.load_geometry(matched_sector_id)
    def create_map_image_full(self):
        """
        Creates a full map image: RGB background + Indicator overlay inside subsector.
        """

        # Load sector geometry
        sector_geometry = self._load_sector_geometry_from_subsector(self.map_loader.region_name)

        sector_rgb_background = self._get_sector_rgb_basemap(sector_geometry)

        # Load collection
        collection = self.map_loader.load_map_image()
        count = collection.size().getInfo()

        for i in range(count):
            current_image = ee.Image(collection.get(i))
            timestamp = current_image.get('system:time_start')
            date_label = ee.Date(timestamp).format('YYYY-MM-dd').getInfo()

            # 2. Clip indicator image to sector
            current_image_clipped = current_image.clip(sector_geometry)

            # 3. Mask: Only show inside subsector
            mask = ee.Image.constant(1).clip(self.map_loader.region_geometry)
            current_image_masked = current_image_clipped.updateMask(mask)

            # 4. Visualization parameters for NDSI (indicator)
            if self.map_loader.visualization_params is None:
                self.map_loader.visualization_params = {
                    'min': -1,
                    'max': 1,
                    'palette': ['blue', 'white', 'green']
                }

            # 5. Visualize the indicator
            indicator_vis = current_image_masked.visualize(**self.map_loader.visualization_params)

            # 6. Blend RGB background and NDSI indicator
            final_image = sector_rgb_background.blend(indicator_vis)

            # 7. Create thumbnail URL
            url = final_image.getThumbUrl({
                'region': sector_geometry,
                'dimensions': 512,
                'format': 'png',
            })

            # 8. Download and add timestamp
            response = requests.get(url)
            if response.status_code == 200:
                current_image_data = Image.open(BytesIO(response.content)).convert("RGBA")

                # Add timestamp label
                draw = ImageDraw.Draw(current_image_data)
                font = ImageFont.truetype(self.map_loader.arial, 20)
                draw.text((10, 10), date_label, font=font, fill="white")

                # Save image
                img_path = os.path.join(self.map_loader.output_folder, f"{self.map_loader.indicator_name}_{date_label}.png")
                current_image_data.save(img_path)
                print(f"✅ Image saved at {img_path}")
            else:
                print(f"❌ Failed to retrieve image for date {date_label}. Status code: {response.status_code}")

    def _get_sector_rgb_basemap(self, sector_geometry):
        # Load Landsat 8 SR C2 Level 2 image collection
        l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
            .filterBounds(sector_geometry) \
            .filterDate('2019-01-01', '2021-01-01') \
            .filter(ee.Filter.lt('CLOUD_COVER', 20))  
        l8 = l8.map(self._apply_scale_factors)
        # Check if collection is not empty
        size = l8.size().getInfo()
        if size == 0:
            raise ValueError("❌ No Landsat 8 images found for the sector in the given time range.")

        # Median composite
        l8_median = l8.median()

        # Select RGB bands and clip
        rgb = l8_median.select(['SR_B4', 'SR_B3', 'SR_B2']).clip(sector_geometry)

        rgb_vis = rgb.visualize(min=0, max=0.3)  

        return rgb_vis
    def _apply_scale_factors(self,image):
        optical_bands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
        thermal_bands = image.select('ST_B.*').multiply(0.00341802).add(149.0)
        return image.addBands(optical_bands, None, True).addBands(
            thermal_bands, None, True
        )
    def generate_gif(self):
        """
        Generates a GIF from the saved images.
        """
        img_files = sorted(os.listdir(self.map_loader.output_folder))
        img_files = [os.path.join(self.map_loader.output_folder, f) for f in img_files if f.endswith('.png')]
        
        # Load images
        images = [Image.open(f) for f in img_files]

        # Save as GIF
        gif_path = os.path.join(self.map_loader.output_folder, 'animation.gif')
        images[0].save(gif_path, save_all=True, append_images=images[1:], duration=500, loop=0,disposal=2)
        print(f"✅ GIF saved at {gif_path}")