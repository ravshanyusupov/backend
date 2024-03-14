from ninja import Schema, Field
from typing import Optional
from src.apps.core.schemas import BaseSchema


class CreateRegionSchema(BaseSchema):
    precincts_count: int = Field(0, gt=0, le=32767)
