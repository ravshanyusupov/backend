import pytest
from tests.faker import fake


@pytest.mark.parametrize(
    "auth_client_str, url_name_str, payload_str,status_code, code",
    [
        ("district_client", "url_name", "SUCCESS", 204, None),
        (
            "district_client",
            "url_name",
            "ATTEMPTING_TO_DELETE_STORAGE_PLACE_FOR_ANOTHER_DISTRICT",
            403,
            3001,
        ),
        ("region_client", "url_name", "PERMISSION_DENIED", 403, 1000),
    ],
)
@pytest.mark.django_db
def test_delete(
    request,
    auth_client_str,
    url_name_str,
    payload_str,
    status_code,
    code,
    delete_payload,
):
    auth_client = request.getfixturevalue(auth_client_str)
    url_name = request.getfixturevalue(url_name_str)
    payload = delete_payload[payload_str]

    url = url_name(__file__)

    response = auth_client.post(url, payload)

    if code:
        assert response.json()[0]["code"] == code
    assert response.status_code == status_code


@pytest.fixture
def delete_payload(district_user, storage_place_factory):
    storage_place_1 = storage_place_factory.create(
        district_id=district_user.district_id
    )
    storage_place_2 = storage_place_factory.create()

    PAYLOAD = {
        "SUCCESS": {
            "id": storage_place_1.id,
        },
        "ATTEMPTING_TO_DELETE_STORAGE_PLACE_FOR_ANOTHER_DISTRICT": {
            "id": storage_place_2.id,
        },
        "PERMISSION_DENIED": {
            "id": storage_place_1.id,
        },
    }

    return PAYLOAD
