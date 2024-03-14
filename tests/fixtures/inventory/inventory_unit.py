import pytest
from tests.faker import fake
from tests.fixtures import APIClient


@pytest.fixture
def inventory_unit_create_data(
    district_user_factory,
    product_factory,
    storage_place_factory,
    inventory_unit_factory,
    client,
):
    product = product_factory.create()
    storage_place = storage_place_factory.create()
    user = district_user_factory.create(
        username=district_user_factory.username,
        user_type=district_user_factory.user_type,
        region=storage_place.district.region,
        district=storage_place.district,
    )
    user.set_password(district_user_factory.password)
    user.raw_password = district_user_factory.password
    user.save()
    payload = dict(
        username=user.username,
        password=user.raw_password,
    )

    response = client.post("/api/users/login/", payload)
    auth_client = APIClient(
        headers={"Authorization": f"Bearer {response.json()['access']}"}
    )
    inventory_unit = inventory_unit_factory.create(district=user.district)
    inventory_unit_2 = inventory_unit_factory.create(district=user.district)
    inventory_unit_data = {
        "id": inventory_unit.id,
        "product_id": product.id,
        "storage_place_id": storage_place.id,
        "district_id": user.district_id,
        "commissioning_year": 2020,
        "inventory_number": "121212121233",
    }

    return {
        "inventory_unit_data": inventory_unit_data,
        "auth_client": auth_client,
        "inventory_unit": inventory_unit,
        "inventory_unit_2": inventory_unit_2,
    }


@pytest.fixture
def inventory_unit_district_client(
    district_user_factory, inventory_unit_factory, client
):
    user = district_user_factory.create()
    user.set_password(district_user_factory.password)
    user.raw_password = district_user_factory.password
    user.save()
    payload = dict(
        username=user.username,
        password=user.raw_password,
    )

    response = client.post("/api/users/login/", payload)
    auth_client = APIClient(
        headers={"Authorization": f"Bearer {response.json()['access']}"}
    )
    for _ in range(20):
        inventory_unit_factory.create(district=user.district)
    return auth_client


@pytest.fixture
def inventory_unit_region_client(
    region_user_factory, inventory_unit_factory, district_factory, client
):
    user = region_user_factory.create()
    user.set_password(region_user_factory.password)
    user.raw_password = region_user_factory.password
    user.save()
    district = district_factory.create(region=user.region)
    payload = dict(
        username=user.username,
        password=user.raw_password,
    )

    response = client.post("/api/users/login/", payload)
    auth_client = APIClient(
        headers={"Authorization": f"Bearer {response.json()['access']}"}
    )
    for _ in range(40):
        inventory_unit_factory.create(district=district)
    return auth_client
