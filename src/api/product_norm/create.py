from src.apps.users.permissions import IsCECUser, IsRegionUser
from src.apps.inventory.schemas import ProductNormCreateSchema, ProductNormDetailSchema
from src.apps.inventory.services.validator import ProductNormCreate
from src.apps.inventory.services.crud import product_norm_crud, annual_norm_crud

permissions = [IsCECUser | IsRegionUser]
response = {201: ProductNormDetailSchema}


async def handler(request, payload: ProductNormCreateSchema):
    """
    # Description

    **This endpoint creates a new Product Standard and it's Annual Standard with the provided payload.
    The created Product Standard includes the product, it's category, region, district, annual standards.**

    **Roles:**
    - `CEC User`: **Can create only for Region, not districts.**

    - `Region User`: **Can create only for its own districts.**

    """
    await ProductNormCreate(request.user, payload).validator()
    payload_dict = payload.dict(exclude_unset=True)
    annual_norms = payload_dict.pop("annual_norms", None)

    product_norm_instance = await product_norm_crud.create(payload_dict)

    for annual_norm in annual_norms:
        annual_norm["product_norm_id"] = product_norm_instance.id
        annual_norm_instance = await annual_norm_crud.create(annual_norm)

    instance = await product_norm_crud.read(
        pk=product_norm_instance.id,
        select_related=["product__category", "district", "region"],
        prefetch_related=["annual_norm_for_product_norm"],
    )
    return instance
