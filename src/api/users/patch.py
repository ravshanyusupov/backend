from src.apps.users.services.crud import user_crud
from src.apps.users.permissions import UserPermission
from django.http import HttpRequest
from src.apps.users.schemas import UpdateUserSchema, UserSchema
from src.apps.users.services.validator import update_validator

permissions = [UserPermission]
response = UserSchema


async def handler(request: HttpRequest, payload: UpdateUserSchema):
    """
    # Description

    **This endpoint updates a User based on the provided ID and payload.**

    **Roles:**
    - `CEC User`: **Can update a User of any role.**

    - `Region User`: **Can update a User of its own districts only.**

    - `District User`: **Can update only the current user.**

    """
    user = await user_crud.read(pk=payload.id)
    payload_dict = {
        k: v for k, v in payload.dict(exclude_unset=True).items() if k != "password"
    }

    await update_validator(request, payload, user, payload_dict)

    updated_instance = await user_crud.update(user, payload_dict)
    if payload.password:
        updated_instance.set_password(payload.password)
        await updated_instance.asave()

    instance = await user_crud.read(
        pk=updated_instance.id, select_related=["region", "district"]
    )

    return instance
