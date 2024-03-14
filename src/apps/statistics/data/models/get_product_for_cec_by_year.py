from asgiref.sync import sync_to_async

from src.apps.inventory.models import InventoryUnit, Product, ProductPrice


@sync_to_async
def get_products_for_cec_by_year(region_id: int = 0, category=None):
    filters = {'district__region_id': region_id}
    products_out = {}

    products = Product.objects.filter(category=category).only("id", "name_uz")

    for product in products:
        filters.update({'product': product, 'visible': True})
        key = f"{product.name_uz}_{product.id}"
        products_out[key] = []
        product_prices = ProductPrice.objects.filter(product=product)
        for product_price in product_prices:
            filters.update({'commissioning_year': product_price.year.year})
            inventory_counts = InventoryUnit.objects.filter(**filters).count()
            products_out[key].append({
                'year': product_price.year.year,
                'price': product_price.price,
                'inventory_count': inventory_counts,
            })

    return products_out
