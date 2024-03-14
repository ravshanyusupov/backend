from src.apps.core.models import TimeStampedModel, NamedModel
from django.db import models


class Product(TimeStampedModel, NamedModel):
    category = models.ForeignKey(
        "inventory.Category",
        on_delete=models.CASCADE,
        related_name="product_for_category",
    )
