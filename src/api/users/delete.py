from src.apps.users.services.crud import user_crud
from src.apps.users.schemas import UserIdSchema
from src.apps.users.permissions import UserPermission
from src.apps.users.services.validator import delete_validator

response = {204: None}
permissions = [UserPermission]


async def handler(request, payload: UserIdSchema):
    """
    # Description

    **This endpoint deletes a User based on the provided ID.**

    **Roles:**
    - `CEC User`: **Can delete a User of any role.**

    - `Region User`: **Can delete a User for its own districts.**

    - `District User`: **Can delete the current user only.**

    """
    user = await user_crud.read(pk=payload.id)
    await delete_validator(request.user, user)
    await user_crud.delete(user)

    return 204, None
