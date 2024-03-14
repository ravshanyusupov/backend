from src.apps.users.permissions import UserPermission
from src.apps.users.schemas import UserSchema
from src.apps.users.services.crud import user_crud
from django.http import HttpRequest

permissions = [UserPermission]
response = UserSchema


async def handler(request: HttpRequest):
    """
    # Description

    **This endpoint shows the details of the currently authenticated User.**

    **Roles:**
    - `CEC User`
    - `Region User`
    - `District User`

    """
    instance = await user_crud.read(
        pk=request.user.id, select_related=["region", "district"]
    )
    return instance
