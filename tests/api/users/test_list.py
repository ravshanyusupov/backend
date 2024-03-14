import pytest
from tests.faker import fake


@pytest.mark.parametrize(
    "client_str, url_name_str, status_code, length",
    [
        ("cec_client", "url_name", 200, 10),
        ("region_client", "url_name", 200, 5),
        ("district_client", "url_name", 200, 2),
    ],
)
@pytest.mark.django_db
def test_list(request, client_str, url_name_str, status_code, length, list_payload):
    clint = request.getfixturevalue(client_str)
    url_name = request.getfixturevalue(url_name_str)

    url = url_name(__file__)
    response = clint.post(url)

    assert response.status_code == status_code
    assert len(response.json()["items"]) == length


@pytest.fixture
def list_payload(
    region_factory,
    district_factory,
    cec_user_factory,
    region_user_factory,
    district_user_factory,
    region_user,
    district_user,
):
    region_1 = region_factory.create(name_uz=fake.name(), name_ru=fake.name())

    district_1 = district_factory.create(
        name_uz=fake.name(), name_ru=fake.name(), region_id=region_user.region_id
    )
    district_2 = district_factory.create(
        name_uz=fake.name(), name_ru=fake.name(), region_id=region_user.region_id
    )
    district_3 = district_factory.create(
        name_uz=fake.name(), name_ru=fake.name(), region_id=region_1.id
    )

    cec_user_1 = cec_user_factory.create(
        username=fake.name(), user_type="C", password=fake.password()
    )

    region_user_1 = region_user_factory.create(
        username=fake.name(),
        user_type="R",
        password=fake.password(),
        region_id=region_user.region_id,
    )
    region_user_2 = region_user_factory.create(
        username=fake.name(),
        user_type="R",
        password=fake.password(),
        region_id=region_1.id,
    )

    district_user_1 = district_user_factory.create(
        username=fake.name(),
        user_type="D",
        password=fake.password(),
        region_id=region_user.region_id,
        district_id=district_1.id,
    )
    district_user_2 = district_user_factory.create(
        username=fake.name(),
        user_type="D",
        password=fake.password(),
        region_id=region_user.region_id,
        district_id=district_1.id,
    )
    district_user_3 = district_user_factory.create(
        username=fake.name(),
        user_type="D",
        password=fake.password(),
        region_id=region_user.region_id,
        district_id=district_2.id,
    )
    district_user_4 = district_user_factory.create(
        username=fake.name(),
        user_type="D",
        password=fake.password(),
        region_id=region_1.id,
        district_id=district_3.id,
    )
    district_user_4 = district_user_factory.create(
        username=fake.name(),
        user_type="D",
        password=fake.password(),
        region_id=region_1.id,
        district_id=district_user.district_id,
    )
