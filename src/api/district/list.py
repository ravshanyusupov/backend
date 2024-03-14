from typing import List
from ninja import Query
from src.apps.dictionary.schemas.district import DistrictDetailSchema
from src.apps.dictionary.services.crud import district_crud
from src.apps.dictionary.filters import DistrictFilter
from src.apps.core.filters import OrderFilter
from src.apps.users.permissions import UserPermission

permissions = [UserPermission]
response = List[DistrictDetailSchema]


async def handler(
    request,
    filters: DistrictFilter = Query(...),
    order_filter: OrderFilter = Query(...),
):
    """
    # Description

    **This endpoint gets a list of districts based on the provided filters and ordering. Each district is included with its associated region.**

    **Roles:**
    - `CEC User`
    - `Region User`
    - `District User`

    """
    ordering = order_filter.ordering
    filter_args = filters.get_filter_expression()
    qs = await district_crud.get_list(
        select_related=["region"], conditions=filter_args, ordering=ordering
    )
    return qs
