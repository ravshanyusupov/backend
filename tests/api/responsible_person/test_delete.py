import pytest
from tests.fixtures.core import APIClient


@pytest.mark.parametrize(
    "user_client_string, url_name_string, status_code",
    [
        ("district_client", "url_name", 403),
        ("region_client", "url_name", 403),
        ("cec_client", "url_name", 403),
        ("client", "url_name", 401),
    ],
)
@pytest.mark.django_db
def test_delete_responsible_person_fail(
    responsible_person_factory,
    request,
    user_client_string,
    url_name_string,
    status_code,
):
    responsible_person = responsible_person_factory.create()

    payload = {"id": responsible_person.id}
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    response = user_client.post(url_name(__file__), payload)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_delete_responsible_person_success(
    responsible_person_patch_delete_access,
    url_name,
):
    auth_client = responsible_person_patch_delete_access["auth_client"]
    responsible_person_data = responsible_person_patch_delete_access[
        "responsible_person_data"
    ]
    payload = {"id": responsible_person_data["id"]}
    response = auth_client.post(url_name(__file__), payload)
    assert response.status_code == 204
