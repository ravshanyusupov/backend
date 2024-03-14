from src.apps.users.permissions import IsCECUser, IsRegionUser
from src.apps.inventory.schemas import IdProductNormSchema
from src.apps.inventory.services.crud import product_norm_crud
from src.apps.inventory.services.validator import ProductNormDelete

permissions = [IsCECUser | IsRegionUser]
response = {204: None}


async def handler(request, payload: IdProductNormSchema):
    """
    # Description

    **This endpoint deletes a Product Standard with the provided ID.**

    **Roles:**
    - `CEC User`: **Can delete only for Regions, not districts.**
    
    - `Region User`: **Can delete only for its own districts.**

    """
    instance = await product_norm_crud.read(payload.id, ["district"])
    await ProductNormDelete(request.user, instance).validator()
    await product_norm_crud.delete(instance)

    return None
