from ninja_lib.error.exceptions import DomainException

from src.apps.users.models import User
from src.apps.users.services.validator.core import (
    cec_required_fields,
    region_required_field,
    district_required_fields,
    check_allowed_user_types,
    check_region_id,
    check_district_id,
)


async def payload_validator(request, payload):
    user = request.user
    user_type = user.user_type

    check_functions = {
        User.CEC: cec_check_payload,
        User.REGION: region_check_payload,
        User.DISTRICT: district_check_payload,
    }

    check_function = check_functions.get(user_type)

    await check_function(user, payload)


async def cec_check_payload(user, payload):
    user_type = payload.user_type

    check_functions = {
        User.CEC: cec_required_fields,
        User.REGION: region_required_field,
        User.DISTRICT: district_required_fields,
    }

    check_function = check_functions.get(user_type)
    await check_function(payload)


async def region_check_payload(user, payload):
    user_type = user.user_type
    payload_user_type = payload.user_type

    check_allowed_user_types(user_type, payload_user_type)

    check_functions = {
        User.DISTRICT: district_required_fields,
        User.REGION: region_required_field,
    }

    check_function = check_functions.get(payload_user_type)

    await check_function(payload)
    await check_region_id(user, payload)


async def district_check_payload(user, payload):
    user_type = user.user_type
    payload_user_type = payload.user_type

    check_allowed_user_types(user_type, payload_user_type)
    await check_region_id(user, payload)
    check_district_id(user, payload.district_id)


def validate_password(cls, password):
    error_codes = []
    special_chars = "@$!%*?&#^()[]{}<>.-_+|=:;,/"

    if len(password) < 8:
        error_codes.append(2007)
    if not any(char.isdigit() for char in password):
        error_codes.append(2008)
    if not any(char.islower() for char in password):
        error_codes.append(2009)
    if not any(char.isupper() for char in password):
        error_codes.append(2010)
    if not any(char in special_chars for char in password):
        error_codes.append(2011)

    if error_codes:
        raise DomainException(*error_codes)
    return password
