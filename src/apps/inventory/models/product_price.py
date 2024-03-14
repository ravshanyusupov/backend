from django.db import models
from src.apps.core.models import TimeStampedModel


class ProductPrice(TimeStampedModel):
    product = models.ForeignKey(
        "inventory.Product",
        on_delete=models.CASCADE,
        related_name="product_price_for_product",
    )
    price = models.PositiveIntegerField(default=0)
    year = models.ForeignKey(
        "dictionary.Year",
        on_delete=models.CASCADE,
        related_name="year_for_product_price",
    )

    class Meta:
        unique_together = ("product", "year")
