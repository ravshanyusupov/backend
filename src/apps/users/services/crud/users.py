from ninja_lib.crud import CRUD_Queryset
from src.apps.users.models.user import User

crud_instance = CRUD_Queryset(User)
