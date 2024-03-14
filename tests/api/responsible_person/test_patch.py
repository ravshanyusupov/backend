import datetime
import pytest
from tests.faker import fake
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
def test_patch_responsible_person_fail(
    user_client_string,
    url_name_string,
    status_code,
    responsible_person_data,
    responsible_person_factory,
    request,
):
    responsible_person = responsible_person_factory.create()
    responsible_person_data.update({"id": responsible_person.id})
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)

    response = user_client.post(url_name(__file__), responsible_person_data)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_patch_responsible_person_data_success(
    url_name, responsible_person_patch_delete_access
):
    auth_client = responsible_person_patch_delete_access["auth_client"]
    responsible_person_data = responsible_person_patch_delete_access[
        "responsible_person_data"
    ]

    response = auth_client.post(url_name(__file__), responsible_person_data)
    response_data = response.json()
    response_date_of_order = datetime.datetime.strptime(
        response_data["date_of_order"], "%Y-%m-%dT%H:%M:%S"
    )
    payload_date_of_order = datetime.datetime.strptime(
        responsible_person_data["date_of_order"], "%Y-%m-%d %H:%M:%S"
    )
    assert response.status_code == 200
    assert response_data["first_name"] == responsible_person_data["first_name"]
    assert response_data["last_name"] == responsible_person_data["last_name"]
    assert response_data["middle_name"] == responsible_person_data["middle_name"]
    assert response_data["phone_number"] == responsible_person_data["phone_number"]
    assert response_data["work_place"] == responsible_person_data["work_place"]
    assert (
        response_data["passport_serial"] == responsible_person_data["passport_serial"]
    )
    assert response_data["job_title"] == responsible_person_data["job_title"]
    assert response_data["order"] == responsible_person_data["order"]
    assert response_date_of_order == payload_date_of_order


@pytest.mark.django_db
def test_patch_responsible_person_data_success_with_data_with_space(
    url_name, responsible_person_patch_delete_access
):
    auth_client = responsible_person_patch_delete_access["auth_client"]
    responsible_person_data = responsible_person_patch_delete_access[
        "responsible_person_data"
    ]
    responsible_person_data["first_name"] = "    Ilhom Xusanov    "
    response = auth_client.post(url_name(__file__), responsible_person_data)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["first_name"] == "Ilhom Xusanov"
