from abc import ABC, abstractmethod
from typing import Any, Optional

from ninja.security.http import HttpBearer
from ninja_jwt.authentication import AsyncJWTAuth
from ninja_jwt.exceptions import InvalidToken, TokenError, AuthenticationFailed
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.conf import settings

from .logger import logger


class AsyncHttpBearer(HttpBearer, ABC):
    async def __call__(self, request: HttpRequest) -> Optional[Any]:
        headers = request.headers
        auth_value = headers.get(self.header)
        if not auth_value:
            raise TokenError()
        parts = auth_value.split(" ")

        if parts[0].lower() != self.openapi_scheme:
            if settings.DEBUG:
                logger.error(f"Unexpected auth - '{auth_value}'")
            raise TokenError()
        token = " ".join(parts[1:])
        return await self.authenticate(request, token)

    @abstractmethod
    async def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        pass  # pragma: no cover


class CustomAsyncJWTAuth(AsyncHttpBearer, AsyncJWTAuth):
    def __init__(self, permissions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permissions = permissions

    async def authenticate(self, request, token):
        try:
            user = await AsyncJWTAuth().authenticate(request, token)
        except (InvalidToken, AuthenticationFailed):
            raise TokenError()

        if self.permissions:
            self.check_permissions(request, user)
        return user

    def get_permissions(self):
        return [permission() for permission in self.permissions]

    def check_permissions(self, request, user):
        for permission in self.get_permissions():
            if not permission.has_permission(request, user):
                raise PermissionDenied()
        return True
