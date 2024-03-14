from typing import List
from ninja import Schema
from src.apps.statistics.schemas.dashboard.base_schemas import CategoryOut, ResponsiblePersonOut, TotalOfProducts

# Region User

class RegionProductsOut(Schema):
    district_name_uz: str
    district_name_ru: str
    responsible_persons: List[ResponsiblePersonOut]
    categories: List[CategoryOut]

class RegionUserOut(Schema):
    region_name_uz: str
    region_name_ru: str
    products: List[RegionProductsOut]
    Total: List[TotalOfProducts]

# End of Region User