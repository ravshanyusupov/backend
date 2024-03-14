import pytest


@pytest.mark.parametrize(
    "auth_client_str, url_name_str, filters, status_code, total",
    [
        ("cec_client", "url_name", "FILTER_1", 200, 0),
        ("cec_client", "url_name", "NONE", 200, 4),
        ("region_client", "url_name", "FILTER_2", 200, 1),
        ("region_client", "url_name", "NONE", 200, 2),
        ("district_client", "url_name", "NONE", 200, 1),
        ("district_client", "url_name", "FILTER_2", 200, 0),
    ],
)
@pytest.mark.django_db
def test_list(
    request, auth_client_str, url_name_str, filters, status_code, total, list_payload
):
    auth_client = request.getfixturevalue(auth_client_str)
    url_name = request.getfixturevalue(url_name_str)
    filter_arg = list_payload[filters]

    url = url_name(__file__)
    url = url + filter_arg

    response = auth_client.post(url)

    assert response.json()["total"] == total
    assert response.status_code == status_code


@pytest.fixture
def list_payload(
    district_user,
    region_user,
    district_factory,
    storage_place_factory,
    building_category_factory,
):
    district_1 = district_factory.create(region_id=region_user.region_id)
    district_2 = district_factory.create(region_id=region_user.region_id)

    building_category = building_category_factory.create(
        name_uz="Школа", name_ru="Maktab"
    )

    storage_place_1 = storage_place_factory.create(
        district_id=district_1.id, building_category_id=building_category.id
    )
    storage_place_2 = storage_place_factory.create(district_id=district_2.id)
    storage_place_3 = storage_place_factory.create()
    storage_place_4 = storage_place_factory.create(
        district_id=district_user.district_id
    )

    filter_payload = {
        "FILTER_1": "?building_category_id=100",
        "NONE": "",
        "FILTER_2": f"?building_category_id={building_category.id}",
    }

    return filter_payload
