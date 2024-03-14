from src.apps.inventory.services.crud import annual_norm_crud, product_norm_crud
from src.apps.inventory.schemas import AnnualNormCreateSchema, AnnualNormDetailSchema
from src.apps.users.permissions import IsCECUser, IsRegionUser
from src.apps.inventory.services.validator import AnnualNorm
from typing import List
from django.db.models import Q

permissions = [IsCECUser | IsRegionUser]
response = {201: List[AnnualNormDetailSchema]}


async def handler(request, items: List[AnnualNormCreateSchema]):
    """
    # Description

    **This endpoint creates a new Annual Norm with the provided payload.**

    **Roles:**
    - `CEC User`: **Can create only for Region, not districts.**

    - `Region User`: **Can create only for its own districts.**

    """
    instance_ids = []
    for payload in items:
        product_norm_instance = await product_norm_crud.read(
            pk=payload.product_norm_id, select_related=["district"]
        )

        await AnnualNorm(request.user, product_norm_instance).validator()

        instance = await annual_norm_crud.create(payload.dict())
        instance_ids.append(instance.id)

    instances = await annual_norm_crud.get_list(conditions=Q(id__in=instance_ids))

    return instances
