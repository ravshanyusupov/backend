import pytest


@pytest.mark.parametrize(
    "client_str, result_length, filter, total",
    [
        ("cec_client", 50, None, 50),
        ("cec_client", 100, "?search=Tashkent", 0),
        ("region_client", 30, "?search=Toshkent", 1),
        ("district_client", 2, "?search=Ташкент", 1),
    ],
)
@pytest.mark.django_db
def test_list_category_building(
    region_factory,
    url_name,
    client_str,
    result_length,
    request,
    filter,
    total,
):
    region_factory.create_batch(result_length)
    url = url_name(__file__)
    if filter:
        region_factory.create(name_uz="Toshkent", name_ru="Ташкент")
        url += filter
    client = request.getfixturevalue(client_str)
    response = client.post(url)
    result = response.json()

    assert response.status_code == 200
    assert len(result) == total
