from src.apps.dictionary.services.crud import storage_place_crud
from src.apps.dictionary.services.validator import (
    check_whether_users_district_matches_the_payload_district,
)
from src.apps.dictionary.schemas import (
    CreateStoragePlaceSchema,
    StoragePlaceDetailSchema,
)
from src.apps.users.permissions import IsDistrictUser


permissions = [IsDistrictUser]
response = {201: StoragePlaceDetailSchema}


async def handler(request, payload: CreateStoragePlaceSchema):
    """
    # Description

    **This endpoint creates a new Storage Place with the provided payload.**

    **Roles:**
    - `District User`: <big>**Can create a new Storage Place if the user's district matches the district in the payload.**</big>

    """
    await check_whether_users_district_matches_the_payload_district(
        request.user, payload
    )
    instance = await storage_place_crud.create(payload.dict())
    instance = await storage_place_crud.read(
        pk=instance.pk, select_related=["building_category", "district__region"]
    )

    return instance
