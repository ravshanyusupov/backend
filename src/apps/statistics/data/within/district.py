from django.db.models import Q

from src.apps.statistics.data.models import get_categories, get_products_with_number, get_storage_places, get_responsible_persons


async def get_data_within_district(district_id):
    inventory_places = []

    addresses = await get_storage_places(Q(district_id=district_id))
    responsible_persons = await get_responsible_persons(Q(district_id=district_id))
    responsible_persons_data = [
        f"{person.first_name} {person.last_name} {person.middle_name} ({person.passport_serial})"
        for person in responsible_persons
    ]
    category_names = await get_categories()
    async for address in addresses:
        category_data = []
        async for category in category_names:
            items = await get_products_with_number(district=district_id, storage_place=address, category=category)
            category_items = {"category_name":category.name_uz, "items":items}
            category_data.append(category_items)

        numbers_in_places = {"address":address.address, "responsible_persons":responsible_persons_data, "category_names":category_data}
        inventory_places.append(numbers_in_places)
    return {"products": inventory_places}
    