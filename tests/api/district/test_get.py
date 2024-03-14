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
def test_get_district(
    user_client_string, url_name_string, status_code, district_factory, request
):
    district = district_factory.create()

    payload = {"id": district.id}
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    response = user_client.post(url_name(__file__), payload)

    assert response.status_code == status_code


@pytest.mark.django_db
def test_get_unavailable_district(cec_client, url_name, district_factory):
    district = district_factory.create()
    non_exists_id = district.id + 1
    payload = {"id": non_exists_id}
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 404
