from ninja_lib.paginator import paginate_response
from src.apps.users.schemas import PaginatedUserSchema, UserSchema
from src.apps.users.permissions import UserPermission
from src.apps.users.services.crud import user_crud
from src.apps.users.models import User
from src.apps.users.filters import UserFilter
from src.apps.core.filters import OrderFilter
from ninja import Query
from django.db.models import Q


response = PaginatedUserSchema
permissions = [UserPermission]


async def handler(
    request,
    filters: UserFilter = Query(...),
    order_filter: OrderFilter = Query(...),
    page: int = 1,
    size: int = 10,
):
    """
    # Description

    **This endpoint retrieves a paginated list of Users based on the provided filters, ordering, page number, and page size.**

    **Roles:**
    - `CEC User`: **Can get the list of Users of any role. Can use all filters.**

    - `Region User`: **Can get the list of Users with the same Region as the current user and for it's own districts. Can filter by Username, Roles (Region role and District role) and District.**

    - `District User`: **Can get the list of Users with the same District as the current user. Can filter by username.**

    """
    ordering = order_filter.ordering

    filter_conditions = {
        User.REGION: Q(region_id=request.user.region_id),
        User.DISTRICT: Q(district_id=request.user.district_id),
    }
    filter_args = filter_conditions.get(request.user.user_type, Q())
    filter_args &= filters.get_filter_expression()

    qs = await user_crud.get_queryset(
        conditions=filter_args, select_related=["region", "district"]
    )

    return await paginate_response(qs, UserSchema, page, size, ordering)
