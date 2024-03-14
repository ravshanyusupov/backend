from src.apps.users.permissions import IsDistrictUser
from src.apps.statistics.excels.within import WithinDistrict
from src.apps.statistics.models import StatisticData
from src.apps.dictionary.services.crud import district_crud


permissions = [IsDistrictUser]

async def handler(request):
    """
    # Description

    **This endpoint generates Excel Report about products Within the District.**

    **Roles:**

    - `District User`

    """
    instance = await district_crud.read(pk=request.user.district_id, select_related=["region"])
    region_name = instance.region.name_uz
    district_name = instance.name_uz
    try:
        data = (await StatisticData.objects.aget(name=f'Data_for_within_district_{request.user.district_id}')).data
    except StatisticData.DoesNotExist:
        data = {}

    report = WithinDistrict(data=data, region_name=region_name, district_name=district_name)
    report.generate_report()
    response = report.get_http_response('Tuman_miqyosida')

    return response