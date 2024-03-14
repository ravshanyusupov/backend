from src.apps.inventory.schemas import AnnualNormPatchSchema, AnnualNormDetailSchema
from src.apps.users.permissions import IsCECUser, IsRegionUser
from src.apps.inventory.services.crud import annual_norm_crud
from src.apps.inventory.services.validator import AnnualNorm

permissions = [IsCECUser | IsRegionUser]
response = AnnualNormDetailSchema


async def handler(request, payload: AnnualNormPatchSchema):
    """
    # Description

    **This endpoint updates a Annual Norm with the provided ID and payload.
    The access to update the Annual Norm is determined by the user's role.**

    **Roles:**
    - `CEC User`: **Can update any Annual Norms of Product Standards of any regions, NOT District.**

    - `Region User`: **Can update Annual Norms of Product Standards only for its own Districts.**

    """
    instance = await annual_norm_crud.read(
        pk=payload.id,
        select_related=["product_norm__region", "product_norm__district"],
    )

    await AnnualNorm(request.user, instance.product_norm).validator()

    instance = await annual_norm_crud.update(instance, payload.dict(exclude_unset=True))

    return instance
