from src.apps.dictionary.schemas.region import (
    IdRegionSchema,
    RegionSchema,
)
from src.apps.dictionary.services.crud import region_crud
from src.apps.users.permissions import UserPermission

permissions = [UserPermission]
response = {200: RegionSchema}


async def handler(request, payload: IdRegionSchema):
    """
    # Description

    **This endpoint gets a single Region with the provided ID.**

    **Roles:**
    - `CEC User`
    
    - `Region User`

    - `District User`

    """
    instance = await region_crud.read(payload.id)
    return 200, instance
