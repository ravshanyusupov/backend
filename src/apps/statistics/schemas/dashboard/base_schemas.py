from typing import List
from ninja import Schema


class ItemOut(Schema):
    product_name_uz: str
    product_name_ru: str
    inventory_count: int


class CategoryOut(Schema):
    category_name_uz: str
    category_name_ru: str
    items: List[ItemOut]


class ResponsiblePersonOut(Schema):
    first_name: str
    last_name: str
    middle_name: str
    passport_serial: str


class TotalOfProducts(Schema):
    product_name_uz: str
    product_name_ru: str
    inventory_count: int
