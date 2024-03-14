import pytest
from tests.faker import fake


@pytest.mark.parametrize(
    "auth_client_str, url_name_str, payload_str,status_code, code",
    [
        ("district_client", "url_name", "SUCCESS", 200, None),
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
            "ATTEMPTING_TO_UPDATE_STORAGE_PLACE_FOR_ANOTHER_DISTRICT",
            403,
            3001,
        ),
        ("region_client", "url_name", "PERMISSION_DENIED", 403, 1000),
    ],
)
@pytest.mark.django_db
def test_patch(
    request,
    auth_client_str,
    url_name_str,
    payload_str,
    status_code,
    code,
    patch_payload,
):
    auth_client = request.getfixturevalue(auth_client_str)
    url_name = request.getfixturevalue(url_name_str)
    payload = patch_payload[payload_str]

    url = url_name(__file__)

    response = auth_client.post(url, payload)

    if code:
        assert response.json()[0]["code"] == code
    assert response.status_code == status_code


@pytest.fixture
def patch_payload(district_user, building_category_factory, storage_place_factory):
    building_category = building_category_factory.create()
    storage_place_1 = storage_place_factory.create(
        district_id=district_user.district_id
    )
    storage_place_2 = storage_place_factory.create()

    PAYLOAD = {
        "SUCCESS": {
            "id": storage_place_1.id,
            "building_category_id": building_category.id,
            "address": fake.address(),
        },
        "FIELD_REQUIRED_DISTRICT": {
            "building_category_id": building_category.id,
            "address": fake.address(),
        },
        "ATTEMPTING_TO_UPDATE_STORAGE_PLACE_FOR_ANOTHER_DISTRICT": {
            "id": storage_place_2.id,
            "building_category_id": building_category.id,
            "address": fake.address(),
        },
        "PERMISSION_DENIED": {
            "id": storage_place_1.id,
            "building_category_id": building_category.id,
            "address": fake.address(),
        },
    }

    return PAYLOAD
