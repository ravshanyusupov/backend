from ninja import UploadedFile, Form, File
from src.apps.inventory.services.validator import check_inventory_numbers_access
from src.apps.inventory.services.crud import write_off_act_crud, inventory_unit_crud
from src.apps.inventory.schemas import (
    CreateWriteOffActSchema,
    WriteOffActSchema,
)
from src.apps.users.permissions import IsDistrictUser
from django.db.models import Prefetch


permissions = [IsDistrictUser]
response = {201: WriteOffActSchema}


async def handler(
    request,
    payload: CreateWriteOffActSchema = Form(...),
    file: UploadedFile = File(...),
):
    """
    # Description

    **This endpoint creates a Write-Off Act with the provided data and file, and in response shows the created Write-Off Act.**

    **Roles:**
    - `District User`

    """
    data = payload.dict()
    inventory_numbers = data.pop("inventory_numbers")
    inventory_queryset = await check_inventory_numbers_access(
        request.user, inventory_numbers
    )
    data.update(
        {
            "file": file,
            "district_id": request.user.district_id,
            "region_id": request.user.region_id,
        }
    )
    instance = await write_off_act_crud.create(data)

    async for inventory_unit in inventory_queryset:
        await inventory_unit_crud.update(inventory_unit, {"write_off_act": instance})
    prefetch = Prefetch("inventory_unit_for_write_off_act")
    instance = await write_off_act_crud.read(
        instance.id, select_related=["region", "district"], prefetch_related=[prefetch]
    )
    return 201, instance
