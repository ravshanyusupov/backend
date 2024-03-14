from ninja import Schema
from src.apps.dictionary.models import StoragePlace


class CreateStoragePlaceSchema(Schema):
    building_category_id: int
    district_id: int
    address: str
