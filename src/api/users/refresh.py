from src.apps.users.schemas import AccessTokenSchema, RefreshTokenSchema
from ninja_jwt.tokens import RefreshToken

response = AccessTokenSchema
auth = None


async def handler(request, payload: RefreshTokenSchema):
    """
    # Description

    **This endpoint refreshes the access token.**

    """
    refresh = RefreshToken(payload.refresh)

    return {"access": str(refresh.access_token)}
