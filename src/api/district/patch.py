from src.apps.dictionary.schemas.district import (
    DistrictPatchSchema,
    DistrictDetailSchema,
)
from src.apps.dictionary.services.crud import district_crud
from src.apps.users.permissions import IsCECUser


permissions = [IsCECUser]
response = {200: DistrictDetailSchema}


async def handler(request, payload: DistrictPatchSchema):
    """
    # Description

    **This endpoint updates a district with the provided id and payload, and in response shows the updated district with its associated region.**

    **Roles:**
    - `CEC User`

    """
    instance_id = payload.id
    district_instance = await district_crud.read(instance_id)
    updated_instance = await district_crud.update(
        district_instance, payload.dict(exclude_unset=True)
    )
    updated_instance = await district_crud.read(
        district_instance.id, select_related=["region"]
    )
    return 200, updated_instance
