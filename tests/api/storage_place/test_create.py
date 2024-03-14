import pytest
from tests.faker import fake


@pytest.mark.parametrize(
    "auth_client_str, url_name_str, payload_str,status_code, code",
    [
        ("district_client", "url_name", "SUCCESS", 201, None),
        (
            "district_client",
            "url_name",
            "FIELD_REQUIRED_DISTRICT",
            400,
            "missing",
        ),
        (
            "district_client",
            "url_name",
            "ATTEMPTING_TO_CREATE_STORAGE_PLACE_FOR_ANOTHER_DISTRICT",
            403,
            3001,
        ),
        ("region_client", "url_name", "PERMISSION_DENIED", 403, 1000),
    ],
)
@pytest.mark.django_db
def test_create(
    request,
    auth_client_str,
    url_name_str,
    payload_str,
    status_code,
    code,
    create_payload,
):
    auth_client = request.getfixturevalue(auth_client_str)
    url_name = request.getfixturevalue(url_name_str)
    payload = create_payload[payload_str]

    url = url_name(__file__)

    response = auth_client.post(url, payload)

    if code:
        assert response.json()[0]["code"] == code
    assert response.status_code == status_code


@pytest.fixture
def create_payload(district_user, district_factory, building_category_factory):
    building_category = building_category_factory.create(
        name_uz=fake.name(), name_ru=fake.name()
    )
    district = district_factory.create(name_uz=fake.name(), name_ru=fake.name())

    PAYLOAD = {
        "SUCCESS": {
            "building_category_id": building_category.id,
            "district_id": district_user.district_id,
            "address": fake.address(),
        },
        "FIELD_REQUIRED_DISTRICT": {
            "building_category_id": building_category.id,
            "address": fake.address(),
        },
        "ATTEMPTING_TO_CREATE_STORAGE_PLACE_FOR_ANOTHER_DISTRICT": {
            "building_category_id": building_category.id,
            "district_id": district.id,
            "address": fake.address(),
        },
        "PERMISSION_DENIED": {
            "building_category_id": building_category.id,
            "district_id": district.id,
            "address": fake.address(),
        },
    }

    return PAYLOAD
