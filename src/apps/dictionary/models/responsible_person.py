from django.db import models
from src.apps.core.models import TimeStampedModel


class ResponsiblePerson(TimeStampedModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    work_place = models.CharField(max_length=100)
    passport_serial = models.CharField(max_length=9, unique=True)
    job_title = models.CharField(max_length=50)
    order = models.CharField(max_length=20)
    date_of_order = models.DateTimeField()

    region = models.ForeignKey(
        "dictionary.Region",
        on_delete=models.CASCADE,
        related_name="responsible_person_for_region",
    )
    district = models.ForeignKey(
        "dictionary.District",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="responsible_person_for_district",
    )
