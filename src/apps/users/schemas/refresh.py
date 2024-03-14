from ninja import Schema


class RefreshTokenSchema(Schema):
    refresh: str


class AccessTokenSchema(Schema):
    access: str
