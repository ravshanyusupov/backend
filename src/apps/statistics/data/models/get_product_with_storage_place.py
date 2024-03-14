from asgiref.sync import sync_to_async
from src.apps.inventory.models import InventoryUnit, Product
from src.apps.dictionary.models import StoragePlace, BuildingCategory


@sync_to_async
def get_products_with_storage_place(region_id: int = 0, district=None, category=None):
    filter_args = {
        True: {'district__region_id': region_id},
        False: {'district': district},
    }
    filters = filter_args.get(bool(region_id))
    products_out = {}
    building_categories = BuildingCategory.objects.all()
    products = Product.objects.filter(category=category).only("id", "name_uz")
    
    for product in products:
        filters.update({'product': product, 'visible': True})
        products_out[product.name_uz] = []

        for building_category in building_categories:
            storage_places = StoragePlace.objects.filter(building_category=building_category)
            filters.update({'storage_place__in': storage_places})

            inventory_counts = InventoryUnit.objects.filter(**filters).count()

            products_out[product.name_uz].append({
                "building_category": building_category.name_uz, 
                "inventory_counts": inventory_counts,
                "product_id": product.id,
            })

    return products_out
