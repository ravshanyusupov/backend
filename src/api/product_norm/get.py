from src.apps.users.permissions import UserPermission
from src.apps.inventory.services.validator import ProductNormRead
from src.apps.inventory.schemas import ProductNormDetailSchema, IdProductNormSchema
from src.apps.inventory.services.crud import product_norm_crud

permissions = [UserPermission]
response = ProductNormDetailSchema


async def handler(request, payload: IdProductNormSchema):
    """
    # Description

    **This endpoint gets a single Product Standard with the provided ID.**

    **Roles:**
    - `CEC User`: **Can get the single product standard of any regions, and districts.**

    - `Region User`: **Can get the single product standard of its own districts, and its own region.**

    - `District User`: **Can get the single product standard of its own only.**

    """
    instance = await product_norm_crud.read(
        pk=payload.id,
        select_related=["product__category", "region", "district"],
        prefetch_related=["annual_norm_for_product_norm"],
    )
    await ProductNormRead(request.user, instance).validator()
    return instance
