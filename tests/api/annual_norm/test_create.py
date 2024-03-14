import pytest


@pytest.mark.parametrize(
    "auth_client, user, payload_str, status_code, code",
    [
        ("cec_client", "CEC", "SUCCESS", 201, None),
        (
            "cec_client",
            "CEC",
            "ATTEMPTING_TO_CREATE_ANNUAL_NORM_FOR_DISTRICT_PRODUCT_NORM",
            403,
            4011,
        ),
        ("region_client", "REGION", "SUCCESS", 201, None),
    ],
)
@pytest.mark.django_db
def test_create(
    request, auth_client, user, payload_str, status_code, code, url_name, data
):
    client = request.getfixturevalue(auth_client)
    url = url_name(__file__)
    payload = data[user][payload_str]

    response = client.post(url, payload)

    if code:
        assert response.json()[0]["code"] == code
    assert response.status_code == status_code


@pytest.fixture
def data(product_norm_region, product_norm_district, year):
    DATA = {
        "CEC": {
            "SUCCESS": [
                {
                    "product_norm_id": product_norm_region.id,
                    "year_id": year.id,
                    "count": 1000,
                }
            ],
            "ATTEMPTING_TO_CREATE_ANNUAL_NORM_FOR_DISTRICT_PRODUCT_NORM": [
                {
                    "product_norm_id": product_norm_district.id,
                    "year_id": year.id,
                    "count": 1000,
                }
            ],
        },
        "REGION": {
            "SUCCESS": [
                {
                    "product_norm_id": product_norm_district.id,
                    "year_id": year.id,
                    "count": 1000,
                }
            ],
            "ATTEMPTING_TO_CREATE_ANNUAL_NORM_FOR_REGION_PRODUCT_NORM": [
                {
                    "product_norm_id": product_norm_region.id,
                    "year_id": year.id,
                    "count": 1000,
                }
            ],
        },
    }

    return DATA
