from src.apps.dictionary.schemas import (
    IdResponsiblePersonSchema,
    ResponsiblePersonSchema,
)
from src.apps.dictionary.services.crud import responsible_person_crud
from src.apps.users.permissions import UserPermission

permissions = [UserPermission]
response = {200: ResponsiblePersonSchema}


async def handler(request, payload: IdResponsiblePersonSchema):
    """
    # Description

    **This endpoint gets a Responsible Person based on the provided ID.**

    **Roles:**
    - `CEC User`: **Can get the Responsible Person of any regions, and districts.**
    
    - `Region User`: **Can get the Responsible Person of its own districts, and itself.**

    - `District User`: **Can get the Responsible Person of its own district only.**

    """
    instance = await responsible_person_crud.read(
        payload.id, select_related=["region", "district"]
    )
    return 200, instance
