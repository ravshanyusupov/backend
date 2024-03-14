from asgiref.sync import sync_to_async
from ninja_jwt.tokens import RefreshToken


@sync_to_async
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@sync_to_async
def blacklist_refresh_token(encoded_token):
    token = RefreshToken(encoded_token)
    token.blacklist()
