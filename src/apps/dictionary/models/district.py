from src.apps.core.models import TimeStampedModel, NamedModel
from django.db import models


class District(TimeStampedModel, NamedModel):
    region = models.ForeignKey(
        "dictionary.Region",
        on_delete=models.CASCADE,
        related_name="district_for_region",
    )
