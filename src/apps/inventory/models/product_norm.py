from src.apps.core.models import TimeStampedModel
from django.db import models


class ProductNorm(TimeStampedModel):
    product = models.ForeignKey(
        "inventory.Product",
        on_delete=models.CASCADE,
        related_name="product_norm_for_product",
    )
    district = models.ForeignKey(
        "dictionary.District",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="product_norm_for_district",
    )
    region = models.ForeignKey(
        "dictionary.Region",
        on_delete=models.CASCADE,
        related_name="product_norm_for_region",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "region", "district"],
                condition=models.Q(district__isnull=False),
                name="unique_region_product_with_district",
            ),
            models.UniqueConstraint(
                fields=["product", "region"],
                condition=models.Q(district__isnull=True),
                name="unique_region_product_without_district",
            ),
        ]
