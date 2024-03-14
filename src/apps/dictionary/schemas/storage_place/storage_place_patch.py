from ninja import Schema
from typing import Optional


class StoragePlacePatchSchema(Schema):
    id: int
    building_category_id: Optional[int] = None
    address: Optional[str] = None
