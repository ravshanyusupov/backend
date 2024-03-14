from src.apps.dictionary.models import Region
from ninja_lib.crud import CRUD_Queryset


region_crud = CRUD_Queryset(Region)
