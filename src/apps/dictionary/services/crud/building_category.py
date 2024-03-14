from ninja_lib.crud import CRUD_Queryset
from src.apps.dictionary.models import BuildingCategory

building_category_crud = CRUD_Queryset(BuildingCategory)
