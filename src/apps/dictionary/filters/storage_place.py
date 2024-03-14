from typing import Optional

from src.apps.users.models import User
from ninja import FilterSchema


class StoragePlaceFilter(FilterSchema):
    district_id: Optional[int] = None
    district__region_id: Optional[int] = None
    building_category_id: Optional[int] = None
    address__icontains: Optional[str] = None
