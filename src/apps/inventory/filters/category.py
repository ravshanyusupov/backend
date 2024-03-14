from ninja import FilterSchema, Field
from typing import Optional


class CategoryFilter(FilterSchema):
    search: Optional[str] = Field(
        None,
        q=[
            "name_uz__icontains",
            "name_ru__icontains",
        ],
    )
