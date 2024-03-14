import pytest
from tests.faker import fake


@pytest.mark.parametrize(
    "auth_client_str, url_name_str, update_user, updated_user, status_code, code",
    [
        ("cec_client", "url_name", "CEC_USER", "SELF", 200, None),
        ("cec_client", "url_name", "CEC_USER", "REGION_USER", 200, None),
        ("cec_client", "url_name", "CEC_USER", "DISTRICT_USER", 200, None),
        (
            "cec_client",
            "url_name",
            "CEC_USER",
            "INCORRECT_FIELDS_PROVIDED_FOR_REGION_USER",
            422,
            2000,
        ),
        (
            "cec_client",
            "url_name",
            "CEC_USER",
            "INCORRECT_FIELDS_PROVIDED_FOR_DISTRICT_USER",
            422,
            2000,
        ),
        (
            "cec_client",
            "url_name",
            "CEC_USER",
            "INVALID_DISTRICT_FOR_REGION",
            422,
            2001,
        ),
        ("cec_client", "url_name", "CEC_USER", "EMPTY_PASSWORD_PROVIDED", 400, 2007),
        ("cec_client", "url_name", "CEC_USER", "NO_DIGIT_PASSWORD_PROVIDED", 400, 2008),
        ("cec_client", "url_name", "CEC_USER", "NO_LOWER_CASE_PASSWORD_PROVIDED", 400, 2009),
        ("cec_client", "url_name", "CEC_USER", "NO_UPPER_CASE_PASSWORD_PROVIDED", 400, 2010),
        ("cec_client", "url_name", "CEC_USER", "NO_SPECIAL_CHARACTER_PASSWORD_PROVIDED", 400, 2011),
        (
            "region_client",
            "url_name",
            "REGION_USER",
            "INVALID_USER_ACCESS_LEVEL_PROVIDED",
            403,
            2002,
        ),
        (
            "region_client",
            "url_name",
            "REGION_USER",
            "PROVIDED_REGION_DOES_NOT_MATCH_YOUR_REGION",
            403,
            2003,
        ),
        ("region_client", "url_name", "REGION_USER", "SELF", 200, None),
        ("region_client", "url_name", "REGION_USER", "DISTRICT_USER", 200, None),
        ("district_client", "url_name", "DISTRICT_USER", "SELF", 200, None),
        (
            "district_client",
            "url_name",
            "DISTRICT_USER",
            "ATTEMPTING_TO_MODIFY_ANOTHER_USER",
            403,
            2005,
        ),
    ],
)
@pytest.mark.django_db
def test_update(
    request,
    auth_client_str,
    url_name_str,
    update_user,
    updated_user,
    status_code,
    code,
    update_payload,
):
    auth_client = request.getfixturevalue(auth_client_str)
    url_name = request.getfixturevalue(url_name_str)
    payload = update_payload[update_user][updated_user]

    url = url_name(__file__)
    response = auth_client.post(url, payload)
    if code:
        assert response.json()[0]["code"] == code

    assert response.status_code == status_code


@pytest.fixture
def update_payload(
    cec_user,
    region_user,
    district_user,
    region_factory,
    district_factory,
    region_user_factory,
    district_user_factory,
):
    region_1 = region_factory.create(name_uz=fake.name(), name_ru=fake.name())
    region_user_1 = region_user_factory.create(
        username=fake.name(), password=fake.password(), region=region_1, user_type="R"
    )
    district_1 = district_factory.create(
        name_uz=fake.name(), name_ru=fake.name(), region=region_1
    )
    district_2 = district_factory.create(
        name_uz=fake.name(), name_ru=fake.name(), region_id=region_user.region_id
    )
    district_user_2 = district_user_factory.create(
        username=fake.name(),
        password=fake.password(),
        region_id=district_2.region_id,
        district_id=district_2.id,
    )
    payload = {
        "CEC_USER": {
            "SELF": {"id": cec_user.id, "username": fake.name(), "user_type": "C"},
            "REGION_USER": {
                "id": region_user.id,
                "username": fake.name(),
                "user_type": "R",
                "region_id": region_1.id,
                "password": fake.password(),
            },
            "DISTRICT_USER": {
                "id": district_user.id,
                "username": fake.name(),
                "user_type": "R",
                "region_id": region_1.id,
                "password": fake.password(),
            },
            "INCORRECT_FIELDS_PROVIDED_FOR_REGION_USER": {
                "id": region_user.id,
                "username": fake.name(),
                "user_type": "R",
                "password": fake.password(),
                "region_id": region_1.id,
                "district_id": district_user.district_id,
            },
            "INCORRECT_FIELDS_PROVIDED_FOR_DISTRICT_USER": {
                "id": region_user.id,
                "username": fake.name(),
                "user_type": "D",
                "password": fake.password(),
                "district_id": district_user.district_id,
            },
            "INVALID_DISTRICT_FOR_REGION": {
                "id": region_user.id,
                "username": fake.name(),
                "user_type": "D",
                "password": fake.password(),
                "region_id": region_user.region_id,
                "district_id": district_1.id,
            },
            "EMPTY_PASSWORD_PROVIDED": {
                "id": cec_user.id,
                "username": fake.name(),
                "user_type": "C",
                "password": "",
            },
            "NO_DIGIT_PASSWORD_PROVIDED": {
                "id": cec_user.id,
                "username": fake.name(),
                "user_type": "C",
                "password": "qWert$yz",
            },
            "NO_LOWER_CASE_PASSWORD_PROVIDED": {
                "id": cec_user.id,
                "username": fake.name(),
                "user_type": "C",
                "password": "1234A$AA",
            },
            "NO_UPPER_CASE_PASSWORD_PROVIDED": {
                "id": cec_user.id,
                "username": fake.name(),
                "user_type": "C",
                "password": "1234a$aa",
            },
            "NO_SPECIAL_CHARACTER_PASSWORD_PROVIDED": {
                "id": cec_user.id,
                "username": fake.name(),
                "user_type": "C",
                "password": "1234aAaa",
            },
        },
        "REGION_USER": {
            "INVALID_USER_ACCESS_LEVEL_PROVIDED": {
                "id": region_user.id,
                "username": fake.name(),
                "user_type": "C",
                "password": fake.password(),
            },
            "PROVIDED_REGION_DOES_NOT_MATCH_YOUR_REGION": {
                "id": region_user_1.id,
                "username": fake.name(),
                "user_type": "R",
                "password": fake.password(),
                "region_id": region_1.id,
            },
            "SELF": {
                "id": region_user.id,
                "username": fake.name(),
                "user_type": "D",
                "password": fake.password(),
                "region_id": region_user.region.id,
                "district_id": district_2.id,
            },
            "DISTRICT_USER": {
                "id": district_user_2.id,
                "username": fake.name(),
                "user_type": "D",
                "password": fake.password(),
                "region_id": region_user.region.id,
                "district_id": district_user_2.district_id,
            },
        },
        "DISTRICT_USER": {
            "SELF": {
                "id": district_user.id,
                "username": fake.name(),
                "user_type": "D",
                "password": fake.password(),
                "region_id": district_user.region.id,
                "district_id": district_user.district_id,
            },
            "ATTEMPTING_TO_MODIFY_ANOTHER_USER": {
                "id": district_user_2.id,
                "username": fake.name(),
                "user_type": "D",
                "password": fake.password(),
                "region_id": district_user.region.id,
                "district_id": district_user.district_id,
            },
        },
    }
    return payload
