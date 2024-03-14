from src.apps.core.models import TimeStampedModel
from django.db import models


class StoragePlace(TimeStampedModel):
    building_category = models.ForeignKey(
        "dictionary.BuildingCategory",
        on_delete=models.CASCADE,
        related_name="storage_place_for_building_category",
    )
    district = models.ForeignKey(
        "dictionary.District",
        on_delete=models.CASCADE,
        related_name="storage_place_for_district",
    )
    address = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.address
