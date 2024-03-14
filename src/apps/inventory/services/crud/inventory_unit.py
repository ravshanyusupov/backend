from src.apps.inventory.models import InventoryUnit
from ninja_lib.crud import CRUD_Queryset


inventory_unit_crud = CRUD_Queryset(InventoryUnit)
