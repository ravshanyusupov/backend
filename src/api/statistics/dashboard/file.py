from django.contrib.auth import get_user_model

from src.apps.users.permissions import UserPermission
from src.apps.statistics.excels.dashboard import (
    CECUserReport,
    RegionUserReport,
    DistrictUserReport,
)
from src.apps.statistics.models import StatisticData


User = get_user_model()
permissions = [UserPermission]


async def handler(request):
    """
    # Description

    **This endpoint generates Excel Report for Dashboard.
    The access to generate report is determined by the user's role.**

    **Roles:**
    - `CEC User`: **Can get report for all regions at once.**

    - `Region User`: **Can get data for all its own districts at once.**

    - `District User`: **Can get data for its own.**

    """

    response_conditions = {
        User.CEC: (CECUserReport, "Respublika", lambda: StatisticData.objects.aget(name="Dashboard_data_for_CEC")),
        User.REGION: (RegionUserReport, "Viloyat", lambda: StatisticData.objects.aget(name=f"Dashboard_data_for_region_{request.user.region_id}")),
        User.DISTRICT: (DistrictUserReport, "Tuman-Shahar", lambda: StatisticData.objects.aget(name=f"Dashboard_data_for_district_{request.user.district_id}")),
    }

    report_class, report_name, data_fetcher = response_conditions.get(request.user.user_type)
    try:
        data = (await data_fetcher()).data
    except StatisticData.DoesNotExist:
        data = {}

    report = report_class(data)
    report.generate_report()
    response = report.get_http_response(report_name)
    return response
