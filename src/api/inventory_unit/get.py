from src.apps.inventory.schemas import (
    IdInventoryUnitSchema,
    InventoryUnitSchema,
)
from src.apps.inventory.services.crud import inventory_unit_crud
from src.apps.inventory.services.validator import check_get_access_of_instance
from src.apps.users.permissions import UserPermission


permissions = [UserPermission]
response = {200: InventoryUnitSchema}


async def handler(request, payload: IdInventoryUnitSchema):
    """
    # Description

    **This endpoint gets a single Inventory Unit with the provided ID. 
    The access to get the Inventory Unit is determined by the user's role.**

    **Roles:**
    - `CEC User`: **Can get any visible Inventory Unit.**
    
    - `Region User`: **Can get Inventory Unit only for its own districts.**

    - `District User`: **Can get Inventory Unit for its own.**

    """
    instance = await inventory_unit_crud.read(
        payload.id,
        select_related=["product__category", "storage_place", "district__region"],
    )
    await check_get_access_of_instance(request.user, instance)
    return 200, instance
