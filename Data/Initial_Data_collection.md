# Data Collection process 


## Index
- [Data Collection process](#data-collection-process)
  - [Index](#index)
  - [Introduction](#introduction)
  - [Targeted data](#targeted-data)
  - [Targeted areas](#targeted-areas)
    - [Table of AOI , Sectors and Subsectors](#table-of-aoi--sectors-and-subsectors)
    - [Images from Google earth engine on the Areas](#images-from-google-earth-engine-on-the-areas)
      - [Area of interest (AOI)](#area-of-interest-aoi)
  - [Time series](#time-series)
  - [Methods](#methods)
  - [Data storing and visuals](#data-storing-and-visuals)
  - [Conclusion](#conclusion)
  - [Referencing and data sources](#referencing-and-data-sources)

## Introduction
In this section of the project we shall put the first steps into the data acquisition for the proposal .

All those data were taken by google earth engine using remote sensing from different satellites on different bandwidth .  


More (TBD)

## Targeted data 

- Vegetation (NDVI, SAVI, EVI…)

- Precipitation (total, anomalies, seasonal trends)

- Temperature (min, max, average, trends)

- Drought (indices like SPI, SPEI, NDWI)

- Salinity (soil salinity indicators via remote sensing or field)
- Evapotranspiration (ET) (Water loss via evaporation and plant transpiration.) ( Dataset: MOD16 (MODIS ET), WaPOR (FAO))
- Land Use / Land Cover Change (LULC) (Tracks crop areas, fallow land, desertification.) (Shows impact of conflict, migration, or farming shifts.)
- Soil Type / Soil Properties (Affects water retention, salinity sensitivity. Global datasets: HWSD, SoilGrids )
- (TBD)

## Targeted areas


> [!IMPORTANT]
> The area of interest (AOI) is currently only east of syria  this could expand later to all of the country

> [!IMPORTANT]
> The data for the polygons of those ares are under **/Data/Area_Data/** there are two files a .csv and a .geojson file



### Table of AOI , Sectors and Subsectors  

| Level        | Name                          | Description                        |
|--------------|-------------------------------|------------------------------------|
| AOI          | SYRIA_EAST_AOI                | Main area of interest              |
| Sector 1     | SECTOR_1_WEST_NORTH           | Western North                      |
|              | ├─ SECTOR_1_SUB_1_NORTH_WEST  | Subsector 1                        |
|              | ├─ SECTOR_1_SUB_2_NORTH_EAST  | Subsector 2                        |
|              | ├─ SECTOR_1_SUB_3_MID_WEST    | Subsector 3                        |
|              | ├─ SECTOR_1_SUB_4_MID_EAST    | Subsector 4                        |
|              | ├─ SECTOR_1_SUB_5_SOUTH_WEST  | Subsector 5                        |
|              | └─ SECTOR_1_SUB_6_SOUTH_EAST  | Subsector 6                        |
| Sector 2     | SECTOR_2_MID                  | Central zone                       |
|              | ├─ SECTOR_2_SUB_1_NORTH_WEST  | Subsector 1                        |
|              | ├─ SECTOR_2_SUB_2_NORTH_MID   | Subsector 2                        |
|              | ├─ SECTOR_2_SUB_3_NORTH_EAST  | Subsector 3                        |
|              | ├─ SECTOR_2_SUB_4_MID_WEST    | Subsector 4                        |
|              | ├─ SECTOR_2_SUB_5_MID_MID     | Subsector 5                        |
|              | ├─ SECTOR_2_SUB_6_MID_EAST    | Subsector 6                        |
|              | ├─ SECTOR_2_SUB_7_SOUTH_WEST  | Subsector 7                        |
|              | ├─ SECTOR_2_SUB_8_SOUTH_MID   | Subsector 8                        |
|              | └─ SECTOR_2_SUB_9_SOUTH_EAST  | Subsector 9                        |
| Sector 3     | SECTOR_3_EAST_NORTH           | Eastern North                      |
|              | ├─ SECTOR_3_SUB_1_SOUTH       | Subsector 1                        |
|              | ├─ SECTOR_3_SUB_2_MID         | Subsector 2                        |
|              | └─ SECTOR_3_SUB_3_NORTH       | Subsector 3                        |
| Sector 4     | SECTOR_4_EAST_SOUTH           | Eastern South                      |
|              | ├─ SECTOR_4_SUB_1_NORTH       | Subsector 1                        |
|              | ├─ SECTOR_4_SUB_2_MID         | Subsector 2                        |
|              | └─ SECTOR_4_SUB_3_SOUTH       | Subsector 3                        |


### Images from Google earth engine on the Areas 

#### Area of interest (AOI) 
 

## Time series

- year by year ( each year tack months)
- from 2000 to 2011 ( pre war )
- from 2012 to 2017 (rev start - migration crisis)
- from 2018 to 2024 ( after division to today)

## Methods

(TBD)

## Data storing and visuals 

(TBD)
## Conclusion
(TBD)
## Referencing and data sources
(TBD)