from src.apps.users.permissions import IsCECUser
from src.apps.statistics.excels.within import WithinRepublicPercent
from src.apps.statistics.models import StatisticData


permissions = [IsCECUser]


async def handler(request):
    """
    # Description

    **This endpoint generates Excel Report about products by percentage Within the Republic.**

    **Roles:**

    - `CEC User`

    """
    try:
        data = (
            await StatisticData.objects.aget(name="Data_for_within_republic_percent")
        ).data
    except StatisticData.DoesNotExist:
        data = {}

    report = WithinRepublicPercent(data)
    report.generate_report()
    response = report.get_http_response("Respublika_miqyosida_foiz")

    return response
