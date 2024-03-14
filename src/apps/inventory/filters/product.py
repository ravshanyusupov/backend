from ninja import FilterSchema, Field
from typing import Optional


class ProductFilter(FilterSchema):
    category_id: Optional[int] = None
    search: Optional[str] = Field(
        None,
        q=[
            "name_uz__icontains",
            "name_ru__icontains",
        ],
    )
