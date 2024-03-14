from src.apps.users.schemas import LoginSchema, LoginResponseSchema
from django.contrib.auth import authenticate
from ninja_lib.error import DomainException
from ninja_lib.jwt import get_tokens_for_user
from asgiref.sync import sync_to_async

auth = None
response = LoginResponseSchema


async def handler(request, payload: LoginSchema):
    """
    # Description

    **This endpoint authenticates the user based on the credentials(login and password). The response provides access and refresh tokens.**

    """
    user = await sync_to_async(authenticate)(
        username=payload.username, password=payload.password
    )

    if user is None:
        raise DomainException(2006)

    return await get_tokens_for_user(user)
