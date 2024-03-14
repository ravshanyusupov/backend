from collections import Counter

from django.db.models import Q

from src.apps.statistics.data.models import get_categories, get_products, get_storage_places, get_responsible_persons
from src.apps.statistics.schemas.dashboard import StoragePlaceOut, DistrictUserOut, CategoryOut, TotalOfProducts


async def get_data_for_district_user(district_id):
    product_counter = Counter()
    responsible_persons = await get_responsible_persons(Q(district_id=district_id))
    storage_places = await get_storage_places(Q(district_id=district_id))
    categories = await get_categories()
    storage_place_out = []
    async for storage_place in storage_places:
        categories_data = []
        async for category in categories:
            items = await get_products(district=district_id, storage_place=storage_place, category=category)
            for item in items:
                product_counter[(item['product_name_uz'], item['product_name_ru'])] += item['inventory_count']
            category_items = CategoryOut(category_name_uz=category.name_uz, category_name_ru=category.name_ru, items=items).dict()
            categories_data.append(category_items)
        storage_place_products = StoragePlaceOut(address=storage_place.address, category_items=categories_data).dict()
        storage_place_out.append(storage_place_products)
    total_of_products = [TotalOfProducts(product_name_uz=name_uz, product_name_ru=name_ru, inventory_count=count) for (name_uz, name_ru), count in product_counter.items()]
    return DistrictUserOut(responsible_persons=responsible_persons, storage_place_products=storage_place_out, Total=total_of_products).dict()
