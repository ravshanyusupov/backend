from src.apps.dictionary.models import District
from ninja_lib.crud import CRUD_Queryset


district_crud = CRUD_Queryset(District)
