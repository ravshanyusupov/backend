from django.db.models import Q
from asgiref.sync import sync_to_async
from src.apps.dictionary.models import District


@sync_to_async
def get_districts(region_id):
    return District.objects.filter(Q(region_id=region_id)).values("id", "name_uz", "name_ru")