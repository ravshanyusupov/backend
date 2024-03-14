from ninja_lib.crud import CRUD_Queryset

from src.apps.users.models import User

user_crud = CRUD_Queryset(User)
