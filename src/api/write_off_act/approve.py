from src.apps.inventory.schemas import (
    IdWriteOffActSchema,
    WriteOffActSchema,
)
from src.apps.inventory.services.crud import write_off_act_crud, inventory_unit_crud
from src.apps.inventory.services.validator import check_status_of_write_off_act
from src.apps.users.permissions import IsRegionUser, IsCECUser
from src.apps.inventory.models import WriteOffAct

from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from asgiref.sync import sync_to_async


User = get_user_model()

permissions = [IsRegionUser | IsCECUser]
response = {200: WriteOffActSchema}


async def handler(request, payload: IdWriteOffActSchema):
    """
    # Description

    **This endpoint updates the status of a Write-Off Act based on the user's role and in response shows the updated Write-Off Act.**

    **Roles:**
    - `CEC User`: **Can update the status of a Write-Off Act to 'Approved'.**
    - `Region User`: **Can update the status of a Write-Off Act to 'Pending by CEC'.**

    """
    instance = await write_off_act_crud.read(payload.id)
    await check_status_of_write_off_act(request.user, instance)
    USER_TYPES = {User.CEC: WriteOffAct.APPROVED, User.REGION: WriteOffAct.PENDING_CEC}
    status = USER_TYPES.get(request.user.user_type)
    payload = {"status": status}
    instance = await write_off_act_crud.update(instance, payload)
    prefetch = Prefetch("inventory_unit_for_write_off_act")
    instance = await write_off_act_crud.read(
        instance.id,
        select_related=["region", "district"],
        prefetch_related=[prefetch],
    )
    await sync_to_async(
        inventory_unit_crud.Model.objects.filter(write_off_act=instance).update
    )(visible=False)
    return 200, instance
