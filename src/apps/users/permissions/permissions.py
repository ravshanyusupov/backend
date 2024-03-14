from ninja_lib.permissions import BasePermission
from django.http import HttpRequest
from src.apps.users.models import User


class UserPermission(BasePermission):
    def has_permission(self, request: HttpRequest, user):
        return user.user_type in [User.CEC, User.DISTRICT, User.REGION]


class IsCECUser(BasePermission):
    def has_permission(self, request, user):
        return user.user_type == User.CEC


class IsRegionUser(BasePermission):
    def has_permission(self, request, user):
        return user.user_type == User.REGION


class IsDistrictUser(BasePermission):
    def has_permission(self, request, user):
        return user.user_type == User.DISTRICT
