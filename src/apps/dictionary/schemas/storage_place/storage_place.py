from ninja import ModelSchema
from src.apps.dictionary.models import StoragePlace
from src.apps.dictionary.schemas import BuildingCategorySchema, DistrictDetailSchema


class StoragePlaceDetailSchema(ModelSchema):
    building_category: BuildingCategorySchema
    district: DistrictDetailSchema

    class Meta:
        model = StoragePlace
        fields = "__all__"


class StoragePlaceSchema(ModelSchema):
    building_category_id: int
    district_id: int

    class Meta:
        model = StoragePlace
        exclude = ["building_category", "district"]
