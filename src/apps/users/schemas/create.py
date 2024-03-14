from ninja import Schema
from typing import Optional
from pydantic import StrictStr, Field, validator

from src.apps.users.services.validator import validate_password


class UserCreateSchema(Schema):
    username: str
    user_type: StrictStr
    district_id: Optional[int] = None
    region_id: Optional[int] = None
    password: str = Field(...)

    validate_password = validator("password", allow_reuse=True)(validate_password)
