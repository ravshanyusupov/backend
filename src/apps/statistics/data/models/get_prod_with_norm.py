from asgiref.sync import sync_to_async
from src.apps.inventory.models import InventoryUnit, Product


@sync_to_async
def get_products_for_percent(region_id: int = 0, category=None):
    filters = {'district__region_id': region_id}
    products_out = {}

    products = Product.objects.filter(category=category).only("id", "name_uz")

    for product in products:
        filters.update({'product': product, 'visible': True})
        products_out[product.name_uz] = []
        inventory_counts = InventoryUnit.objects.filter(**filters).count()
        products_out[product.name_uz].append({
            "inventory_counts": inventory_counts,
            "product_id": product.id,
        })
    return products_out

