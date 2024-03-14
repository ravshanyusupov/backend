from src.apps.dictionary.services.validator.storage_place import patch_delete_validator
from src.apps.dictionary.schemas import IdStoragePlaceSchema
from src.apps.users.permissions import IsDistrictUser
from src.apps.dictionary.services.crud import storage_place_crud

permissions = [IsDistrictUser]

response = {204: None}


async def handler(request, payload: IdStoragePlaceSchema):
    """
    # Description

    **This endpoint deletes a Storage Place based on the provided ID.**

    **Roles:**
    - `District User`: <big>**Can delete a Storage Place if the Storage Place is in the same district as the user.**</big>

    """
    instance = await storage_place_crud.read(pk=payload.id)
    await patch_delete_validator(request, instance)
    await storage_place_crud.delete(instance)
    return 204, None
