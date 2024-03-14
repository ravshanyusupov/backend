from src.apps.users.permissions import IsRegionUser
from src.apps.dictionary.services.crud import region_crud
from src.apps.statistics.excels.within import WithinRegion
from src.apps.statistics.models import StatisticData


permissions = [IsRegionUser]

async def handler(request):
    """
    # Description

    **This endpoint generates Excel Report about products Within the Region.**

    **Roles:**

    - `Region User`

    """
    instance = await region_crud.read(pk=request.user.region_id)
    region_name = instance.name_uz
    try:
        data = (await StatisticData.objects.aget(name=f'Data_for_within_region_{request.user.region_id}')).data
    except StatisticData.DoesNotExist:
        data = {}
    
    report = WithinRegion(data=data, region_name=region_name)
    
    report.generate_report()
    response = report.get_http_response('Viloyat_miqyosida')

    return response