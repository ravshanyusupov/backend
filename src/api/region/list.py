from typing import List
from ninja import Query
from src.apps.dictionary.schemas.region import RegionSchema
from src.apps.dictionary.services.crud import region_crud
from src.apps.users.permissions import UserPermission
from src.apps.dictionary.filters import RegionFilter
from src.apps.core.filters import OrderFilter


permissions = [UserPermission]
response = List[RegionSchema]


async def handler(
    request, filters: RegionFilter = Query(...), order_filter: OrderFilter = Query(...)
):
    """
    # Description

    **This endpoint gets a list of Regions based on the provided filters and ordering parameters.**

    **Roles:**
    - `CEC User`

    - `Region User`

    - `District User`
    """
    filter_args = filters.get_filter_expression()
    ordering = order_filter.ordering
    qs = await region_crud.get_list(ordering=ordering, conditions=filter_args)
    return qs
