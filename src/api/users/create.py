from src.apps.users.schemas import UserCreateSchema, UserSchema
from src.apps.users.services.crud import user_crud
from src.apps.users.permissions import UserPermission
from src.apps.users.services.validator import payload_validator

response = {201: UserSchema}
permissions = [UserPermission]


async def handler(request, payload: UserCreateSchema):
    """
    # Description

    **This endpoint creates a new User with the provided payload.**
    **The user_type field accepts the values 'C', 'R' and 'D', where 'C' corresponds to CEC USER, 'R' - REGION USER, 'D' - DISTRICT USER.**

    **Roles:**
    - `CEC User`: **Can create a new User of any role.**
    
    - `Region User`: **Can create a new User of same Region as the current user, and for it's own districts' users.**

    - `District User`: **Can create a new user only for it's own district.**

    """
    await payload_validator(request, payload)
    instance = await user_crud.create(payload.dict())
    instance.set_password(payload.password)
    await instance.asave()
    instance = await user_crud.read(
        pk=instance.id, select_related=["region", "district"]
    )

    return 201, instance
