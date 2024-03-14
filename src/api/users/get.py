from src.apps.users.services.crud import user_crud
from src.apps.users.schemas import UserSchema, UserIdSchema
from src.apps.users.permissions import UserPermission
from src.apps.users.services.validator import read_validator

permissions = [UserPermission]
response = UserSchema


async def handler(request, payload: UserIdSchema):
    """
    # Description

    **This endpoint gets a User based on the provided ID.**

    **Roles:**
    - `CEC User`: **Can get any User of any role.**

    - `Region User`: **Can get a User with the same Region as the current user, and it's own districts' users.**
    
    - `District User`: **Can get a User with the same District as the current user.**

    """
    instance = await user_crud.read(
        pk=payload.id, select_related=["region", "district"]
    )
    await read_validator(request.user, instance)
    return instance
