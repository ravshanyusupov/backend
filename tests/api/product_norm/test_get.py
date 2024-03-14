import pytest


@pytest.mark.parametrize(
    "auth_client, user, payload, status_code, code",
    [
        ("cec_client", "CEC", "SUCCESS_1", 200, None),
        ("cec_client", "CEC", "SUCCESS_2", 200, None),
        ("region_client", "REGION", "SELF", 200, None),
        ("region_client", "REGION", "SUCCESS", 200, None),
        (
            "region_client",
            "REGION",
            "ATTEMPTING_TO_READ_PRODUCT_NORM_FOR_OTHER_REGION",
            403,
            4007,
        ),
        (
            "region_client",
            "REGION",
            "ATTEMPTING_TO_READ_PRODUCT_NORM_FOR_DISTRICT_OF_OTHER_REGION",
            403,
            4007,
        ),
        ("district_client", "DISTRICT", "SELF", 200, None),
        (
            "district_client",
            "DISTRICT",
            "ATTEMPTING_TO_READ_PRODUCT_NORM_FOR_REGION",
            403,
            4010,
        ),
        (
            "district_client",
            "DISTRICT",
            "ATTEMPTING_TO_READ_PRODUCT_NORM_FOR_OTHER_DISTRICT",
            403,
            4010,
        ),
    ],
)
@pytest.mark.django_db
def test_get(
    request, auth_client, user, payload, status_code, code, url_name, get_payload
):
    client = request.getfixturevalue(auth_client)
    url = url_name(__file__)
    payload = get_payload[user][payload]

    response = client.post(url, payload)

    assert response.status_code == status_code
    if code:
        assert response.json()[0]["code"] == code


@pytest.fixture
def get_payload(
    product_norm_district,
    product_norm_region,
    region_user,
    product_norm_factory,
    district_user,
):
    region_product_norm = product_norm_factory.create(
        district=None, region=region_user.region
    )
    district_product_norm = product_norm_factory.create(district=district_user.district)

    payload = {
        "CEC": {
            "SUCCESS_1": {"id": product_norm_region.id},
            "SUCCESS_2": {"id": product_norm_district.id},
        },
        "REGION": {
            "SELF": {"id": region_product_norm.id},
            "SUCCESS": {"id": product_norm_district.id},
            "ATTEMPTING_TO_READ_PRODUCT_NORM_FOR_OTHER_REGION": {
                "id": product_norm_region.id
            },
            "ATTEMPTING_TO_READ_PRODUCT_NORM_FOR_DISTRICT_OF_OTHER_REGION": {
                "id": district_product_norm.id
            },
        },
        "DISTRICT": {
            "SELF": {"id": district_product_norm.id},
            "ATTEMPTING_TO_READ_PRODUCT_NORM_FOR_REGION": {
                "id": product_norm_region.id
            },
            "ATTEMPTING_TO_READ_PRODUCT_NORM_FOR_OTHER_DISTRICT": {
                "id": product_norm_district.id
            },
        },
    }

    return payload
