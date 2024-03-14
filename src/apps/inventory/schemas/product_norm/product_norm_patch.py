from ninja import Schema
from typing import Optional


class ProductNormPatchSchema(Schema):
    id: int
    product_id: Optional[int] = None
    region_id: Optional[int] = None
    district_id: Optional[int] = None
