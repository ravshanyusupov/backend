from src.apps.users.permissions import IsCECUser
from src.apps.inventory.schemas import IdProductPriceSchema
from src.apps.inventory.services.crud import product_price_crud

permissions = [IsCECUser]
response = {204: None}


async def handler(request, payload: IdProductPriceSchema):
    """
    # Description

    **This endpoint deletes a Product Price with the provided ID.**

    **Roles:**
    - `CEC User`

    """
    instance = await product_price_crud.read(payload.id)
    await product_price_crud.delete(instance)

    return None
