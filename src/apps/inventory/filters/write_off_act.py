from typing import List, Optional
from ninja import FilterSchema


class WriteOffActFilter(FilterSchema):
    district_id: Optional[int] = None
    region_id: Optional[int] = None
    status__in: Optional[List[str]] = None
