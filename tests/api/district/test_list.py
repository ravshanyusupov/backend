import pytest


@pytest.mark.parametrize(
    "client_str, result_length, filter, total",
    [
        ("cec_client", 50, None, 50),
        ("region_client", 100, None, 100),
        ("cec_client", 100, "?search=Shayhontoxur", 1),
        ("region_client", 100, "?search=Шайхонтохур", 1),
    ],
)
@pytest.mark.django_db
def test_list_district(
    district_factory,
    url_name,
    client_str,
    result_length,
    request,
    filter,
    total,
):
    url = url_name(__file__)
    if filter:
        district_factory.create(name_uz="Shayhontoxur", name_ru="Шайхонтохур")
        url += filter
    district_factory.create_batch(result_length)
    client = request.getfixturevalue(client_str)
    response = client.post(url)
    result = response.json()
    assert response.status_code == 200
    assert len(result) == total
