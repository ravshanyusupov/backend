from django.db import models


class NamedModel(models.Model):
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_uz = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name_uz

    class Meta:
        abstract = True
