from src.apps.users.permissions import UserPermission
from src.apps.inventory.schemas import IdCategorySchema, CategoryDetailSchema
from src.apps.inventory.services.crud import category_crud

permissions = [UserPermission]
response = CategoryDetailSchema


async def handler(request, payload: IdCategorySchema):
    """
    # Description

    **This endpoint gets a single Category with the provided id.**

    **Roles:**
    - `CEC User`
    - `Region User`
    - `District User`
    """
    instance = await category_crud.read(payload.id)

    return instance
