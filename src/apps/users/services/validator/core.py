from src.apps.users.models import User
from src.apps.dictionary.services.crud import district_crud
from django.core.exceptions import ValidationError
from ninja_lib.error import DomainException


async def cec_required_fields(payload):
    region_id = payload.region_id
    district_id = payload.district_id
    if region_id or district_id:
        raise DomainException(2000)


async def region_required_field(payload):
    region_id = payload.region_id
    district_id = payload.district_id

    if not region_id or district_id:
        raise DomainException(2000)


async def district_required_fields(payload):
    region_id = payload.region_id
    district_id = payload.district_id
    if not region_id or not district_id:
        raise DomainException(2000)
    await check_district_in_region(region_id, district_id)


async def check_district_in_region(region_id, district_id):
    district_instance = await district_crud.read(pk=district_id)
    if not (region_id == district_instance.region_id):
        raise DomainException(2001)


def check_allowed_user_types(user_type, payload_user_type):
    USER_TYPES_LEVELS = {User.CEC: 1, User.REGION: 2, User.DISTRICT: 3}

    if USER_TYPES_LEVELS[user_type] > USER_TYPES_LEVELS[payload_user_type]:
        raise DomainException(2002)


async def check_region_id(user, instance):
    if not (user.region_id == instance.region_id):
        raise DomainException(2003)


def check_district_id(user, district_id):
    if not (user.district_id == district_id):
        raise DomainException(2004)


async def check_cec_instance(user, instance):
    pass


async def check_region_instance(user, instance):
    if user.id != instance.id:
        await check_district_in_region(user.region_id, instance.district_id)


async def check_district_instance(user, instance):
    if not (user.id == instance.id):
        raise DomainException(2005)
