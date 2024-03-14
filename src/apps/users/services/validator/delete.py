from src.apps.users.models import User
from src.apps.users.services.validator.core import (
    check_cec_instance,
    check_region_instance,
    check_district_instance,
)


async def delete_validator(user, instance):
    check_functions = {
        User.CEC: check_cec_instance,
        User.REGION: check_region_instance,
        User.DISTRICT: check_district_instance,
    }

    user_type = user.user_type
    check_function = check_functions.get(user_type)
    await check_function(user, instance)
