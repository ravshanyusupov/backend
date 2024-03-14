from ninja import Schema, Field


class ProductPriceCreateSchema(Schema):
    product_id: int
    year_id: int
    price: int = Field(..., gt=0, le=2147483647)
