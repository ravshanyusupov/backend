from ninja import Schema


class YearPatchSchema(Schema):
    id: int
    year: int
