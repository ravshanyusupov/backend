from ninja import FilterSchema
from typing import Optional


class ProductNormFilter(FilterSchema):
    product_id: Optional[int] = None
    region_id: Optional[int] = None
    district_id: Optional[int] = None
