import pytest


@pytest.mark.parametrize(
    "user_client_string, url_name_string, status_code",
    [
        ("cec_client", "url_name", 200),
        ("region_client", "url_name", 403),
        ("district_client", "url_name", 403),
        ("client", "url_name", 401),
    ],
)
@pytest.mark.django_db
def test_patch_category_building(
    user_client_string, url_name_string, status_code, building_category_factory, request
):
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    building_category = building_category_factory.create()
    payload = {
        "id": building_category.id,
        "name_uz": "some_name_uz",
        "name_ru": "some_name_ru",
    }
    response = user_client.post(url_name(__file__), payload)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "payload",
    [
        {"name_uz": "some_name_uz", "name_ru": "some_name_ru"},
        {"name_uz": "   some_name_uz    ", "name_ru": "   some_name_ru"},
    ],
)
@pytest.mark.django_db
def test_patch_category_building_data(
    payload, url_name, cec_client, building_category_factory
):
    building_category = building_category_factory.create()
    payload.update({"id": building_category.id})
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 200
    if payload["name_uz"] == "   some_name_uz    ":
        assert response.json()["name_uz"] == "some_name_uz"
        assert response.json()["name_ru"] == "some_name_ru"
    else:
        assert response.json()["name_uz"] == payload["name_uz"]
        assert response.json()["name_ru"] == payload["name_ru"]
