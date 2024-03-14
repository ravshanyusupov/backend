from typing import Optional

from ninja import FilterSchema


class InventoryUnitFilter(FilterSchema):
    product_id: Optional[int] = None
    storage_place_id: Optional[int] = None
    inventory_number__icontains: Optional[str] = None
