import pytest


@pytest.mark.parametrize(
    "auth_client, user, payload, status_code, code",
    [
        ("cec_client", "CEC", "SUCCESS", 204, None),
        (
            "cec_client",
            "CEC",
            "ATTEMPTING_TO_DELETE_ANNUAL_NORM_FOR_DISTRICT_PRODUCT_NORM",
            403,
            4011,
        ),
        ("region_client", "REGION", "SUCCESS", 204, None),
        (
            "region_client",
            "REGION",
            "ATTEMPTING_TO_DELETE_ANNUAL_NORM_FOR_REGION_PRODUCT_NORM",
            403,
            4011,
        ),
    ],
)
@pytest.mark.django_db
def test_delete(request, auth_client, user, payload, status_code, code, url_name, data):
    client = request.getfixturevalue(auth_client)
    url = url_name(__file__)
    payload = data[user][payload]

    response = client.post(url, payload)
    if code:
        assert response.json()[0]["code"] == code
    assert response.status_code == status_code


@pytest.fixture
def data(annual_norm_for_district_product_norm, annual_norm_for_region_product_norm):
    DATA = {
        "CEC": {
            "SUCCESS": {"id": annual_norm_for_region_product_norm.id},
            "ATTEMPTING_TO_DELETE_ANNUAL_NORM_FOR_DISTRICT_PRODUCT_NORM": {
                "id": annual_norm_for_district_product_norm.id
            },
        },
        "REGION": {
            "SUCCESS": {"id": annual_norm_for_district_product_norm.id},
            "ATTEMPTING_TO_DELETE_ANNUAL_NORM_FOR_REGION_PRODUCT_NORM": {
                "id": annual_norm_for_region_product_norm.id
            },
        },
    }

    return DATA
