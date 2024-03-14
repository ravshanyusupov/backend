from typing import List
from ninja import Schema
from src.apps.core.schemas import BaseSchema


class CreateWriteOffActSchema(BaseSchema):
    inventory_numbers: List[str]
