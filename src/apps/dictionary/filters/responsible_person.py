from typing import Optional

from ninja import FilterSchema


class ResponsiblePersonFilter(FilterSchema):
    district_id: Optional[int] = None
    region_id: Optional[int] = None
