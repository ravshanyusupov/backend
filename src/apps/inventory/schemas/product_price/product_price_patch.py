from ninja import Schema
from typing import Optional


class ProductPricePatchSchema(Schema):
    id: int
    product_id: Optional[int] = None
    year_id: Optional[int] = None
    price: Optional[int] = None
