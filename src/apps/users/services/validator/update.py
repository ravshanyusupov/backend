from src.apps.users.services.validator import payload_validator
from src.apps.users.services.validator.core import (
    check_cec_instance,
    check_region_instance,
    check_district_instance,
)
from src.apps.users.models import User


async def update_validator(request, payload, instance, payload_dict):
    check_functions = {
        User.CEC: check_cec_instance,
        User.REGION: check_region_instance,
        User.DISTRICT: check_district_instance,
    }

    user = request.user
    user_type = user.user_type

    if payload_dict.get("user_type"):
        await payload_validator(request, payload)

    check_function = check_functions.get(user_type)
    await check_function(user, instance)
