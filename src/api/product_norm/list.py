from src.apps.users.permissions import UserPermission
from src.apps.inventory.schemas import ProductNormDetailSchema
from src.apps.inventory.filters import ProductNormFilter
from src.apps.core.filters import OrderFilter
from src.apps.inventory.services.crud import product_norm_crud
from src.apps.users.models import User
from ninja_lib.paginator import paginate_response
from ninja import Query
from django.db.models import Q

permissions = [UserPermission]


async def handler(
    request,
    filters: ProductNormFilter = Query(...),
    order_filter: OrderFilter = Query(...),
    page: int = 1,
    size: int = 10,
):
    """
    # Description

    **This endpoint gets a paginated list of Product Standards based on the provided filters and ordering parameters.**

    **Roles:**
    - `CEC User`: **Can get the list of Product Standards. Can filter by all fields.**

    - `Region User`: **Can get the list of Product Standards of its own districts, and region. Can filter by product, and district.**

    - `District User`: **Can get the list of Product Standards of its district own. Can filter by product.**

    """
    ordering = order_filter.ordering
    # filter_args = filters.dict(exclude_unset=True)

    filter_conditions = {
        User.REGION: Q(region_id=request.user.region_id),
        User.DISTRICT: Q(district_id=request.user.district_id),
    }
    filter_args = filter_conditions.get(request.user.user_type, Q())
    filter_args &= filters.get_filter_expression()
    qs = await product_norm_crud.get_queryset(
        conditions=filter_args,
        select_related=["product__category", "region", "district"],
        prefetch_related=["annual_norm_for_product_norm"],
    )

    return await paginate_response(qs, ProductNormDetailSchema, page, size, ordering)
