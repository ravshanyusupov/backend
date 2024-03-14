from src.apps.dictionary.services.crud import building_category_crud
from src.apps.dictionary.schemas.building_category import (
    CreateBuildingCategorySchema,
    BuildingCategorySchema,
)
from src.apps.users.permissions import IsCECUser

permissions = [IsCECUser]
response = {201: BuildingCategorySchema}


async def handler(request, payload: CreateBuildingCategorySchema):
    """
    # Description

    **This endpoint creates a new Building Category with the provided payload.**

    **Roles:**
    - `CEC User`

    """
    instance = await building_category_crud.create(payload.dict())
    return 201, instance
