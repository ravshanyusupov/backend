import pytest


@pytest.mark.parametrize(
    "auth_client, user, payload, status_code, code",
    [
        ("cec_client", "CEC", "SUCCESS", 200, None),
        (
            "cec_client",
            "CEC",
            "ATTEMPTING_TO_UPDATE_PRODUCT_NORM_FOR_DISTRICT",
            403,
            4011,
        ),
        ("region_client", "REGION", "SUCCESS", 200, None),
        (
            "region_client",
            "REGION",
            "ATTEMPTING_TO_UPDATE_PRODUCT_NORM_FOR_REGION",
            403,
            4011,
        ),
        (
            "region_client",
            "REGION",
            "ATTEMPTING_TO_UPDATE_PRODUCT_NORM_FOR_DISTRICT_OF_OTHER_REGION",
            403,
            4011,
        ),
        ("district_client", "DISTRICT", "PERMISSION_DENIED", 403, 1000),
    ],
)
@pytest.mark.django_db
def test_patch(
    request, auth_client, user, payload, status_code, code, url_name, patch_payload
):
    client = request.getfixturevalue(auth_client)
    url = url_name(__file__)
    payload = patch_payload[user][payload]

    response = client.post(url, payload)

    assert response.status_code == status_code
    if code:
        assert response.json()[0]["code"] == code


@pytest.fixture
def patch_payload(
    product_norm_district,
    product_norm_region,
    region_user,
    product_norm_factory,
    district_user,
    district_factory,
):
    district_for_region_user = district_factory.create(region=region_user.region)
    district_product_norm_for_region_user = product_norm_factory.create(
        district=district_for_region_user, region=district_for_region_user.region
    )
    region_product_norm = product_norm_factory.create(
        district=None, region=region_user.region
    )
    district_product_norm = product_norm_factory.create(district=district_user.district)

    payload = {
        "CEC": {
            "SUCCESS": {
                "id": product_norm_region.id,
                "region_id": region_user.region_id,
            },
            "ATTEMPTING_TO_UPDATE_PRODUCT_NORM_FOR_DISTRICT": {
                "id": district_product_norm.id,
            },
        },
        "REGION": {
            "SUCCESS": {
                "id": district_product_norm_for_region_user.id,
            },
            "ATTEMPTING_TO_UPDATE_PRODUCT_NORM_FOR_REGION": {
                "id": region_product_norm.id,
            },
            "ATTEMPTING_TO_UPDATE_PRODUCT_NORM_FOR_DISTRICT_OF_OTHER_REGION": {
                "id": district_product_norm.id,
            },
        },
        "DISTRICT": {
            "PERMISSION_DENIED": {
                "id": district_product_norm.id,
            },
        },
    }

    return payload
