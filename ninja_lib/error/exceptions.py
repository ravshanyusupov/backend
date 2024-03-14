class DomainException(Exception):
    def __init__(self, *code, ctx: dict = None, message: str = "") -> None:
        self.code = code
        self.ctx = ctx
        super().__init__(message)
