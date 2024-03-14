from ninja import Field, FilterSchema
from typing import Optional


class RegionFilter(FilterSchema):
    search: Optional[str] = Field(
        None,
        q=[
            "name_uz__icontains",
            "name_ru__icontains",
        ],
    )
