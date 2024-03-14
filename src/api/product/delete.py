from src.apps.users.permissions import IsCECUser
from src.apps.inventory.schemas import IdProductSchema
from src.apps.inventory.services.crud import product_crud

permissions = [IsCECUser]
response = {204: None}


async def handler(request, payload: IdProductSchema):
    """
    # Description

    **This endpoint deletes a Product with the provided ID.**

    **Roles:**
    - `CEC User`

    """
    instance = await product_crud.read(payload.id)
    await product_crud.delete(instance)

    return None
