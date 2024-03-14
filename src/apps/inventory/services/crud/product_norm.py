from ninja_lib.crud import CRUD_Queryset
from src.apps.inventory.models import ProductNorm


product_norm_crud = CRUD_Queryset(ProductNorm)
