from ninja_lib.schema import BasePaginatedResponseSchema
from src.apps.users.schemas import UserSchema
from typing import List


class PaginatedUserSchema(BasePaginatedResponseSchema):
    items: List[UserSchema]
