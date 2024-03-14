from src.apps.dictionary.models import StoragePlace
from ninja_lib.crud import CRUD_Queryset


storage_place_crud = CRUD_Queryset(StoragePlace)
