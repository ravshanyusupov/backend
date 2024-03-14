from src.apps.users.permissions import UserPermission
from src.apps.dictionary.schemas import YearDetailSchema
from src.apps.dictionary.services.crud import year_crud
from src.apps.core.filters import OrderFilter
from typing import List
from ninja import Query
from django.db.models import Q

permissions = [UserPermission]
response = List[YearDetailSchema]


async def handler(request, order_filter: OrderFilter = Query(...)):
    """
    # Description

    **This endpoint gets a list of Years based on the provided ordering parameters.**

    **Roles:**
    - `CEC User`

    - `Region User`

    - `District User`
    """
    ordering = order_filter.ordering
    qs = await year_crud.get_list(ordering=ordering)

    return qs
