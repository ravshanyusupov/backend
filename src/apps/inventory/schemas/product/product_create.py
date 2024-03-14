from typing import Optional

from ninja import Schema
from src.apps.core.schemas import BaseSchema


class ProductCreateSchema(BaseSchema):
    category_id: int
