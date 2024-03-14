from django.contrib.auth import get_user_model

from src.apps.statistics.schemas.dashboard import UserOut
from src.apps.users.permissions import UserPermission
from src.apps.statistics.models import StatisticData


User = get_user_model()
permissions = [UserPermission]

response = UserOut


async def handler(request):
    """
    # Description

    **This endpoint provides data for Dashboard in JSON Format.
    The access to generate report is determined by the user's role.**

    **Roles:**
    - `CEC User`: **Can get data for all regions.**

    - `Region User`: **Can get data for only its own districts.**

    - `District User`: **Can get data for its own.**

    """

    response_conditions = {
        User.CEC: (lambda: StatisticData.objects.aget(name="Dashboard_data_for_CEC"), "cec_user"),
        User.REGION: (lambda: StatisticData.objects.aget(name=f"Dashboard_data_for_region_{request.user.region_id}"), "region_user"),
        User.DISTRICT: (lambda: StatisticData.objects.aget(name=f"Dashboard_data_for_district_{request.user.district_id}"), "district_user"),
    }

    data_function, response_key = response_conditions.get(request.user.user_type)

    try:
        data = (await data_function()).data
    except StatisticData.DoesNotExist:
        data = {}

    return {response_key: data}
