from typing import List
from ninja import Schema
from src.apps.statistics.schemas.dashboard.base_schemas import CategoryOut, TotalOfProducts


# CEC User

class CECProductsOut(Schema):
    region_name_uz: str
    region_name_ru: str
    categories: List[CategoryOut]

class CECUserOut(Schema):
    products: List[CECProductsOut]
    Total: List[TotalOfProducts]

# End of CEC User