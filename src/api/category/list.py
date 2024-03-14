from src.apps.inventory.services.crud import category_crud
from src.apps.inventory.schemas import CategoryDetailSchema
from src.apps.inventory.filters import CategoryFilter
from src.apps.core.filters import OrderFilter
from src.apps.users.permissions import UserPermission
from ninja import Query
from typing import List


permissions = [UserPermission]
response = List[CategoryDetailSchema]


async def handler(
    request,
    filters: CategoryFilter = Query(...),
    order_filter: OrderFilter = Query(...),
):
    """
    # Description

    **This endpoint gets a list of Categories based on the provided filters and ordering.**

    **Roles:**
    - `CEC User`
    - `Region User`
    - `District User`
    """
    ordering = order_filter.ordering
    filter_args = filters.get_filter_expression()
    qs = await category_crud.get_list(
        conditions=filter_args,
        ordering=ordering,
    )

    return qs
