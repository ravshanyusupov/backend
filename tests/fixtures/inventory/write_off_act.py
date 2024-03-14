import pytest
from tests.faker import fake
from tests.fixtures import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def write_off_act_district_client(
    district_user_factory, write_off_act_factory, client, example_file
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

    write_off_act_factory.create_batch(20, district=user.district, file=example_file)
    return auth_client


@pytest.fixture
def write_off_act_region_client(
    region_user_factory, write_off_act_factory, client, example_file
):
    user = region_user_factory.create()
    user.set_password(region_user_factory.password)
    user.raw_password = region_user_factory.password
    user.save()
    payload = dict(
        username=user.username,
        password=user.raw_password,
    )
    response = client.post("/api/users/login/", payload)
    auth_client = APIClient(
        headers={"Authorization": f"Bearer {response.json()['access']}"}
    )
    write_off_act_factory.create_batch(40, region=user.region, file=example_file)
    return auth_client


@pytest.fixture
def write_off_act_data_for_region(
    region_user_factory, write_off_act_factory, client, example_file
):
    user = region_user_factory.create()
    user.set_password(region_user_factory.password)
    user.raw_password = region_user_factory.password
    user.save()
    payload = dict(
        username=user.username,
        password=user.raw_password,
    )

    response = client.post("/api/users/login/", payload)
    auth_client = APIClient(
        headers={"Authorization": f"Bearer {response.json()['access']}"}
    )

    instance = write_off_act_factory.create(region=user.region, file=example_file)
    return {"auth_client": auth_client, "instance": instance}


@pytest.fixture
def write_off_act_data_for_district(
    district_user_factory, write_off_act_factory, client, example_file
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

    instance = write_off_act_factory.create(district=user.district, file=example_file)
    return {"auth_client": auth_client, "instance": instance}


@pytest.fixture
def write_off_act_create_data(inventory_unit_factory, example_file):
    inventory_units = inventory_unit_factory.create_batch(5)
    inventory_numbers = []
    for inventory_unit in inventory_units:
        inventory_numbers.append(inventory_unit.inventory_number)

    payload = {
        "inventory_numbers": inventory_numbers,
        "name_uz": "akt 12221",
        "file": example_file,
    }
    return payload


@pytest.fixture
def example_file():
    file = SimpleUploadedFile(
        "file.pdf", b"file_content", content_type="application/pdf"
    )
    return file
