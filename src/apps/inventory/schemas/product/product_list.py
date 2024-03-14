from ninja_lib.schema import BasePaginatedResponseSchema
from .product import ProductDetailSchema
from typing import List


class PaginatedProductSchema(BasePaginatedResponseSchema):
    items: List[ProductDetailSchema]
