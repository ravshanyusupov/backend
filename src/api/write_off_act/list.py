from typing import List
from ninja import Query
from src.apps.inventory.schemas import WriteOffActSchema
from src.apps.inventory.services.crud import write_off_act_crud
from src.apps.inventory.filters import WriteOffActFilter
from src.apps.core.filters import OrderFilter
from src.apps.users.permissions import UserPermission
from ninja_lib.paginator import paginate_response

from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django.db.models import Q

User = get_user_model()

permissions = [UserPermission]


async def handler(
    request,
    filters: WriteOffActFilter = Query(...),
    order_filter: OrderFilter = Query(...),
    page: int = 1,
    size: int = 10,
):
    """
    # Description

    **This endpoint gets a paginated list of Write-Off Acts based on the provided filters, and ordering.**

    **Roles:**
    - `CEC User`: **Can get the list of Write-Off Acts of any regions, and districts. Can use all filters**
    - `Region User`: **Can get the list of Write-Off Acts of its own districts. Can filter by district**
    - `District User`: **Can get the list of Write-Off Acts of its own only. Can filter by district**

    """
    ordering = order_filter.ordering
    filter_conditions = {
        User.REGION: Q(region_id=request.user.region_id),
        User.DISTRICT: Q(district_id=request.user.district_id),
    }
    filter_args = filter_conditions.get(request.user.user_type, Q())
    filter_args &= filters.get_filter_expression()
    prefetch = Prefetch("inventory_unit_for_write_off_act")
    qs = await write_off_act_crud.get_queryset(
        select_related=["region", "district"],
        prefetch_related=[prefetch],
        conditions=filter_args,
    )
    return await paginate_response(qs, WriteOffActSchema, page, size, ordering)
