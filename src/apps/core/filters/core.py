from ninja import Schema


class OrderFilter(Schema):
    ordering: list = ["-created_at", "-updated_at"]
