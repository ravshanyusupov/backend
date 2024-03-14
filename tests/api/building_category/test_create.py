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
def test_create_category_building(
    request, user_client_string, url_name_string, status_code
):
    payload = {"name_uz": "Davlat bayrog'i"}
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    response = user_client.post(url_name(__file__), payload)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "payload",
    [
        {"name_uz": "Davlat bayrog'i", "name_ru": "Государственный флаг"},
        {"name_uz": "    Maktab    ", "name_ru": "Школа    "},
    ],
)
@pytest.mark.django_db
def test_create_category_building_data(payload, cec_client, url_name):
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 201
    if payload["name_uz"] == "    Maktab    ":
        assert response.json()["name_uz"] == "Maktab"
        assert response.json()["name_ru"] == "Школа"
    else:
        assert response.json()["name_uz"] == payload["name_uz"]
        assert response.json()["name_ru"] == payload["name_ru"]
