from ninja import Schema
from typing import Optional
from src.apps.core.schemas import BasePatchSchema


class ProductPatchSchema(BasePatchSchema):
    category_id: Optional[int] = None
