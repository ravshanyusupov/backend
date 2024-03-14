from collections import Counter

from django.db.models import Q

from src.apps.statistics.data.models import get_categories, get_products, get_districts, get_responsible_persons
from src.apps.statistics.schemas.dashboard import RegionProductsOut, RegionUserOut, CategoryOut, TotalOfProducts
from src.apps.dictionary.models import Region


async def get_data_for_region_user(region_id):
    region = await Region.objects.aget(id=region_id)
    region_name_uz = region.name_uz
    region_name_ru = region.name_ru
    product_counter = Counter()
    districts = await get_districts(region_id)
    categories = await get_categories()
    products_data = []
    async for district in districts:
        categories_data = []
        async for category in categories:
            items = await get_products(district=district['id'], category=category)
            for item in items:
                product_counter[(item['product_name_uz'], item['product_name_ru'])] += item['inventory_count']
            category_items = CategoryOut(category_name_uz=category.name_uz, category_name_ru=category.name_ru, items=items).dict()
            categories_data.append(category_items)
        responsible_persons = await get_responsible_persons(Q(district_id=district['id']))
        district_products = RegionProductsOut(district_name_uz=district['name_uz'], district_name_ru=district['name_ru'], responsible_persons=responsible_persons, categories=categories_data).dict()
        products_data.append(district_products)
    total_of_products = [TotalOfProducts(product_name_uz=name_uz, product_name_ru=name_ru, inventory_count=count) for (name_uz, name_ru), count in product_counter.items()]
    return RegionUserOut(region_name_uz=region_name_uz, region_name_ru=region_name_ru, products=products_data, Total=total_of_products).dict()
