from django.contrib import admin

from src.apps.statistics.models import StatisticData

# Register your models here.


@admin.register(StatisticData)
class StatisticDataAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "updated_at")
    list_filter = ("name", "updated_at")
    fields = ("name", "data")
    
