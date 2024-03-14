from ninja_lib.crud import CRUD_Queryset
from src.apps.inventory.models import AnnualNorm

annual_norm_crud = CRUD_Queryset(AnnualNorm)
