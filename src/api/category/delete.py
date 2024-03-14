from src.apps.users.permissions import IsCECUser
from src.apps.inventory.schemas import IdCategorySchema
from src.apps.inventory.services.crud import category_crud

permissions = [IsCECUser]
response = {204: None}


async def handler(request, payload: IdCategorySchema):
    """
    # Description

    **This endpoint deletes a category with the provided id.**

    **Roles:**
    - `CEC User`

    """
    instance = await category_crud.read(payload.id)
    await category_crud.delete(instance)

    return 204, None
