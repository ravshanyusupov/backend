from src.apps.dictionary.schemas.building_category import (
    IdBuildingCategorySchema,
    BuildingCategorySchema,
)
from src.apps.dictionary.services.crud import building_category_crud
from src.apps.users.permissions import UserPermission

permissions = [UserPermission]
response = {200: BuildingCategorySchema}


async def handler(request, payload: IdBuildingCategorySchema):
    """
    # Description

    **This endpoint gets a Building Category with the provided ID.**

    **Roles:**
    - `CEC User`
    - `Region User`
    - `District User`

    """
    instance = await building_category_crud.read(payload.id)
    return 200, instance
