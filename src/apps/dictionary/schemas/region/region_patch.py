from ninja import Schema, Field
from typing import Optional
from src.apps.core.schemas import BasePatchSchema


class RegionPatchSchema(BasePatchSchema):
    precincts_count: Optional[int] = Field(None, gt=0, le=32767)
