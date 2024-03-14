from ninja import ModelSchema
from src.apps.dictionary.models import Region


class RegionSchema(ModelSchema):
    class Meta:
        model = Region
        fields = "__all__"
        fields_optional = "__all__"
