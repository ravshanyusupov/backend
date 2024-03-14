from asgiref.sync import sync_to_async
from src.apps.dictionary.models import Region


@sync_to_async
def get_regions():
    return Region.objects.values("id", "name_uz", "name_ru")