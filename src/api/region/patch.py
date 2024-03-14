from src.apps.dictionary.schemas.region import (
    RegionPatchSchema,
    RegionSchema,
)
from src.apps.dictionary.services.crud import region_crud
from src.apps.users.permissions import IsCECUser


permissions = [IsCECUser]
response = {200: RegionSchema}


async def handler(request, payload: RegionPatchSchema):
    """
    # Description

    **This endpoint updates a Region with the provided ID and payload.**

    **Roles:**
    - `CEC User`

    """
    instance_id = payload.id
    region_instance = await region_crud.read(instance_id)
    updated_instance = await region_crud.update(
        region_instance, payload.dict(exclude_unset=True)
    )
    return 200, updated_instance
