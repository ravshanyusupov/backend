from ninja_lib.error import DomainException
from src.apps.inventory.models import InventoryUnit, WriteOffAct
from src.apps.inventory.services.crud import inventory_unit_crud
from typing import List
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()


async def check_inventory_numbers_access(user: User, inventory_number_list: List[str]):
    qs = await inventory_unit_crud.get_queryset(
        conditions=Q(inventory_number__in=inventory_number_list)
    )

    if not await qs.aexists():
        raise DomainException(4012)

    async for inventory_unit in qs:
        if not inventory_unit.district_id == user.district_id:
            raise DomainException(4003)
    return qs


async def check_get_access_of_write_off_act(user, instance):
    USER_TYPES = {
        User.REGION: {user.region_id: instance.region_id},
        User.DISTRICT: {user.district_id: instance.district_id},
    }
    for key, value in USER_TYPES.get(user.user_type, {}).items():
        if key != value:
            raise DomainException(4002)


async def check_status_of_write_off_act(user, instance):
    USER_TYPES = {
        User.REGION: {user.region_id: instance.region_id},
        User.CEC: {},
    }
    for key, value in USER_TYPES.get(user.user_type).items():
        if key != value:
            raise DomainException(4004)

    if (
        instance.status == WriteOffAct.REJECTED
        or instance.status == WriteOffAct.APPROVED
    ):
        raise DomainException(4005)
