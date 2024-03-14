import pytest


@pytest.mark.parametrize(
    "auth_client, user, payload, status_code, code",
    [
        ("cec_client", "CEC", "SUCCESS", 201, None),
        ("cec_client", "CEC", "FIELD_REQUIRED", 400, "missing"),
        (
            "cec_client",
            "CEC",
            "ATTEMPTING_TO_CREATE_PRODUCT_NORM_FOR_REGION",
            400,
            4006,
        ),
        ("region_client", "REGION", "SUCCESS", 201, None),
        ("region_client", "REGION", "FIELD_REQUIRED", 400, 4008),
        (
            "region_client",
            "REGION",
            "ATTEMPTING_TO_CREATE_PRODUCT_NORM_FOR_OTHER_REGION",
            403,
            4007,
        ),
        (
            "region_client",
            "REGION",
            "ATTEMPTING_TO_CREATE_PRODUCT_NORM_FOR_DISTRICT_OF_OTHER_REGION",
            403,
            4009,
        ),
        ("district_client", "DISTRICT", "PERMISSION_DENIED", 403, 1000),
    ],
)
@pytest.mark.django_db
def test_create(
    request, auth_client, user, payload, status_code, code, url_name, create_payload
):
    client = request.getfixturevalue(auth_client)
    url = url_name(__file__)
    payload = create_payload[user][payload]

    response = client.post(url, payload)

    assert response.status_code == status_code
    if code:
        assert response.json()[0]["code"] == code


@pytest.fixture
def create_payload(product, district, region, region_user, district_factory, year):
    district_for_region_user = district_factory.create(region=region_user.region)

    payload = {
        "CEC": {
            "SUCCESS": {
                "product_id": product.id,
                "region_id": region.id,
                "annual_norms": [{"year_id": year.id, "count": 1000}],
            },
            "FIELD_REQUIRED": {
                "product_id": product.id,
                "count": 1000,
            },
            "ATTEMPTING_TO_CREATE_PRODUCT_NORM_FOR_REGION": {
                "product_id": product.id,
                "region_id": region.id,
                "district_id": district.id,
                "annual_norms": [{"year_id": year.id, "count": 1000}],
            },
        },
        "REGION": {
            "SUCCESS": {
                "product_id": product.id,
                "region_id": region_user.region_id,
                "district_id": district_for_region_user.id,
                "annual_norms": [{"year_id": year.id, "count": 1000}],
            },
            "FIELD_REQUIRED": {
                "product_id": product.id,
                "region_id": region_user.region_id,
                "annual_norms": [{"year_id": year.id, "count": 1000}],
            },
            "ATTEMPTING_TO_CREATE_PRODUCT_NORM_FOR_OTHER_REGION": {
                "product_id": product.id,
                "region_id": region.id,
                "district_id": district_for_region_user.id,
                "annual_norms": [{"year_id": year.id, "count": 1000}],
            },
            "ATTEMPTING_TO_CREATE_PRODUCT_NORM_FOR_DISTRICT_OF_OTHER_REGION": {
                "product_id": product.id,
                "region_id": region_user.region_id,
                "district_id": district.id,
                "annual_norms": [{"year_id": year.id, "count": 1000}],
            },
        },
        "DISTRICT": {
            "PERMISSION_DENIED": {
                "product_id": product.id,
                "region_id": region_user.region_id,
                "district_id": district_for_region_user.id,
                "annual_norms": [{"year_id": year.id, "count": 1000}],
            }
        },
    }

    return payload
