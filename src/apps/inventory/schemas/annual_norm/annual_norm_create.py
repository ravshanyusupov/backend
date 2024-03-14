from ninja import Schema, Field


class AnnualNormCreateSchema(Schema):
    product_norm_id: int
    count: int = Field(..., gt=0, le=32767)
    year_id: int


class AnnualNormCreateInProductNormSchema(Schema):
    count: int = Field(..., gt=0, le=2147483647)
    year_id: int
