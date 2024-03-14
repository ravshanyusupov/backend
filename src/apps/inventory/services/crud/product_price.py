from ninja_lib.crud import CRUD_Queryset
from src.apps.inventory.models import ProductPrice

product_price_crud = CRUD_Queryset(ProductPrice)
