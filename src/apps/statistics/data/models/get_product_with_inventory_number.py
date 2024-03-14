from asgiref.sync import sync_to_async
from src.apps.inventory.models import InventoryUnit, Product


@sync_to_async
def get_products_with_number(district=None, storage_place=None, category=None):
    filters = {
        'district': district,
    }
    products_data = Product.objects.filter(category=category).only("id", "name_uz")
    products_out = []
    for product in products_data:
        filters.update({'product': product, 'visible': True})
        if storage_place:
            filters.update({'storage_place': storage_place})
        inventory_counts = InventoryUnit.objects.filter(**filters).values_list('inventory_number', flat=True)
        if inventory_counts:
            for inventory_number in inventory_counts:
                products_out.append(
                    {
                        'product_name': product.name_uz,
                        'inventory_number': inventory_number,
                        'inventory_count': 1
                    }
                )
        else:
            products_out.append(
                    {
                        'product_name': product.name_uz,
                        'inventory_number': None,
                        'inventory_count': None
                    }
                )
    return products_out