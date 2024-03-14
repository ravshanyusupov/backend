from typing import List
from ninja import Query
from ninja_lib.paginator import paginate_response
from src.apps.inventory.schemas import InventoryUnitSchema
from src.apps.inventory.services.crud import inventory_unit_crud
from src.apps.inventory.filters import InventoryUnitFilter
from src.apps.core.filters import OrderFilter
from src.apps.users.permissions import UserPermission

from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()

permissions = [UserPermission]


async def handler(
    request,
    filters: InventoryUnitFilter = Query(...),
    order_filter: OrderFilter = Query(...),
    page: int = 1,
    size: int = 10,
):
    """
    # Description

    **This endpoint gets a paginated list of visible Inventory Units based on the provided filters and ordering parameters.
    The access to get the Inventory Units is determined by the user's role.**

    **Roles:**
    - `CEC User`: **Can get any visible Inventory Units.**

    - `Region User`: **Can get visible Inventory Units only for its own districts.**

    - `District User`: **Can get visible Inventory Units only for its own.**

    """
    ordering = order_filter.ordering

    filter_conditions = {
        User.REGION: Q(district__region_id=request.user.region_id),
        User.DISTRICT: Q(district_id=request.user.district_id),
    }
    filter_args = filter_conditions.get(request.user.user_type, Q())
    filter_args &= Q(visible=True)
    filter_args &= filters.get_filter_expression()

    qs = await inventory_unit_crud.get_queryset(
        select_related=["product__category", "storage_place", "district__region"],
        conditions=filter_args,
    )
    return await paginate_response(qs, InventoryUnitSchema, page, size, ordering)
