from ninja import Schema


class LoginSchema(Schema):
    username: str
    password: str


class LoginResponseSchema(Schema):
    access: str
    refresh: str
