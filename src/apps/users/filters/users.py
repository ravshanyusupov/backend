from typing import Optional

from ninja import FilterSchema
from enum import Enum


class UserTypeEnum(str, Enum):
    C = "C"
    R = "R"
    D = "D"


class UserFilter(FilterSchema):
    username__icontains: Optional[str] = None
    user_type: Optional[UserTypeEnum] = None
    region_id: Optional[int] = None
    district_id: Optional[int] = None
