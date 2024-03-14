from django.db import models
from src.apps.core.models import TimeStampedModel


class InventoryUnit(TimeStampedModel):
    product = models.ForeignKey(
        "inventory.Product",
        on_delete=models.CASCADE,
        related_name="inventory_unit_for_product",
    )
    storage_place = models.ForeignKey(
        "dictionary.StoragePlace",
        on_delete=models.CASCADE,
        related_name="inventory_unit_for_storage_place",
    )
    write_off_act = models.ForeignKey(
        "inventory.WriteOffAct",
        on_delete=models.SET_NULL,
        related_name="inventory_unit_for_write_off_act",
        blank=True,
        null=True,
    )
    district = models.ForeignKey(
        "dictionary.District",
        on_delete=models.CASCADE,
        related_name="inventory_unit_for_district",
    )
    commissioning_year = models.PositiveSmallIntegerField()
    inventory_number = models.CharField(db_index=True, unique=True, max_length=50)
    visible = models.BooleanField(default=True)
