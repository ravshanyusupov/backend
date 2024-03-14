import pytest


@pytest.mark.parametrize(
    "user_client_string, url_name_string, status_code",
    [
        ("cec_client", "url_name", 200),
        ("region_client", "url_name", 200),
        ("district_client", "url_name", 200),
        ("client", "url_name", 401),
    ],
)
@pytest.mark.django_db
def test_get_category_building(
    user_client_string, url_name_string, status_code, request, building_category_factory
):
    building_category = building_category_factory.create()

    payload = {"id": building_category.id}
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    response = user_client.post(url_name(__file__), payload)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_get_unavailable_building_category(
    cec_client, url_name, building_category_factory
):
    building_category = building_category_factory.create()
    non_exists_id = building_category.id + 1
    payload = {"id": non_exists_id}
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 404
