from asgiref.sync import sync_to_async
from src.apps.inventory.models import Category


@sync_to_async
def get_categories():
    return Category.objects.only("name_uz", "name_ru")