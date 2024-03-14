import datetime
import pytest
from tests.faker import fake


@pytest.mark.parametrize(
    "user_client_string, url_name_string, status_code",
    [
        ("district_client", "url_name", 201),
        ("region_client", "url_name", 403),
        ("cec_client", "url_name", 403),
        ("client", "url_name", 401),
    ],
)
@pytest.mark.django_db
def test_create_responsible_person_status(
    request, user_client_string, url_name_string, status_code, responsible_person_data
):
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    response = user_client.post(url_name(__file__), responsible_person_data)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_create_responsible_person_data(
    district_client, url_name, responsible_person_data
):
    response = district_client.post(url_name(__file__), responsible_person_data)
    response_data = response.json()
    response_date_of_order = datetime.datetime.strptime(
        response_data["date_of_order"], "%Y-%m-%dT%H:%M:%S"
    )
    payload_date_of_order = datetime.datetime.strptime(
        responsible_person_data["date_of_order"], "%Y-%m-%d %H:%M:%S"
    )
    assert response.status_code == 201
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
def test_create_responsible_person_missing_data(
    district_client,
    url_name,
):
    payload = {"first_name": "Some name"}
    response = district_client.post(url_name(__file__), payload)
    assert response.status_code == 400
    assert response.json()[0]["code"] == "missing"


@pytest.mark.django_db
def test_create_responsible_with_exceding_max_length_data(
    district_client, url_name, responsible_person_data
):
    responsible_person_data["order"] = "Some long string that exceeds limit of max_length for order which is 20 str length"
    response = district_client.post(url_name(__file__), responsible_person_data)

    assert response.status_code == 400
    assert response.json()[0]["code"] == "string_too_long"


@pytest.mark.django_db
def test_create_responsible_with_space_data(
    district_client, url_name, responsible_person_data
):
    responsible_person_data["first_name"] = "     Ilhom Xusanov    "
    response = district_client.post(url_name(__file__), responsible_person_data)

    assert response.status_code == 201
    assert response.json()["first_name"] == "Ilhom Xusanov"
