from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from src.apps.core.models import TimeStampedModel


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if username is None:
            raise TypeError("username required to login")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        if username is None:
            raise TypeError("username is required to login")
        if password is None:
            raise TypeError("Password is required to login")
        user = self.create_user(username=username, password=password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    CEC = "C"
    REGION = "R"
    DISTRICT = "D"

    TYPE_CHOICES = [
        (CEC, "CEC"),
        (REGION, "Region"),
        (DISTRICT, "District"),
    ]

    username = models.CharField(db_index=True, max_length=100, unique=True)
    user_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=DISTRICT)
    region = models.ForeignKey(
        "dictionary.Region",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user_for_region",
    )
    district = models.ForeignKey(
        "dictionary.District",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user_for_district",
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
