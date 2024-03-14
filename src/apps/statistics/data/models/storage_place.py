from asgiref.sync import sync_to_async

from src.apps.dictionary.models import StoragePlace


@sync_to_async
def get_storage_places(filter_conditions):
    return StoragePlace.objects.filter(filter_conditions).only("address")