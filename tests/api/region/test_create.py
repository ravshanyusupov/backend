import pytest


@pytest.mark.parametrize(
    "user_client_string, url_name_string, status_code",
    [
        ("cec_client", "url_name", 201),
        ("region_client", "url_name", 403),
        ("district_client", "url_name", 403),
        ("client", "url_name", 401),
    ],
)
@pytest.mark.django_db
def test_create_region_status(
    request, user_client_string, url_name_string, status_code
):
    payload = {"name_uz": "Toshkent viloyati"}
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    response = user_client.post(url_name(__file__), payload)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_create_region_data(cec_client, url_name):
    payload = {"name_uz": "Toshkent viloyati", "name_ru": "Ташкентская область", "precincts_count": 5}
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 201
    assert response.json()["name_uz"] == payload["name_uz"]
    assert response.json()["name_ru"] == payload["name_ru"]
    assert response.json()["precincts_count"] == payload["precincts_count"]


@pytest.mark.django_db
def test_create_region_default_precincts_count(cec_client, url_name):
    payload = {"name_uz": "Toshkent viloyati", "name_ru": "Ташкентская область"}
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 201
    assert response.json()["name_uz"] == payload["name_uz"]
    assert response.json()["name_ru"] == payload["name_ru"]
    assert response.json()["precincts_count"] == 0


@pytest.mark.parametrize(
    "count",
    [0, -1, 32768],
)
@pytest.mark.django_db
def test_create_region_out_invalid_precinct_count(cec_client, url_name, count):
    payload = {"name_uz": "Toshkent viloyati", "name_ru": "Ташкентская область", "precincts_count": count}
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 400
