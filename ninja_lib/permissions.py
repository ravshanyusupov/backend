class OperationHolderMixin:
    def __and__(self, other):
        return OperandHolder(AND, self, other)

    def __or__(self, other):
        return OperandHolder(OR, self, other)

    def __rand__(self, other):
        return OperandHolder(AND, other, self)

    def __ror__(self, other):
        return OperandHolder(OR, other, self)

    def __invert__(self):
        return SingleOperandHolder(NOT, self)


class SingleOperandHolder(OperationHolderMixin):
    def __init__(self, operation_type, perm1):
        self.operator_type = operation_type
        self.perm_class = perm1

    def __call__(self, *args, **kwargs):
        perm = self.perm_class(*args, **kwargs)
        return self.operator_type(perm)


class OperandHolder(OperationHolderMixin):
    def __init__(self, operation_type, perm1, perm2):
        self.operation_type = operation_type
        self.perm1_class = perm1
        self.perm2_class = perm2

    def __call__(self, *args, **kwargs):
        perm1 = self.perm1_class(*args, **kwargs)
        perm2 = self.perm2_class(*args, **kwargs)
        return self.operation_type(perm1, perm2)

    def __eq__(self, other):
        return (
            isinstance(other, OperandHolder)
            and self.operation_type == other.operation_type
            and self.perm1_class == other.perm1_class
            and self.perm2_class == other.perm2_class
        )


class AND:
    def __init__(self, perm_1, perm_2):
        self.perm_1 = perm_1
        self.perm_2 = perm_2

    def has_permission(self, request, user):
        return self.perm_1.has_permission(request, user) and self.perm_2.has_permission(
            request, user
        )


class OR:
    def __init__(self, perm_1, perm_2):
        self.perm_1 = perm_1
        self.perm_2 = perm_2

    def has_permission(self, request, user):
        return self.perm_1.has_permission(request, user) or self.perm_2.has_permission(
            request, user
        )


class NOT:
    def __init__(self, perm):
        self.perm = perm

    def has_permission(self, request, user):
        return not self.perm.has_permission(request, user)


class BasePermissionMetaclass(OperationHolderMixin, type):
    pass


class BasePermission(metaclass=BasePermissionMetaclass):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, user):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True
