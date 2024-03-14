from src.apps.users.permissions import IsCECUser, IsRegionUser
from src.apps.inventory.services.crud import annual_norm_crud
from src.apps.inventory.schemas import IdAnnualNormSchema
from src.apps.inventory.services.validator import AnnualNorm

permissions = [IsCECUser | IsRegionUser]
response = {204: None}


async def handler(request, payload: IdAnnualNormSchema):
    """
    # Description

    **This endpoint deletes a Annual Norm with the provided ID.**

    **Roles:**
    - `CEC User`: **Can delete only for Regions, not districts.**

    - `Region User`: **Can delete only for its own districts.**

    """
    instance = await annual_norm_crud.read(
        pk=payload.id, select_related=["product_norm__district", "product_norm__region"]
    )

    await AnnualNorm(request.user, instance.product_norm).validator()

    instance = await annual_norm_crud.delete(instance)

    return None
