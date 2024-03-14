from src.apps.dictionary.services.crud import building_category_crud
from src.apps.dictionary.schemas.building_category import IdBuildingCategorySchema
from src.apps.users.permissions import IsCECUser

permissions = [IsCECUser]
response = {204: None}


async def handler(request, payload: IdBuildingCategorySchema):
    """
    # Description

    **This endpoint deletes a Building Category with the provided ID.**

    **Roles:**
    - `CEC User`

    """
    instance = await building_category_crud.read(payload.id)
    await building_category_crud.delete(instance)
    return 204, None
