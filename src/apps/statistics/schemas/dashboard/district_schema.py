from typing import List
from ninja import Schema
from src.apps.statistics.schemas.dashboard.base_schemas import CategoryOut, ResponsiblePersonOut, TotalOfProducts

# District User

class StoragePlaceOut(Schema):
    address: str
    category_items: List[CategoryOut]


class DistrictUserOut(Schema):
    responsible_persons: List[ResponsiblePersonOut]
    storage_place_products: List[StoragePlaceOut]
    Total: List[TotalOfProducts]
    
# End of District User