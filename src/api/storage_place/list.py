from src.apps.users.permissions import UserPermission
from src.apps.dictionary.services.crud import storage_place_crud
from src.apps.dictionary.schemas import (
    PaginatedStoragePlaceSchema,
    StoragePlaceDetailSchema,
)
from src.apps.dictionary.filters import StoragePlaceFilter
from src.apps.core.filters import OrderFilter
from src.apps.users.models import User
from ninja_lib.paginator import paginate_response

from django.db.models import Q
from ninja import Query


permissions = [UserPermission]
response = PaginatedStoragePlaceSchema


async def handler(
    request,
    filters: StoragePlaceFilter = Query(...),
    order_filter: OrderFilter = Query(...),
    page: int = 1,
    size: int = 10,
):
    """
    # Description

    **This endpoint gets a paginated list of Storage Places based on the provided filters, and ordering.**

    **Roles:**
    - `CEC User`: **Can get the list of Storage Places of any regions, and districts. Can use all filters**

    - `Region User`: **Can get the list of Storage Places of its own districts. Can filter by district, building category and address**

    - `District User`: **Can get the list of Storage Places of its own district only. Can filter by building category and address**

    """
    ordering = order_filter.ordering

    filter_conditions = {
        User.REGION: Q(district__region_id=request.user.region_id),
        User.DISTRICT: Q(district_id=request.user.district_id),
    }

    filter_args = filter_conditions.get(request.user.user_type, Q())
    filter_args &= filters.get_filter_expression()
    qs = await storage_place_crud.get_queryset(conditions=filter_args)

    return await paginate_response(qs, StoragePlaceDetailSchema, page, size, ordering)
