from ninja import Schema
from pydantic import constr
from typing import Optional


class BaseSchema(Schema):
    name_uz: constr(min_length=1, strip_whitespace=True)
    name_ru: Optional[constr(min_length=1, strip_whitespace=True)] = None


class BasePatchSchema(Schema):
    id: int
    name_uz: Optional[constr(min_length=1, strip_whitespace=True)] = None
    name_ru: Optional[constr(min_length=1, strip_whitespace=True)] = None

