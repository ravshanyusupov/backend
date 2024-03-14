import pytest


@pytest.mark.parametrize(
    "auth_client, filter, total",
    [
        ("cec_client", "NONE", 4),
        ("cec_client", "FILTER-1", 1),
        ("region_client", "NONE", 2),
        ("region_client", "FILTER-2", 1),
        ("district_client", "NONE", 1),
    ],
)
@pytest.mark.django_db
def test_list(request, auth_client, filter, total, url_name, list_payload):
    client = request.getfixturevalue(auth_client)
    url = url_name(__file__)

    response = client.post(url + list_payload[filter])

    assert response.json()["total"] == total


@pytest.fixture
def list_payload(
    product_norm_district,
    product_norm_region,
    region_user,
    product_norm_factory,
    district_user,
):
    product_norm_factory.create(district=None, region=region_user.region)
    product_norm_factory.create(district=district_user.district)

    filters = {
        "NONE": "",
        "FILTER-1": f"?region_id={product_norm_region.region_id}",
        "FILTER-2": f"?district_id={product_norm_district.district_id}",
    }

    return filters
