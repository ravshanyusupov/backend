from src.apps.inventory.schemas import (
    IdWriteOffActSchema,
    WriteOffActSchema,
)
from src.apps.inventory.services.crud import write_off_act_crud
from src.apps.inventory.services.validator import check_status_of_write_off_act
from src.apps.users.permissions import IsRegionUser, IsCECUser
from src.apps.inventory.models import WriteOffAct

from django.db.models import Prefetch


permissions = [IsRegionUser | IsCECUser]
response = {200: WriteOffActSchema}


async def handler(request, payload: IdWriteOffActSchema):
    """
    # Description

    **This endpoint updates the status of a Write-Off Act to 'REJECTED' based on the provided ID and in response shows the updated Write-Off Act.**

    **Roles:**
    - `CEC User`
    - `Region User`

    """
    instance = await write_off_act_crud.read(payload.id)
    await check_status_of_write_off_act(request.user, instance)
    status = WriteOffAct.REJECTED
    payload = {"status": status}
    instance = await write_off_act_crud.update(instance, payload)
    prefetch = Prefetch("inventory_unit_for_write_off_act")
    instance = await write_off_act_crud.read(
        instance.id,
        select_related=["region", "district"],
        prefetch_related=[prefetch],
    )

    return 200, instance
