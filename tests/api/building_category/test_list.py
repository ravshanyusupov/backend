import pytest


@pytest.mark.parametrize(
    "client_str, result_length, filter, total",
    [
        ("cec_client", 50, None, 50),
        ("region_client", 100, None, 100),
        ("region_client", 100, "?search=Maktab", 1),
        ("region_client", 100, "?search=Школа", 1),
        ("district_client", 0, None, 0),
    ],
)
@pytest.mark.django_db
def test_list_category_building(
    building_category_factory,
    url_name,
    client_str,
    result_length,
    request,
    filter,
    total,
):
    building_category_factory.create_batch(result_length)
    url = url_name(__file__)
    if filter:
        building_category_factory.create(name_uz="Maktab", name_ru="Школа")
        url += filter
    client = request.getfixturevalue(client_str)
    response = client.post(url)
    result = response.json()

    assert response.status_code == 200
    assert len(result) == total
