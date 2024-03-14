from ninja_lib.schema import BasePaginatedResponseSchema
from typing import List
from .storage_place import StoragePlaceDetailSchema


class PaginatedStoragePlaceSchema(BasePaginatedResponseSchema):
    items: List[StoragePlaceDetailSchema]
