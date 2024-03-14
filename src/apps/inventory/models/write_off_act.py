from django.db import models
from src.apps.core.models import TimeStampedModel, NamedModel


def upload_path(instance, filename):
    return f"write_off_acts/district/{instance.district.id}/{filename}"


class WriteOffAct(NamedModel, TimeStampedModel):
    PENDING_REGION = "PR"
    PENDING_CEC = "PC"
    APPROVED = "AD"
    REJECTED = "RD"

    STATUS_CHOICES = [
        (PENDING_REGION, "Pending region"),
        (PENDING_CEC, "Pending cec"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    district = models.ForeignKey(
        "dictionary.District",
        on_delete=models.CASCADE,
        related_name="write_off_act_for_district",
    )
    region = models.ForeignKey(
        "dictionary.Region",
        on_delete=models.CASCADE,
        related_name="write_off_act_for_region",
    )
    file = models.FileField(upload_to=upload_path)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=PENDING_REGION
    )

    def __str__(self) -> str:
        return self.name_uz
