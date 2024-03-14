from src.apps.inventory.models import AnnualNorm
from ninja import ModelSchema


class AnnualNormDetailSchema(ModelSchema):
    class Meta:
        model = AnnualNorm
        fields = ["id", "year", "count"]
