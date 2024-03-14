from src.apps.inventory.models import InventoryUnit
from src.apps.dictionary.models import StoragePlace
from ninja_lib.error import DomainException

from django.contrib.auth import get_user_model


User = get_user_model()


async def check_district_of_instance(user, instance):
    if not user.district_id == instance.district_id:
        raise DomainException(4000)


async def check_get_access_of_instance(user, instance):
    USER_TYPES = {
        User.REGION: {user.region_id: instance.district.region_id},
        User.DISTRICT: {user.district_id: instance.district_id},
    }
    for key, value in USER_TYPES.get(user.user_type, {}).items():
        if key != value:
            raise DomainException(4002)
