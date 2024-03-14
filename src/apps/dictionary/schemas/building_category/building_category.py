from ninja import ModelSchema
from src.apps.dictionary.models.building_category import BuildingCategory


class BuildingCategorySchema(ModelSchema):
    class Meta:
        model = BuildingCategory
        fields = "__all__"
