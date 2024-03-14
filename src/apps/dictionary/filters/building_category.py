from ninja import FilterSchema, Field
from typing import Optional


class BuildingCategoryFilter(FilterSchema):
    search: Optional[str] = Field(
        None,
        q=[
            "name_uz__icontains",
            "name_ru__icontains",
        ],
    )
