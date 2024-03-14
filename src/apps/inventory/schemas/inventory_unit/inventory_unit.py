from datetime import datetime
from typing import Optional
from ninja import Schema, ModelSchema
from src.apps.inventory.models import InventoryUnit
from src.apps.inventory.schemas import ProductDetailSchema
from src.apps.dictionary.schemas import StoragePlaceSchema, DistrictDetailSchema


class InventoryUnitSchema(Schema):
    id: int
    product: ProductDetailSchema
    storage_place: StoragePlaceSchema
    district: DistrictDetailSchema
    commissioning_year: int
    inventory_number: str
    created_at: datetime
    updated_at: datetime
