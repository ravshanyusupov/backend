from src.apps.users.permissions import IsCECUser
from src.apps.dictionary.services.crud import year_crud
from src.apps.dictionary.schemas import YearPatchSchema, YearDetailSchema

permissions = [IsCECUser]
response = YearDetailSchema


async def handler(request, payload: YearPatchSchema):
    """
    # Description

    **This endpoint updates a Year with the provided ID and payload.**

    **Roles:**
    - `CEC User`

    """
    instance = await year_crud.read(pk=payload.id)

    instance = await year_crud.update(instance, payload.dict(exclude_unset=True))

    return instance
