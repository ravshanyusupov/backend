from src.apps.dictionary.schemas.building_category import (
    BuildingCategoryPatchSchema,
    BuildingCategorySchema,
)
from src.apps.dictionary.services.crud import building_category_crud
from src.apps.users.permissions import IsCECUser
from ninja.errors import ValidationError


permissions = [IsCECUser]
response = {200: BuildingCategorySchema}


async def handler(request, payload: BuildingCategoryPatchSchema):
    """
    # Description

    **This endpoint updates a Building Category with the provided ID and payload.**

    **Roles:**
    - `CEC User`

    """
    instance_id = payload.id
    building_category = await building_category_crud.read(instance_id)
    updated_instance = await building_category_crud.update(
        building_category, payload.dict(exclude_unset=True)
    )
    return 200, updated_instance
