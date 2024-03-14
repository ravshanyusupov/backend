from ninja import Schema, Field
from typing import Optional


class InventoryUnitPatchSchema(Schema):
    id: int
    product_id: Optional[int] = None
    storage_place_id: Optional[int] = None
    write_off_act_id: Optional[int] = None
    commissioning_year: Optional[int] = None
    inventory_number: str = Field(None, max_length=50)
