import pytest
from tests.fixtures.core import APIClient


@pytest.mark.parametrize(
    "client_str, result_length",
    [
        ("cec_client", 50),
        ("cec_client", 100),
        ("cec_client", 1),
        ("cec_client", 0),
    ],
)
@pytest.mark.django_db
def test_list_responsible_person(
    responsible_person_factory, url_name, client_str, result_length, request
):
    responsible_person_factory.create_batch(result_length)
    url = url_name(__file__)
    client = request.getfixturevalue(client_str)
    response = client.post(url)
    result = response.json()

    assert response.status_code == 200
    assert len(result) == result_length


@pytest.mark.django_db
def test_list_responsible_person_for_region(
    url_name,
    responsible_person_factory,
    region_user_factory,
    client,
):
    user = region_user_factory.create()
    user.set_password(region_user_factory.password)
    user.raw_password = region_user_factory.password
    user.save()
    payload = dict(
        username=user.username,
        password=user.raw_password,
    )
    responsible_person_factory.create_batch(20)
    for _ in range(10):
        responsible_person_factory.create(region=user.region)
    response = client.post("/api/users/login/", payload)
    auth_client = APIClient(
        headers={"Authorization": f"Bearer {response.json()['access']}"}
    )

    response = auth_client.post(url_name(__file__))
    assert response.status_code == 200
    assert len(response.json()) == 10


@pytest.mark.django_db
def test_list_responsible_person_for_district(
    url_name,
    responsible_person_factory,
    district_user_factory,
    client,
):
    user = district_user_factory.create()
    user.set_password(district_user_factory.password)
    user.raw_password = district_user_factory.password
    user.save()
    payload = dict(
        username=user.username,
        password=user.raw_password,
    )
    responsible_person_factory.create_batch(20)
    for _ in range(15):
        responsible_person_factory.create(region=user.region, district=user.district)
    response = client.post("/api/users/login/", payload)
    auth_client = APIClient(
        headers={"Authorization": f"Bearer {response.json()['access']}"}
    )

    response = auth_client.post(url_name(__file__))
    assert response.status_code == 200
    assert len(response.json()) == 15
