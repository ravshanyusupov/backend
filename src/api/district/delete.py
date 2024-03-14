from src.apps.dictionary.services.crud import district_crud
from src.apps.dictionary.schemas.district import IdDistrictSchema
from src.apps.users.permissions import IsCECUser

permissions = [IsCECUser]
response = {204: None}


async def handler(request, payload: IdDistrictSchema):
    """
    # Description

    **This endpoint deletes a district with the provided id.**

    **Roles:**
    - `CEC User`

    """
    instance = await district_crud.read(payload.id)
    await district_crud.delete(instance)
    return 204, None
