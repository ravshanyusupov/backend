from src.apps.users.permissions import UserPermission
from src.apps.dictionary.schemas import IdStoragePlaceSchema, StoragePlaceDetailSchema
from src.apps.dictionary.services.crud import storage_place_crud
from src.apps.dictionary.services.validator import read_validator


permissions = [UserPermission]
response = {200: StoragePlaceDetailSchema}


async def handler(request, payload: IdStoragePlaceSchema):
    """
    # Description

    **This endpoint gets a single Storage Place based on the provided ID.**

    **Roles:**
    - `CEC User`: **Can get the Storage Place of any regions, and districts.**
    
    - `Region User`: **Can get the Storage Place of its own districts.**

    - `District User`: **Can get the Storage Place of its own district only.**

    """
    instance = await storage_place_crud.read(
        pk=payload.id, select_related=["building_category", "district__region"]
    )
    await read_validator(request, instance)
    return 200, instance
