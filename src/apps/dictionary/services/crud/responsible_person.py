from src.apps.dictionary.models import ResponsiblePerson
from ninja_lib.crud import CRUD_Queryset


responsible_person_crud = CRUD_Queryset(ResponsiblePerson)
