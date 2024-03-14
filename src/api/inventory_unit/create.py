from src.apps.inventory.services.crud import inventory_unit_crud
from src.apps.dictionary.services.crud import storage_place_crud
from src.apps.inventory.schemas import (
    CreateInventoryUnitSchema,
    InventoryUnitSchema,
)
from src.apps.users.permissions import IsDistrictUser
from src.apps.inventory.services.validator import check_district_of_instance
from django.core.exceptions import ObjectDoesNotExist
from ninja_lib.error import DomainException

permissions = [IsDistrictUser]
response = {201: InventoryUnitSchema}


async def handler(request, payload: CreateInventoryUnitSchema):
    """
    # Description

    **This endpoint creates a new Inventory Unit with the provided payload.**

    **Roles:**
    - `District User`
    """
    data = payload.dict()
    try:
        storage_place = await storage_place_crud.read(payload.storage_place_id)
    except ObjectDoesNotExist:
        raise DomainException(4001)
    await check_district_of_instance(request.user, storage_place)
    data.update({"district_id": request.user.district_id})
    instance = await inventory_unit_crud.create(data)
    instance = await inventory_unit_crud.read(
        instance.id,
        select_related=["product__category", "storage_place", "district__region"],
    )
    return 201, instance
