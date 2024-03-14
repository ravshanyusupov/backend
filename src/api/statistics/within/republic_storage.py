from src.apps.users.permissions import IsCECUser
from src.apps.statistics.excels.within import WithinRepublicStorage
from src.apps.statistics.models import StatisticData


permissions = [IsCECUser]


async def handler(request):
    """
    # Description

    **This endpoint generates Excel Report about products with Storage Places Within the Republic.**

    **Roles:**

    - `CEC User`

    """
    try:
        data = (
            await StatisticData.objects.aget(name="Data_for_within_republic_storage")
        ).data
    except StatisticData.DoesNotExist:
        data = {}
    report = WithinRepublicStorage(data)
    report.generate_report()
    response = report.get_http_response("Respublika_miqyosida_saqlash_joyi")

    return response
