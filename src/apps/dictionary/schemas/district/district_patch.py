from typing import Optional

from src.apps.core.schemas import BasePatchSchema


class DistrictPatchSchema(BasePatchSchema):
    region_id: Optional[int] = None
