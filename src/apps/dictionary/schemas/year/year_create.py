from ninja import Schema, Field


class YearCreateSchema(Schema):
    year: int = Field(..., gt=0, le=32767)
