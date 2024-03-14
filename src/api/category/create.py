from src.apps.users.permissions import IsCECUser
from src.apps.inventory.schemas import CategoryCreateSchema, CategoryDetailSchema
from src.apps.inventory.services.crud import category_crud

permissions = [IsCECUser]
response = {201: CategoryDetailSchema}


async def handler(request, payload: CategoryCreateSchema):
    """
    # Description

    **This endpoint creates a new category with the provided payload.**

    **Roles:**
    - `CEC User`

    """
    instance = await category_crud.create(payload.dict())

    return 201, instance
