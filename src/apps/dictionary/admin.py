from django.contrib import admin
from src.apps.dictionary.models import (
    Region,
    District,
    BuildingCategory,
    StoragePlace,
    ResponsiblePerson,
    Year,
)

# Register your models here.


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name_ru", "name_uz", "created_at", "updated_at")
    list_filter = ("created_at",)


@admin.register(District)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "region", "name_ru", "name_uz", "created_at", "updated_at")
    list_filter = ("region", "created_at")


@admin.register(BuildingCategory)
class BuildingCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name_ru", "name_uz", "created_at")
    list_filter = ("created_at",)


@admin.register(StoragePlace)
class StoragePlaceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "building_category",
        "district",
        "address",
        "created_at",
        "updated_at",
    )
    list_filter = ("building_category", "district", "created_at")


@admin.register(ResponsiblePerson)
class ResponsiblePersonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone_number",
        "work_place",
        "job_title",
        "region",
        "district",
        "created_at",
        "updated_at",
    )
    list_filter = ("region", "district", "work_place", "job_title", "created_at")


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ("id", "year", "created_at", "updated_at")
