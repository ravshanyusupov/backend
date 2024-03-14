import pytest

from tests.faker import fake


@pytest.mark.parametrize(
    "auth, url, user_type_1, user_type_2, status_code, code",
    [
        ("cec_client", "url_name", "CEC_USER", "REGION_USER", 200, None),
        ("cec_client", "url_name", "CEC_USER", "DISTRICT_USER", 200, None),
        ("cec_client", "url_name", "CEC_USER", "SELF", 200, None),
        (
            "region_client",
            "url_name",
            "REGION_USER",
            "READING_OTHER_REGION_OR_CEC",
            403,
            2003,
        ),
        ("region_client", "url_name", "REGION_USER", "REGION_USER", 200, None),
        (
            "region_client",
            "url_name",
            "REGION_USER",
            "INVALID_DISTRICT_FOR_REGION",
            403,
            2003,
        ),
        ("region_client", "url_name", "REGION_USER", "DISTRICT_USER", 200, None),
        ("region_client", "url_name", "REGION_USER", "SELF", 200, None),
        ("district_client", "url_name", "DISTRICT_USER", "SELF", 200, None),
        (
            "district_client",
            "url_name",
            "DISTRICT_USER",
            "ATTEMPTING_TO_ACCESS_DATA_OF_ANOTHER_USER",
            403,
            2005,
        ),
    ],
)
@pytest.mark.django_db
def test_read(
    request, auth, url, user_type_1, user_type_2, status_code, code, read_payload
):
    auth_client = request.getfixturevalue(auth)
    url_name = request.getfixturevalue(url)
    payload = read_payload[user_type_1][user_type_2]

    url = url_name(__file__)
    response = auth_client.post(url, payload)

    if code:
        assert response.json()[0]["code"] == code
    assert response.status_code == status_code


@pytest.fixture
def read_payload(
    cec_user,
    region_user,
    district_user,
    district_factory,
    district_user_factory,
    region_user_factory,
):
    district = district_factory.create(
        name_uz=fake.name(), name_ru=fake.name(), region_id=region_user.region_id
    )
    region_user_1 = region_user_factory.create(
        username=fake.name(), user_type="R", region_id=region_user.region_id
    )
    region_user_2 = region_user_factory.create(username=fake.name(), user_type="R")
    district_user_1 = district_user_factory.create(
        username=fake.name(),
        password=fake.password(),
        user_type="D",
        region_id=district.region_id,
        district_id=district.id,
    )
    payload = {
        "CEC_USER": {
            "REGION_USER": dict(id=region_user.id),
            "DISTRICT_USER": dict(id=district_user.id),
            "SELF": dict(id=cec_user.id),
        },
        "REGION_USER": {
            "READING_OTHER_REGION_OR_CEC": dict(id=region_user_2.id),
            "REGION_USER": dict(id=region_user_1.id),
            "INVALID_DISTRICT_FOR_REGION": dict(id=district_user.id),
            "DISTRICT_USER": dict(id=district_user_1.id),
            "SELF": dict(id=region_user.id),
        },
        "DISTRICT_USER": {
            "SELF": dict(id=district_user.id),
            "ATTEMPTING_TO_ACCESS_DATA_OF_ANOTHER_USER": dict(id=district_user_1.id),
        },
    }

    return payload
