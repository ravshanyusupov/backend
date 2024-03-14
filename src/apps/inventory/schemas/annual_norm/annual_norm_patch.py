from ninja import Schema
from typing import Optional


class AnnualNormPatchSchema(Schema):
    id: int
    year_id: Optional[int] = None
    count: Optional[int] = None
