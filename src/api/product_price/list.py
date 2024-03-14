from src.apps.users.permissions import UserPermission
from src.apps.inventory.schemas import ProductPriceDetailSchema
from src.apps.inventory.services.crud import product_price_crud
from src.apps.inventory.filters import ProductPriceFilter
from src.apps.core.filters import OrderFilter
from ninja import Query
from typing import List


permissions = [UserPermission]
response = List[ProductPriceDetailSchema]


async def handler(
    request,
    filters: ProductPriceFilter = Query(...),
    order_filter: OrderFilter = Query(...),
):
    """
    # Description

    **This endpoint gets a list of Product Prices based on the provided filters and ordering parameters.**

    **Roles:**
    - `CEC User`

    - `Region User`

    - `District User`

    """
    ordering = order_filter.ordering
    filter_args = filters.get_filter_expression()
    qs = await product_price_crud.get_list(
        ordering=ordering,
        conditions=filter_args,
        select_related=["product__category", "year"],
    )

    return qs
