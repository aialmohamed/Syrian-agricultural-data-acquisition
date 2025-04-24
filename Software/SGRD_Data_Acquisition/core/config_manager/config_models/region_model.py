from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass(frozen=True)
class RegionInfo:
    crop_focus: Optional[str] = None
    resolution: Optional[str] = None

@dataclass(frozen=True)
class RegionAssets:
    parent: str
    regions: Dict[str, RegionInfo] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> "RegionAssets":
        if "parent" not in data:
            raise KeyError("Missing 'parent' key in region configuration.")
        if "regions" not in data:
            raise KeyError("Missing 'regions' key in region configuration.")

        parent = data["parent"]
        raw_regions = data["regions"]

        parsed_regions = {
            name: RegionInfo(**info) if isinstance(info, dict) else RegionInfo()
            for name, info in raw_regions.items()
        }

        return cls(parent=parent, regions=parsed_regions)
