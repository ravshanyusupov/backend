from ninja import Schema
from typing import Optional
from pydantic import StrictStr, Field, validator

from src.apps.users.services.validator import validate_password


class UpdateUserSchema(Schema):
    id: int
    username: Optional[str]
    password: Optional[str] = Field(None)
    user_type: Optional[StrictStr]
    region_id: Optional[int] = None
    district_id: Optional[int] = None

    validate_password = validator("password", allow_reuse=True)(validate_password)
