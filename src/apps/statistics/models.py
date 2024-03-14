from django.db import models


class StatisticData(models.Model):
    name = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    data = models.JSONField()

    def __str__(self):
        return self.name
