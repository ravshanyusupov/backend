from collections import Counter

from src.apps.statistics.data.models import get_regions, get_categories, get_products
from src.apps.statistics.schemas.dashboard import CECUserOut, CECProductsOut, CategoryOut, TotalOfProducts


async def get_data_for_cec_user():
    product_counter = Counter()
    regions = await get_regions()
    categories = await get_categories()
    products_data = []
    async for region in regions:
        categories_data = []
        async for category in categories:
            items = await get_products(region_id=region['id'], category=category)
            for item in items:
                product_counter[(item['product_name_uz'], item['product_name_ru'])] += item['inventory_count']
            category_items = CategoryOut(category_name_uz=category.name_uz, category_name_ru=category.name_ru, items=items).dict()
            categories_data.append(category_items)
        region_products = CECProductsOut(region_name_uz=region['name_uz'], region_name_ru=region['name_ru'], categories=categories_data).dict()
        products_data.append(region_products)
    total_of_products = [TotalOfProducts(product_name_uz=name_uz, product_name_ru=name_ru, inventory_count=count) for (name_uz, name_ru), count in product_counter.items()]
    return CECUserOut(products=products_data, Total=total_of_products).dict()
