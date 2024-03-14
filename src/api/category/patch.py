from src.apps.users.permissions import IsCECUser
from src.apps.inventory.schemas import CategoryPatchSchema, CategoryDetailSchema
from src.apps.inventory.services.crud import category_crud

permissions = [IsCECUser]
response = CategoryDetailSchema


async def handler(request, payload: CategoryPatchSchema):
    """
    # Description

    **This endpoint updates a category with the provided ID and payload.**

    **Roles:**
    - `CEC User`

    """
    instance = await category_crud.read(payload.id)
    instance = await category_crud.update(instance, payload.dict(exclude_unset=True))

    return instance
