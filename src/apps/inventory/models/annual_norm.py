from src.apps.core.models import TimeStampedModel
from django.db import models


class AnnualNorm(TimeStampedModel):
    product_norm = models.ForeignKey(
        "inventory.ProductNorm",
        on_delete=models.CASCADE,
        related_name="annual_norm_for_product_norm",
    )
    count = models.PositiveIntegerField()
    year = models.ForeignKey(
        "dictionary.Year",
        on_delete=models.CASCADE,
        related_name="year_for_annual_norm",
    )

    class Meta:
        unique_together = ("product_norm", "year")
