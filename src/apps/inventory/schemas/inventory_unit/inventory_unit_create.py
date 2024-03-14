from ninja import Schema, Field
from typing import Optional


class CreateInventoryUnitSchema(Schema):
    product_id: int
    storage_place_id: int
    commissioning_year: int = Field(..., gt=0, le=32767)
    inventory_number: str = Field(..., max_length=50)
