from src.apps.dictionary.models import District
from src.apps.dictionary.schemas.region import RegionSchema
from ninja import ModelSchema


class DistrictSchema(ModelSchema):
    class Meta:
        model = District
        fields = "__all__"
        fields_optional = "__all__"


class DistrictDetailSchema(ModelSchema):
    region: RegionSchema

    class Meta:
        model = District
        exclude = ["region"]
        fields_optional = "__all__"
