from src.apps.statistics.data.models import (
    get_regions, 
    get_categories, 
    get_products_with_storage_place, 
    get_products_for_percent, 
    get_products_for_cec_by_year,
    get_products_with_id
    )
from src.apps.dictionary.models import Region


async def get_data_for_cec_by_percent():
    regions = await get_regions()
    categories = await get_categories()
    products_data = []
    async for region in regions:
        categories_data = []
        precincts_counts = Region.objects.filter(id=region["id"]).values_list("precincts_count", flat=True)
        value_of_precincts_count = [i async for i in precincts_counts]
        async for category in categories:
            items = await get_products_for_percent(region_id=region["id"], category=category)
            category_items = {"category_name": category.name_uz, "items": items}
            categories_data.append(category_items)
        region_products = {"region": region["name_uz"], "precincts_count": value_of_precincts_count[0], "categories": categories_data}
        products_data.append(region_products)
    return {"products": products_data}


async def get_data_for_cec_by_storage_place():
    regions = await get_regions()
    categories = await get_categories()
    products_data = []
    async for region in regions:
        categories_data = []
        async for category in categories:
            items = await get_products_with_storage_place(region_id=region["id"], category=category)
            category_items = {"category_name": category.name_uz, "items": items}
            categories_data.append(category_items)
        region_products = {"region":region["name_uz"], "categories": categories_data}
        products_data.append(region_products)
    return {"products": products_data}


async def get_data_for_cec_by_year():
    regions = await get_regions()
    categories = await get_categories()
    products_data = []
    async for region in regions:
        categories_data = []
        async for category in categories:
            items = await get_products_for_cec_by_year(region_id=region["id"], category=category)
            category_items = {"category_name": category.name_uz, "items": items}
            categories_data.append(category_items)
        region_products = {"region": region["name_uz"], "categories": categories_data}
        products_data.append(region_products)
    return {"products": products_data}
        

async def get_data_for_cec_by_products():
    regions = await get_regions()
    categories = await get_categories()
    products_data = []
    async for region in regions:
        categories_data = []
        async for category in categories:
            items = await get_products_with_id(region_id=region['id'], category=category)
            category_items = {"category_name": category.name_uz, "items": items}
            categories_data.append(category_items)
        region_products = {"region": region['name_uz'], "categories": categories_data}
        products_data.append(region_products)
    return {"products": products_data}
