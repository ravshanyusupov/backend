from ninja_lib.error import DomainException
from src.apps.users.models import User


async def read_validator(request, instance):
    user = request.user
    user_type = user.user_type

    check_functions = {
        User.CEC: allow,
        User.REGION: check_storage_place_region_id_matches_the_user_region_id,
        User.DISTRICT: check_whether_users_district_matches_the_payload_district,
    }

    check_function = check_functions.get(user_type)

    await check_function(user, instance)


async def patch_delete_validator(request, instance):
    await check_whether_users_district_matches_the_payload_district(
        request.user, instance
    )


async def check_whether_users_district_matches_the_payload_district(user, payload):
    if not (user.district_id == payload.district_id):
        raise DomainException(3001)


async def check_storage_place_region_id_matches_the_user_region_id(user, instance):
    if not (user.region_id == instance.district.region_id):
        raise DomainException(3001)


async def allow(user, instance):
    pass
