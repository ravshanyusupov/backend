from ninja import ModelSchema
from src.apps.dictionary.models import ResponsiblePerson
from src.apps.dictionary.schemas import RegionSchema, DistrictSchema


class ResponsiblePersonSchema(ModelSchema):
    region: RegionSchema
    district: DistrictSchema

    class Meta:
        model = ResponsiblePerson
        exclude = ["region", "district"]
