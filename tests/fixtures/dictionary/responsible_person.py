import pytest
from tests.faker import fake
from tests.fixtures import APIClient


@pytest.fixture
def responsible_person_data():
    payload = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "middle_name": fake.first_name(),
        "phone_number": "+9989700000000",
        "work_place": fake.job(),
        "passport_serial": fake.passport_number(),
        "job_title": fake.name(),
        "order": str(fake.pyint()),
        "date_of_order": str(fake.date_time()),
    }

    return payload


@pytest.fixture
def responsible_person_patch_delete_access(
    responsible_person_factory,
    district_user_factory,
    responsible_person_data,
    client,
):
    responsible_person = responsible_person_factory.create()
    user = district_user_factory.create(
        username=district_user_factory.username,
        user_type=district_user_factory.user_type,
        region=responsible_person.region,
        district=responsible_person.district,
    )
    user.set_password(district_user_factory.password)
    user.raw_password = district_user_factory.password
    user.save()
    payload = dict(
        username=user.username,
        password=user.raw_password,
    )
    responsible_person_data.update({"id": responsible_person.id})

    response = client.post("/api/users/login/", payload)
    auth_client = APIClient(
        headers={"Authorization": f"Bearer {response.json()['access']}"}
    )

    return {
        "responsible_person_data": responsible_person_data,
        "auth_client": auth_client,
    }
