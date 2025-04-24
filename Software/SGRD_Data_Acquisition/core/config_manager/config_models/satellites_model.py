from dataclasses import dataclass, field
from typing import Optional, Dict


@dataclass
class BandSet:
    red: Optional[str] = None
    nir: Optional[str] = None
    cloud_mask: Optional[str] = None
    saturation_mask: Optional[str] = None
    ndvi: Optional[str] = None
    evi: Optional[str] = None


@dataclass
class ScaleFactor:
    multiplier: float
    offset: float


@dataclass
class ScaleFactors:
    optical: Optional[ScaleFactor] = None
    thermal: Optional[ScaleFactor] = None


@dataclass
class SatelliteInfo:
    name: str
    dataset_id: str
    sensor: Optional[str] = None
    bands: BandSet = field(default_factory=BandSet)
    scale_factors: Optional[ScaleFactors] = None
    scale_factor: Optional[float] = None
    resolution: Optional[int] = None
