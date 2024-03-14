import pytest
import datetime


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
def test_get_responsible_person(
    responsible_person_factory,
    user_client_string,
    url_name_string,
    status_code,
    request,
):
    responsible_person = responsible_person_factory.create()

    payload = {"id": responsible_person.id}
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    response = user_client.post(url_name(__file__), payload)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_get_unavailable_responsible_person(
    cec_client, url_name, responsible_person_factory
):
    responsible_person = responsible_person_factory.create()
    non_exists_id = responsible_person.id + 1
    payload = {"id": non_exists_id}
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_responsible_person_data(
    responsible_person_factory,
    cec_client,
    url_name,
):
    responsible_person = responsible_person_factory.create()

    payload = {"id": responsible_person.id}
    response = cec_client.post(url_name(__file__), payload)
    response_data = response.json()
    date_of_order = datetime.datetime.strptime(
        response_data["date_of_order"], "%Y-%m-%dT%H:%M:%S"
    )
    assert response_data["first_name"] == responsible_person.first_name
    assert response_data["last_name"] == responsible_person.last_name
    assert response_data["middle_name"] == responsible_person.middle_name
    assert response_data["phone_number"] == responsible_person.phone_number
    assert response_data["work_place"] == responsible_person.work_place
    assert response_data["passport_serial"] == responsible_person.passport_serial
    assert response_data["job_title"] == responsible_person.job_title
    assert response_data["order"] == responsible_person.order
    assert response_data["region"]["id"] == responsible_person.region.id
    assert response_data["district"]["id"] == responsible_person.district.id
    assert date_of_order == responsible_person.date_of_order
