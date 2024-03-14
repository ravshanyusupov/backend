from src.apps.users.permissions import UserPermission
from src.apps.dictionary.schemas import IdYearSchema, YearDetailSchema
from src.apps.dictionary.services.crud import year_crud

permissions = [UserPermission]
response = {200: YearDetailSchema}


async def handler(request, payload: IdYearSchema):
    """
    # Description

    **This endpoint gets a single Year with the provided ID.**

    **Roles:**
    - `CEC User`

    - `Region User`

    - `District User`

    """
    instance = await year_crud.read(pk=payload.id)

    return instance
