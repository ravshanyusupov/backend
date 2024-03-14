from src.apps.inventory.schemas import AnnualNormCreateInProductNormSchema
from ninja import Schema
from typing import Optional, List


class ProductNormCreateSchema(Schema):
    product_id: int
    district_id: Optional[int] = None
    region_id: int
    annual_norms: List[AnnualNormCreateInProductNormSchema]
