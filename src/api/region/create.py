from src.apps.dictionary.services.crud import region_crud
from src.apps.dictionary.schemas.region import (
    CreateRegionSchema,
    RegionSchema,
)
from src.apps.users.permissions import IsCECUser

permissions = [IsCECUser]
response = {201: RegionSchema}


async def handler(request, payload: CreateRegionSchema):
    """
    # Description

    **This endpoint creates a new Region with the provided payload.**

    **Roles:**
    - `CEC User`

    """
    instance = await region_crud.create(payload.dict())
    return 201, instance
