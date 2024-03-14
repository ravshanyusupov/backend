from typing import List
from ninja import Query
from src.apps.dictionary.schemas.building_category import BuildingCategorySchema
from src.apps.dictionary.services.crud import building_category_crud
from src.apps.dictionary.filters import BuildingCategoryFilter
from src.apps.core.filters import OrderFilter
from src.apps.users.permissions import UserPermission

permissions = [UserPermission]
response = List[BuildingCategorySchema]


async def handler(
    request,
    filters: BuildingCategoryFilter = Query(...),
    order_filter: OrderFilter = Query(...),
):
    """
    # Description

    **This endpoint gets a list of Building Categories based on the provided filters and ordering.**

    **Roles:**
    - `CEC User`
    - `Region User`
    - `District User`

    """
    ordering = order_filter.ordering
    filter_args = filters.get_filter_expression()
    qs = await building_category_crud.get_list(
        conditions=filter_args, ordering=ordering
    )
    return qs
