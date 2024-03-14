from typing import Optional

from ninja import ModelSchema
from src.apps.users.models import User
from src.apps.dictionary.schemas import RegionSchema, DistrictSchema


class UserSchema(ModelSchema):
    region: Optional[RegionSchema] = None
    district: Optional[DistrictSchema] = None

    class Meta:
        model = User
        fields = ["id", "username", "user_type", "region", "district"]
