from src.apps.core.models import TimeStampedModel
from django.db import models


class Year(TimeStampedModel):
    year = models.PositiveSmallIntegerField(unique=True)

    def __str__(self) -> str:
        return str(self.year)
