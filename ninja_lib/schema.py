from typing import Any, List, Union
from ninja import Schema


class BasePaginatedResponseSchema(Schema):
    """To use this schema you need to provide items key"""

    items: Any
    total: int
    page: int
    size: int


# class BaseErrorSchema(Schema):
#     name_uz: str
#     name_ru: str
#     code: Union[str, int]
#     location: str = None
#
#
# class BaseErrorResponseSchema(Schema):
#     root: List[BaseErrorSchema]
