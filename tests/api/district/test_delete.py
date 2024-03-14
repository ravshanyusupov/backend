import pytest


@pytest.mark.parametrize(
    "user_client_string, url_name_string, status_code",
    [
        ("cec_client", "url_name", 204),
        ("region_client", "url_name", 403),
        ("district_client", "url_name", 403),
        ("client", "url_name", 401),
    ],
)
@pytest.mark.django_db
def test_delete_district(
    district_factory, request, user_client_string, url_name_string, status_code
):
    district = district_factory.create()

    payload = {"id": district.id}
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    response = user_client.post(url_name(__file__), payload)
    assert response.status_code == status_code
