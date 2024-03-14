from django.contrib import admin
from src.apps.inventory.models import (
    Category,
    Product,
    ProductPrice,
    InventoryUnit,
    ProductNorm,
    WriteOffAct,
    AnnualNorm,
)

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name_ru", "name_uz", "created_at", "updated_at")
    list_filter = ("created_at",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "name_ru", "name_uz", "created_at", "updated_at")
    list_filter = ("category", "created_at")


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "price", "year", "created_at", "updated_at")
    list_filter = ("product", "year", "created_at", "price")


@admin.register(InventoryUnit)
class InventoryUnitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "storage_place",
        "write_off_act",
        "commissioning_year",
        "inventory_number",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "product",
        "storage_place",
        "write_off_act",
        "commissioning_year",
        "created_at",
    )


@admin.register(ProductNorm)
class ProductNormAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "district",
        "region",
        "created_at",
        "updated_at",
    )
    list_filter = ("product", "district", "region", "created_at")


@admin.register(WriteOffAct)
class WriteOffActAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "district",
        "region",
        "file",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("district", "region", "status", "created_at")


@admin.register(AnnualNorm)
class AnnualNormAdmin(admin.ModelAdmin):
    list_display = ("id", "product_norm", "count", "year")
    list_filter = ("product_norm", "year")
