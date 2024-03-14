import pytest
from tests.faker import fake


@pytest.mark.parametrize(
    "auth_client_str, url_name_str, create_user, status_code, code",
    [
        ("cec_client", "url_name", "CEC_USER", 201, None),
        ("cec_client", "url_name", "REGION_USER", 201, None),
        (
            "cec_client",
            "url_name",
            "INCORRECT_FIELDS_PROVIDED_FOR_REGION_USER",
            422,
            2000,
        ),
        ("cec_client", "url_name", "DISTRICT_USER", 201, None),
        ("cec_client", "url_name", "INVALID_DISTRICT_FOR_REGION", 422, 2001),
        ("cec_client", "url_name", "EMPTY_PASSWORD_PROVIDED", 400, 2007),
        ("cec_client", "url_name", "NO_DIGIT_PASSWORD_PROVIDED", 400, 2008),
        ("cec_client", "url_name", "NO_LOWER_CASE_PASSWORD_PROVIDED", 400, 2009),
        ("cec_client", "url_name", "NO_UPPER_CASE_PASSWORD_PROVIDED", 400, 2010),
        ("cec_client", "url_name", "NO_SPECIAL_CHARACTER_PASSWORD_PROVIDED", 400, 2011),
        (
            "cec_client",
            "url_name",
            "INCORRECT_FIELDS_PROVIDED_FOR_DISTRICT_USER",
            422,
            2000,
        ),
    ],
)
@pytest.mark.django_db
def test_cec_create(
    request,
    auth_client_str,
    url_name_str,
    create_user,
    status_code,
    code,
    cec_create_payload,
):
    auth_client = request.getfixturevalue(auth_client_str)
    url_name = request.getfixturevalue(url_name_str)
    payload = cec_create_payload[create_user]

    url = url_name(__file__)
    response = auth_client.post(url, payload)
    if code:
        assert response.json()[0]["code"] == code
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "auth_client_str, url_name_str, payload, status_code, code",
    [
        ("region_client", "url_name", "INVALID_USER_ACCESS_LEVEL_PROVIDED", 403, 2002),
        ("region_client", "url_name", "REGION_USER", 201, None),
        (
            "region_client",
            "url_name",
            "PROVIDED_REGION_DOES_NOT_MATCH_YOUR_REGION",
            403,
            2003,
        ),
        ("region_client", "url_name", "DISTRICT_USER", 201, None),
        ("region_client", "url_name", "INVALID_DISTRICT_FOR_REGION", 422, 2001),
        (
            "region_client",
            "url_name",
            "INCORRECT_FIELDS_PROVIDED_FOR_DISTRICT_USER",
            422,
            2000,
        ),
    ],
)
@pytest.mark.django_db
def test_region_create(
    request,
    auth_client_str,
    url_name_str,
    payload,
    status_code,
    code,
    region_create_payload,
):
    auth_client = request.getfixturevalue(auth_client_str)
    url_name = request.getfixturevalue(url_name_str)
    payload = region_create_payload[payload]

    url = url_name(__file__)
    response = auth_client.post(url, payload)

    if code:
        assert response.json()[0]["code"] == code
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "auth_client_str, url_name_str, payload, status_code, code",
    [
        (
            "district_client",
            "url_name",
            "INVALID_USER_ACCESS_LEVEL_PROVIDED",
            403,
            2002,
        ),
        ("district_client", "url_name", "DISTRICT_USER", 201, None),
        (
            "district_client",
            "url_name",
            "INCORRECT_FIELDS_PROVIDED_FOR_DISTRICT_USER",
            403,
            2004,
        ),
    ],
)
@pytest.mark.django_db
def test_district_create(
    request,
    auth_client_str,
    url_name_str,
    payload,
    status_code,
    code,
    district_create_payload,
):
    auth_client = request.getfixturevalue(auth_client_str)
    url_name = request.getfixturevalue(url_name_str)
    payload = district_create_payload[payload]
    url = url_name(__file__)
    response = auth_client.post(url, payload)

    if code:
        assert response.json()[0]["code"] == code
    assert response.status_code == status_code


@pytest.fixture
def cec_create_payload(region_factory, district_factory):
    region_1 = region_factory.build()
    region_1.save()
    district_1 = district_factory.create(
        name_ru=fake.name(), name_uz=fake.name(), region=region_1
    )

    region_2 = region_factory.build()
    region_2.save()
    district_2 = district_factory.create(
        name_ru=fake.name(), name_uz=fake.name(), region=region_2
    )

    payload = {
        "CEC_USER": {
            "username": fake.name(),
            "user_type": "C",
            "password": fake.password(),
        },
        "REGION_USER": {
            "username": fake.name(),
            "user_type": "R",
            "password": fake.password(),
            "region_id": region_1.id,
        },
        "INCORRECT_FIELDS_PROVIDED_FOR_REGION_USER": {
            "username": fake.name(),
            "user_type": "R",
            "password": fake.password(),
            "region_id": region_1.id,
            "district_id": district_1.id,
        },
        "DISTRICT_USER": {
            "username": fake.name(),
            "user_type": "D",
            "password": fake.password(),
            "region_id": region_1.id,
            "district_id": district_1.id,
        },
        "INVALID_DISTRICT_FOR_REGION": {
            "username": fake.name(),
            "user_type": "D",
            "password": fake.password(),
            "region_id": region_1.id,
            "district_id": district_2.id,
        },
        "INCORRECT_FIELDS_PROVIDED_FOR_DISTRICT_USER": {
            "username": fake.name(),
            "user_type": "D",
            "password": fake.password(),
            "region_id": region_1.id,
        },
        "EMPTY_PASSWORD_PROVIDED": {
            "username": fake.name(),
            "user_type": "C",
            "password": "",
        },
        "NO_DIGIT_PASSWORD_PROVIDED": {
            "username": fake.name(),
            "user_type": "C",
            "password": "qWert$yz",
        },
        "NO_LOWER_CASE_PASSWORD_PROVIDED": {
            "username": fake.name(),
            "user_type": "C",
            "password": "1234A$AA",
        },
        "NO_UPPER_CASE_PASSWORD_PROVIDED": {
            "username": fake.name(),
            "user_type": "C",
            "password": "1234a$aa",
        },
        "NO_SPECIAL_CHARACTER_PASSWORD_PROVIDED": {
            "username": fake.name(),
            "user_type": "C",
            "password": "1234aAaa",
        },
    }
    return payload


@pytest.fixture
def region_create_payload(region_factory, district_factory, region_user):
    region_1 = region_factory.build()
    region_1.save()

    district_1 = district_factory.create(
        name_ru=fake.name(), name_uz=fake.name(), region=region_user.region
    )
    district_2 = district_factory.create(
        name_ru=fake.name(), name_uz=fake.name(), region=region_1
    )

    payload = {
        "INVALID_USER_ACCESS_LEVEL_PROVIDED": {
            "username": fake.name(),
            "user_type": "C",
            "password": fake.password(),
        },
        "REGION_USER": {
            "username": fake.name(),
            "user_type": "R",
            "password": fake.password(),
            "region_id": region_user.region.id,
        },
        "PROVIDED_REGION_DOES_NOT_MATCH_YOUR_REGION": {
            "username": fake.name(),
            "user_type": "R",
            "password": fake.password(),
            "region_id": region_1.id,
        },
        "DISTRICT_USER": {
            "username": fake.name(),
            "user_type": "D",
            "password": fake.password(),
            "region_id": region_user.region_id,
            "district_id": district_1.id,
        },
        "INVALID_DISTRICT_FOR_REGION": {
            "username": fake.name(),
            "user_type": "D",
            "password": fake.password(),
            "region_id": region_user.region_id,
            "district_id": district_2.id,
        },
        "INCORRECT_FIELDS_PROVIDED_FOR_DISTRICT_USER": {
            "username": fake.name(),
            "user_type": "D",
            "password": fake.password(),
            "region_id": region_1.id,
        },
    }
    return payload


@pytest.fixture
def district_create_payload(district_user):
    payload = {
        "INVALID_USER_ACCESS_LEVEL_PROVIDED": {
            "username": fake.name(),
            "user_type": "C",
            "password": fake.password(),
        },
        "DISTRICT_USER": {
            "username": fake.name(),
            "user_type": "D",
            "password": fake.password(),
            "region_id": district_user.region_id,
            "district_id": district_user.district_id,
        },
        "INCORRECT_FIELDS_PROVIDED_FOR_DISTRICT_USER": {
            "username": fake.name(),
            "user_type": "D",
            "password": fake.password(),
            "region_id": district_user.region_id,
        },
    }
    return payload
