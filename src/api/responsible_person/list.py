from typing import List
from ninja import Query
from src.apps.dictionary.schemas import ResponsiblePersonSchema
from src.apps.dictionary.services.crud import responsible_person_crud
from src.apps.dictionary.filters import ResponsiblePersonFilter
from src.apps.core.filters import OrderFilter
from src.apps.users.permissions import UserPermission

from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

permissions = [UserPermission]
response = List[ResponsiblePersonSchema]


async def handler(
    request,
    filters: ResponsiblePersonFilter = Query(...),
    order_filter: OrderFilter = Query(...),
):
    """
    # Description

    **This endpoint gets a list of Responsible Persons based on the provided filters and ordering.**

    **Roles:**
    - `CEC User`: **Can get the list of Responsible Persons of any regions, and districts.**

    - `Region User`: **Can get the list of Responsible Persons of its own districts, and itself.**

    - `District User`: **Can get the list of Responsible Persons of its own district only.**

    """
    ordering = order_filter.ordering
    filter_args = filters.dict(exclude_unset=True)

    filter_conditions = {
        User.REGION: Q(region_id=request.user.region_id),
        User.DISTRICT: Q(district_id=request.user.district_id),
    }

    filter_args = filter_conditions.get(request.user.user_type, Q())
    filter_args &= filters.get_filter_expression()
    qs = await responsible_person_crud.get_list(
        select_related=["region", "district"], conditions=filter_args, ordering=ordering
    )
    return qs
