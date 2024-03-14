from ninja_lib.crud import CRUD_Queryset
from src.apps.inventory.models import Product

product_crud = CRUD_Queryset(Product)
