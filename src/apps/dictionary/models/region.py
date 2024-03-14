from src.apps.core.models import TimeStampedModel, NamedModel
from django.db import models


class Region(TimeStampedModel, NamedModel):
    precincts_count = models.PositiveSmallIntegerField(default=0)
