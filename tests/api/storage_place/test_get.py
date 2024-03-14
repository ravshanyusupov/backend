import pytest


@pytest.mark.parametrize(
    "auth_client_str, url_name_str, user_type, payload_str,status_code, code",
    [
        ("cec_client", "url_name", "CEC_USER", "SUCCESS", 200, None),
        ("cec_client", "url_name", "CEC_USER", "NOT_FOUND", 404, 1002),
        ("region_client", "url_name", "REGION_USER", "SUCCESS_1", 200, None),
        ("region_client", "url_name", "REGION_USER", "SUCCESS_2", 200, None),
        (
            "region_client",
            "url_name",
            "REGION_USER",
            "ATTEMPTING_TO_GET_STORAGE_PLACE_OF_ANOTHER_REGION",
            403,
            3001,
        ),
        ("district_client", "url_name", "DISTRICT_USER", "SUCCESS", 200, None),
        (
            "district_client",
            "url_name",
            "DISTRICT_USER",
            "ATTEMPTING_TO_GET_STORAGE_PLACE_OF_ANOTHER_DISTRICT",
            403,
            3001,
        ),
    ],
)
@pytest.mark.django_db
def test_get(
    request,
    auth_client_str,
    url_name_str,
    user_type,
    payload_str,
    status_code,
    code,
    get_payload,
):
    auth_client = request.getfixturevalue(auth_client_str)
    url_name = request.getfixturevalue(url_name_str)
    payload = get_payload[user_type][payload_str]

    url = url_name(__file__)

    response = auth_client.post(url, payload)

    if code:
        assert response.json()[0]["code"] == code
    assert response.status_code == status_code


@pytest.fixture
def get_payload(district_user, region_user, district_factory, storage_place_factory):
    district_1 = district_factory.create(region_id=region_user.region_id)
    district_2 = district_factory.create(region_id=region_user.region_id)

    storage_place_1 = storage_place_factory.create(district_id=district_1.id)
    storage_place_2 = storage_place_factory.create(district_id=district_2.id)
    storage_place_3 = storage_place_factory.create()
    storage_place_4 = storage_place_factory.create(
        district_id=district_user.district_id
    )

    PAYLOAD = {
        "CEC_USER": {
            "SUCCESS": {"id": storage_place_1.id},
            "NOT_FOUND": {"id": 100},
        },
        "REGION_USER": {
            "SUCCESS_1": {"id": storage_place_1.id},
            "SUCCESS_2": {"id": storage_place_2.id},
            "ATTEMPTING_TO_GET_STORAGE_PLACE_OF_ANOTHER_REGION": {
                "id": storage_place_3.id
            },
        },
        "DISTRICT_USER": {
            "SUCCESS": {"id": storage_place_4.id},
            "ATTEMPTING_TO_GET_STORAGE_PLACE_OF_ANOTHER_DISTRICT": {
                "id": storage_place_3.id
            },
        },
    }

    return PAYLOAD
