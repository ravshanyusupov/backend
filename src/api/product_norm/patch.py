from src.apps.users.permissions import IsCECUser, IsRegionUser
from src.apps.inventory.schemas import ProductNormDetailSchema, ProductNormPatchSchema
from src.apps.inventory.services.crud import product_norm_crud
from src.apps.inventory.services.validator import ProductNormPatch

permissions = [IsRegionUser | IsCECUser]
response = ProductNormDetailSchema


async def handler(request, payload: ProductNormPatchSchema):
    """
    # Description

    **This endpoint updates a Product Standard with the provided ID and payload.
    The access to update the Product Standards is determined by the user's role.**

    **Roles:**
    - `CEC User`: **Can update any Product Standards of any regions, NOT District.**

    - `Region User`: **Can update Product Standards only for its own Districts.**

    """
    instance = await product_norm_crud.read(payload.id, ["district"])

    await ProductNormPatch(request.user, instance, payload).validator()

    instance = await product_norm_crud.update(
        instance, payload.dict(exclude_unset=True)
    )
    instance = await product_norm_crud.read(
        pk=instance.id,
        select_related=["product__category", "region", "district"],
        prefetch_related=["annual_norm_for_product_norm"],
    )

    return instance
