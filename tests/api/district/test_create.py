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
def test_create_district(
    request, user_client_string, url_name_string, status_code, region_factory
):
    region = region_factory.create()
    payload = {
        "name_uz": "Shayxontohur tumani",
        "name_ru": "Шайхантахурский район",
        "region_id": region.id,
    }
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    response = user_client.post(url_name(__file__), payload)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "payload",
    [
        {"name_uz": "Shayxontohur tumani", "name_ru": "Шайхантахурский район"},
        {"name_uz": "  Shayxontohur tumani  ", "name_ru": "Шайхантахурский район  "},
    ],
)
@pytest.mark.django_db
def test_create_district_data(payload, cec_client, url_name, region_factory):
    region = region_factory.create()
    payload.update({"region_id": region.id})

    response = cec_client.post(url_name(__file__), payload)

    assert response.status_code == 201
    if payload["name_uz"] == "  Shayxontohur tumani  ":
        assert response.json()["name_uz"] == "Shayxontohur tumani"
        assert response.json()["name_ru"] == "Шайхантахурский район"
    else:
        assert response.json()["name_uz"] == payload["name_uz"]
        assert response.json()["name_ru"] == payload["name_ru"]
        assert response.json()["region"]["name_uz"] == region.name_uz
        assert response.json()["region"]["name_ru"] == region.name_ru


@pytest.mark.django_db(transaction=True)
def test_create_district_for_non_exists_region(region_factory, cec_client, url_name):
    region = region_factory.create()
    payload = {
        "name_uz": "Shayxontohur tumani",
        "name_ru": "Шайхантахурский район",
        "region_id": region.id + 1,
    }
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 400
