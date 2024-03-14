import asyncio

import pytest

from src.apps.inventory.models import InventoryUnit
from src.apps.statistics.models import StatisticData
from src.apps.statistics.data.dashboard import (
    get_data_for_cec_user, 
    get_data_for_region_user, 
    get_data_for_district_user
    )


@pytest.mark.parametrize(
    "for_loop_times",
    [(0), (1), (5)],
)
@pytest.mark.django_db(transaction=True)
def test_data_cec(for_loop_times, cec_client, url_name, inventory_unit_factory):
    for _ in range(for_loop_times):
        inventory_unit = inventory_unit_factory.create()
    
    data = asyncio.run(get_data_for_cec_user())
    StatisticData.objects.update_or_create(
        name='Dashboard_data_for_CEC',
        defaults={'data': data},
    )

    url = url_name(__file__)
    response = cec_client.post(url)
    inventory_units = InventoryUnit.objects.all().count()

    assert response.status_code == 200
    assert response.json()['cec_user']
    if for_loop_times > 0:
        assert response.json()['cec_user']['Total'][0]['product_name'] == inventory_unit.product.name_uz
        assert response.json()['cec_user']['Total'][0]['inventory_count'] == inventory_units
        assert response.json()['cec_user']['Total'][0]['inventory_count'] == for_loop_times


@pytest.mark.parametrize(
    "for_loop_times",
    [(0), (1), (5)],
)
@pytest.mark.django_db(transaction=True)
def test_data_region(for_loop_times, region_client, url_name, inventory_unit_factory, responsible_person_factory, district_factory, region_user):
    region = region_user.region
    district = district_factory.create(region=region)
    for _ in range(for_loop_times):
        responsible_person = responsible_person_factory.create(district=district)
        inventory_unit = inventory_unit_factory.create(district=district)

    data = asyncio.run(get_data_for_region_user(region.id))
    StatisticData.objects.update_or_create(
        name=f"Dashboard_data_for_region_{region.id}",
        defaults={"data": data},
    )

    url = url_name(__file__)
    response = region_client.post(url)
    inventory_units = InventoryUnit.objects.all().count()

    assert response.status_code == 200
    if for_loop_times > 0:
        assert response.json()['region_user']['products'][0]['responsible_persons'][0]['first_name'] == responsible_person.first_name
        assert response.json()['region_user']['Total'][0]['product_name'] == inventory_unit.product.name_uz
        assert response.json()['region_user']['Total'][0]['inventory_count'] == inventory_units
        assert response.json()['region_user']['Total'][0]['inventory_count'] == for_loop_times


@pytest.mark.parametrize(
    "for_loop_times",
    [(0), (1), (5)],
)
@pytest.mark.django_db(transaction=True)
def test_data_district(
    for_loop_times, 
    district_client, 
    url_name, 
    inventory_unit_factory, 
    responsible_person_factory,
    district_user,
    storage_place_factory
    ):
    district = district_user.district
    address = storage_place_factory.create(district=district)

    for _ in range(for_loop_times):
        responsible_person = responsible_person_factory.create(district=district)
        inventory_unit = inventory_unit_factory.create(storage_place=address, district=district)

    data = asyncio.run(get_data_for_district_user(district.id))
    StatisticData.objects.update_or_create(
        name=f"Dashboard_data_for_district_{district.id}",
        defaults={"data": data},
    )
    
    url = url_name(__file__)
    response = district_client.post(url)
    inventory_units = InventoryUnit.objects.all().count()

    assert response.status_code == 200
    if for_loop_times > 0:
        assert response.json()['district_user']['responsible_persons'][0]['first_name'] == responsible_person.first_name
        assert response.json()['district_user']['storage_place_products'][0]['address'] == address.address
        assert response.json()['district_user']['Total'][0]['product_name'] == inventory_unit.product.name_uz
        assert response.json()['district_user']['Total'][0]['inventory_count'] == inventory_units
        assert response.json()['district_user']['Total'][0]['inventory_count'] == for_loop_times
