from src.apps.dictionary.services.validator import patch_delete_validator
from src.apps.users.permissions import IsDistrictUser
from src.apps.dictionary.services.crud import storage_place_crud
from src.apps.dictionary.schemas import (
    StoragePlaceDetailSchema,
    StoragePlacePatchSchema,
)

permissions = [IsDistrictUser]
response = StoragePlaceDetailSchema


async def handler(request, payload: StoragePlacePatchSchema):
    """
    # Description

    **This endpoint updates a Storage Place based on the provided ID and payload.**

    **Roles:**
    - `District User`: <big>**Can update a Storage Place if the Storage Place is in the same district as the user.**</big>

    """
    instance = await storage_place_crud.read(pk=payload.id)
    await patch_delete_validator(request, instance)
    instance = await storage_place_crud.update(
        instance, payload.dict(exclude_unset=True)
    )
    instance = await storage_place_crud.read(
        pk=instance.id, select_related=["building_category", "district__region"]
    )

    return instance
