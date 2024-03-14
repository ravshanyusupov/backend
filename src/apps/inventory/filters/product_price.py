from ninja import FilterSchema
from typing import Optional


class ProductPriceFilter(FilterSchema):
    product_id: Optional[int] = None
