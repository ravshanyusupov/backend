from ninja import ModelSchema
from src.apps.inventory.models import ProductNorm
from src.apps.dictionary.schemas import RegionSchema, DistrictSchema
from src.apps.inventory.schemas import ProductDetailSchema, AnnualNormDetailSchema
from typing import Optional, List


class ProductNormDetailSchema(ModelSchema):
    product: ProductDetailSchema
    region: RegionSchema
    district: Optional[DistrictSchema] = None
    annual_norms: List[AnnualNormDetailSchema]

    class Meta:
        model = ProductNorm
        fields = "__all__"

    @staticmethod
    def resolve_annual_norms(obj):
        annual_norms = obj.annual_norm_for_product_norm.all()

        return annual_norms
