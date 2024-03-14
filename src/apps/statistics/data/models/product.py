from asgiref.sync import sync_to_async
from src.apps.inventory.models import InventoryUnit, Product


@sync_to_async
def get_products(region_id: int = 0, district=None, storage_place=None, category=None):
    filter_args = {
        True: {"district__region_id": region_id},
        False: {"district": district},
    }
    filters = filter_args.get(bool(region_id))
    queryset = Product.objects.filter(category=category).only("id", "name_uz", "name_ru")
    products_data = list(queryset)
    products_out = []
    for product in products_data:
        filters.update({"product": product, "visible": True})
        if storage_place:
            filters.update({"storage_place": storage_place})
        inventory_counts = InventoryUnit.objects.filter(**filters).count()

        products_out.append(
            {
                "product_name_uz": product.name_uz,
                "product_name_ru": product.name_ru,
                "inventory_count": inventory_counts,
            }
        )
    return products_out
