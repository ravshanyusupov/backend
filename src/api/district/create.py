from src.apps.dictionary.services.crud import district_crud
from src.apps.dictionary.schemas.district import (
    CreateDistrictSchema,
    DistrictDetailSchema,
)
from src.apps.users.permissions import IsCECUser

permissions = [IsCECUser]
response = {201: DistrictDetailSchema}


async def handler(request, payload: CreateDistrictSchema):
    """
    # Description

    **This endpoint creates a new district with the provided payload and in response shows the created district with its associated region.**

    **Roles:**
    - `CEC User`

    """
    instance = await district_crud.create(payload.dict())
    instance = await district_crud.read(instance.id, select_related=["region"])
    return 201, instance
