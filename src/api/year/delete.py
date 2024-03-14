from src.apps.users.permissions import IsCECUser
from src.apps.dictionary.services.crud import year_crud
from src.apps.dictionary.schemas import IdYearSchema

permissions = [IsCECUser]
response = {204: None}


async def handler(request, payload: IdYearSchema):
    """
    # Description

    **This endpoint deletes a Year with the provided ID.**

    **Roles:**
    - `CEC User`

    """
    instance = await year_crud.read(pk=payload.id)
    instance = await year_crud.delete(instance)

    return None
