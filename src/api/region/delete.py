from src.apps.dictionary.services.crud import region_crud
from src.apps.dictionary.schemas.region import IdRegionSchema
from src.apps.users.permissions import IsCECUser

permissions = [IsCECUser]
response = {204: None}


async def handler(request, payload: IdRegionSchema):
    """
    # Description

    **This endpoint deletes a Region with the provided ID.**

    **Roles:**
    - `CEC User`

    """
    instance = await region_crud.read(payload.id)
    await region_crud.delete(instance)
    return 204, None
