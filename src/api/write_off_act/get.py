from src.apps.inventory.schemas import (
    IdWriteOffActSchema,
    WriteOffActSchema,
)
from src.apps.inventory.services.crud import write_off_act_crud
from src.apps.inventory.services.validator import check_get_access_of_write_off_act
from src.apps.users.permissions import UserPermission

from django.db.models import Prefetch


permissions = [UserPermission]
response = {200: WriteOffActSchema}


async def handler(request, payload: IdWriteOffActSchema):
    """
    # Description

    **This endpoint gets a single Write-Off Act based on the provided ID and in response shows the Write-Off Act.**

    **Roles:**
    - `CEC User`: **Can get a Write-Off Act of any regions, and districts.**
    - `Region User`: **Can get a Write-Off Act of its own districts, and itself.**
    - `District User`: **Can get a Write-Off Act of its own only.**

    """
    prefetch = Prefetch("inventory_unit_for_write_off_act")
    instance = await write_off_act_crud.read(
        payload.id,
        select_related=["region", "district"],
        prefetch_related=[prefetch],
    )

    await check_get_access_of_write_off_act(request.user, instance)
    return 200, instance
