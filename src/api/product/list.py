from src.apps.users.permissions import UserPermission
from src.apps.inventory.schemas import PaginatedProductSchema, ProductDetailSchema
from src.apps.inventory.services.crud import product_crud
from src.apps.inventory.filters import ProductFilter
from src.apps.core.filters import OrderFilter
from ninja_lib.paginator import paginate_response
from ninja import Query


permissions = [UserPermission]
response = PaginatedProductSchema


async def handler(
    request,
    filters: ProductFilter = Query(...),
    order_filter: OrderFilter = Query(...),
    page: int = 1,
    size: int = 10,
):
    """
    # Description

    **This endpoint gets a paginated list of Products based on the provided filters and ordering parameters.**

    **Roles:**
    - `CEC User`

    - `Region User`

    - `District User`

    """
    ordering = order_filter.ordering
    filter_args = filters.get_filter_expression()
    qs = await product_crud.get_queryset(
        conditions=filter_args, select_related=["category"]
    )
    return await paginate_response(qs, ProductDetailSchema, page, size, ordering)
