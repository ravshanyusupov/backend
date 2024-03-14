from src.apps.users.permissions import IsCECUser
from src.apps.dictionary.services.crud import year_crud
from src.apps.dictionary.schemas import YearCreateSchema, YearDetailSchema

permissions = [IsCECUser]
response = {201: YearDetailSchema}


async def handler(request, payload: YearCreateSchema):
    """
    # Description

    **This endpoint creates a new 'Year' with the provided payload.**

    **Roles:**
    - `CEC User`: **Can create only for Region, not districts.**
    """
    instance = await year_crud.create(payload.dict())

    return instance
