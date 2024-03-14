from src.apps.dictionary.schemas.district import (
    IdDistrictSchema,
    DistrictDetailSchema,
)
from src.apps.dictionary.services.crud import district_crud
from src.apps.users.permissions import UserPermission

permissions = [UserPermission]
response = {200: DistrictDetailSchema}


async def handler(request, payload: IdDistrictSchema):
    """
    # Description

    **This endpoint gets a district with the provided ID and its associated region.**

    **Roles:**
    - `CEC User`
    - `Region User`
    - `District User`

    """
    instance = await district_crud.read(payload.id, select_related=["region"])
    return 200, instance
