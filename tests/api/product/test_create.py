import pytest


@pytest.mark.parametrize(
    "auth_client, payload_str, status_code, code",
    [
        ("cec_client", "SUCCESS", 201, None),
        ("cec_client", "FIELD_REQUIRED", 400, "missing"),
        ("region_client", "SUCCESS", 403, 1000),
    ],
)
@pytest.mark.django_db
def test_create(
    request, auth_client, payload_str, status_code, code, create_payload, url_name
):
    client = request.getfixturevalue(auth_client)
    payload = create_payload[payload_str]
    url = url_name(__file__)
    response = client.post(url, payload)

    if code:
        assert response.json()[0]["code"] == code
    assert response.status_code == status_code


@pytest.fixture
def create_payload(fake_category):
    PAYLOAD = {
        "SUCCESS": {
            "category_id": fake_category.id,
            "name_uz": "Bayroq",
        },
        "FIELD_REQUIRED": {"name_ru": "Флаг"},
    }

    return PAYLOAD
