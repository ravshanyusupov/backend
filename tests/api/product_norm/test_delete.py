import pytest


@pytest.mark.parametrize(
    "auth_client, user, payload, status_code, code",
    [
        ("cec_client", "CEC", "SUCCESS", 204, None),
        (
            "cec_client",
            "CEC",
            "ATTEMPTING_TO_DELETE_PRODUCT_NORM_FOR_DISTRICT",
            403,
            4011,
        ),
        ("region_client", "REGION", "SUCCESS", 204, None),
        (
            "region_client",
            "REGION",
            "ATTEMPTING_TO_DELETE_PRODUCT_NORM_FOR_REGION",
            403,
            4011,
        ),
        (
            "region_client",
            "REGION",
            "ATTEMPTING_TO_DELETE_PRODUCT_NORM_FOR_DISTRICT_OF_ANOTHER_REGION",
            403,
            4011,
        ),
        ("district_client", "DISTRICT", "PERMISSION_DENIED", 403, 1000),
    ],
)
@pytest.mark.django_db()
def test_delete(
    request, auth_client, user, payload, status_code, code, url_name, delete_payload
):
    client = request.getfixturevalue(auth_client)
    url = url_name(__file__)
    payload = delete_payload[user][payload]

    response = client.post(url, payload)

    assert response.status_code == status_code
    if code:
        assert response.json()[0]["code"] == code


@pytest.fixture()
def delete_payload(
    product_norm_region,
    product_norm_district,
    region_user,
    product_norm_factory,
    district_factory,
):
    district = district_factory.create(region_id=region_user.region_id)
    product_norm = product_norm_factory.create(
        region_id=region_user.region_id, district_id=district.id
    )

    payload = {
        "CEC": {
            "SUCCESS": {"id": product_norm_region.id},
            "ATTEMPTING_TO_DELETE_PRODUCT_NORM_FOR_DISTRICT": {"id": product_norm.id},
        },
        "REGION": {
            "SUCCESS": {"id": product_norm.id},
            "ATTEMPTING_TO_DELETE_PRODUCT_NORM_FOR_REGION": {
                "id": product_norm_region.id
            },
            "ATTEMPTING_TO_DELETE_PRODUCT_NORM_FOR_DISTRICT_OF_ANOTHER_REGION": {
                "id": product_norm_district.id
            },
        },
        "DISTRICT": {"PERMISSION_DENIED": {"id": product_norm.id}},
    }

    return payload
