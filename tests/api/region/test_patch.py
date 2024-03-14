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
def test_patch_region(
    user_client_string, url_name_string, status_code, region_factory, request
):
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    region = region_factory.create()
    payload = {
        "id": region.id,
        "name_uz": "some_name_uz",
        "name_ru": "some_name_ru",
        "precincts_count": 5,
    }
    response = user_client.post(url_name(__file__), payload)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_patch_region_data(url_name, cec_client, region_factory):
    region = region_factory.create()
    payload = {
        "id": region.id,
        "name_ru": "some_name_ru",
        "precincts_count": 5,
    }
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 200
    assert response.json()["name_uz"] == region.name_uz
    assert response.json()["name_ru"] == payload["name_ru"]
    assert response.json()["precincts_count"] == payload["precincts_count"]


@pytest.mark.parametrize(
    "count",
    [0, -1, 32768],
)
@pytest.mark.django_db
def test_patch_region_invalid_precincts_count(url_name, cec_client, region_factory, count):
    region = region_factory.create()
    payload = {
        "id": region.id,
        "precincts_count": count,
    }
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 400
