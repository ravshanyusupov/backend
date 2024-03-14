from ninja_lib.crud import CRUD_Queryset
from src.apps.inventory.models import WriteOffAct


write_off_act_crud = CRUD_Queryset(WriteOffAct)
