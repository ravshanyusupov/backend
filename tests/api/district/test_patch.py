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
def test_patch_district(
    user_client_string, url_name_string, status_code, district_factory, request
):
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    district = district_factory.create()
    payload = {
        "id": district.id,
        "name_uz": "some_name_uz",
        "name_ru": "some_name_ru",
        "region_id": district.region.id,
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
def test_patch_district_data(
    payload, url_name, cec_client, district_factory, region_factory
):
    district = district_factory.create()
    region = region_factory.create()
    payload.update({"id": district.id, "region_id": region.id})

    response = cec_client.post(url_name(__file__), payload)

    assert response.status_code == 200
    if payload["name_uz"] == "   some_name_uz    ":
        assert response.json()["name_uz"] == "some_name_uz"
        assert response.json()["name_ru"] == "some_name_ru"
    else:
        assert response.json()["name_uz"] == payload["name_uz"]
        assert response.json()["name_ru"] == payload["name_ru"]
        assert response.json()["region"]["name_uz"] == region.name_uz
        assert response.json()["region"]["name_ru"] == region.name_ru


@pytest.mark.django_db(transaction=True)
def test_patch_district_non_exists_region(
    url_name, cec_client, district_factory, region_factory
):
    district = district_factory.create()
    region = region_factory.create()
    payload = {
        "id": district.id,
        "name_uz": "some_name_uz",
        "name_ru": "some_name_ru",
        "region_id": region.id + 1,
    }
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 400
