from ninja_lib.crud import CRUD_Queryset
from src.apps.inventory.models import Category


category_crud = CRUD_Queryset(Category)
