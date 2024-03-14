from src.apps.statistics.data.models import get_categories, get_products, get_districts


async def get_data_within_region(region_id):
    data = {}

    district_names = await get_districts(region_id)
    category_names = await get_categories()
    async for district_name in district_names:
        data[district_name['name_uz']] = {"district_name": district_name['name_uz'], "category_items": []}
        async for category in category_names:
            items = await get_products(district=district_name['id'], category=category)
            category_items = {"category_name":category.name_uz, "items":items}
            data[district_name['name_uz']]["category_items"].append(category_items)

    return data
