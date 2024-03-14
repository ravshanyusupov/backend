from src.apps.users.permissions import IsCECUser
from src.apps.inventory.schemas import (
    ProductPriceCreateSchema,
    ProductPriceDetailSchema,
)
from src.apps.inventory.services.crud import product_price_crud
from typing import List
from django.db.models import Q


permissions = [IsCECUser]
response = {201: List[ProductPriceDetailSchema]}


async def handler(request, items: List[ProductPriceCreateSchema]):
    """
    # Description

    **This endpoint creates a new Product Price with the provided payload.**

    **Roles:**
    - `CEC User`

    """
    instance_ids = []
    for payload in items:
        instance = await product_price_crud.create(payload.dict())
        instance_ids.append(instance.id)

    instances = await product_price_crud.get_list(
        conditions=Q(id__in=instance_ids),
        select_related=["product__category", "year"],
    )

    return instances
