from src.apps.inventory.schemas import (
    InventoryUnitPatchSchema,
    InventoryUnitSchema,
)
from src.apps.inventory.services.crud import inventory_unit_crud
from src.apps.dictionary.services.crud import storage_place_crud
from src.apps.users.permissions import IsDistrictUser
from src.apps.inventory.services.validator import check_district_of_instance

from django.core.exceptions import ObjectDoesNotExist
from ninja_lib.error import DomainException


permissions = [IsDistrictUser]
response = {200: InventoryUnitSchema}


async def handler(request, payload: InventoryUnitPatchSchema):
    """
    # Description

    **This endpoint updates an Inventory Unit with the provided ID and payload.**

    **Roles:**
    - `District User`
    """
    instance_id = payload.id
    inventory_unit_instance = await inventory_unit_crud.read(instance_id)
    await check_district_of_instance(request.user, inventory_unit_instance)
    storage_place_id = payload.dict().get("storage_place_id")

    if storage_place_id:
        try:
            storage_place = await storage_place_crud.read(storage_place_id)
        except ObjectDoesNotExist:
            raise DomainException(4001)

        await check_district_of_instance(request.user, storage_place)
    updated_instance = await inventory_unit_crud.update(
        inventory_unit_instance, payload.dict(exclude_unset=True)
    )
    updated_instance = await inventory_unit_crud.read(
        updated_instance.id,
        select_related=["product__category", "storage_place", "district__region"],
    )
    return 200, updated_instance
