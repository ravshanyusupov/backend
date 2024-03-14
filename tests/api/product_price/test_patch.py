import pytest


@pytest.mark.parametrize(
    "auth_client, payload_str, status_code, code",
    [
        ("cec_client", "SUCCESS", 200, None),
        ("cec_client", "FIELD_REQUIRED", 400, "missing"),
        ("region_client", "SUCCESS", 403, 1000),
    ],
)
@pytest.mark.django_db
def test_patch(
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
def create_payload(product_price, year):
    PAYLOAD = {
        "SUCCESS": {
            "id": product_price.id,
            "year_id": year.id,
            "price": 100000,
        },
        "FIELD_REQUIRED": {"year_id": 2023},
    }

    return PAYLOAD
