import pytest


@pytest.fixture
def cec_login(client, cec_user):
    payload = dict(
        username=cec_user.username,
        password=cec_user.raw_password,
    )

    response = client.post("/api/users/login/", payload)

    return response.json()


@pytest.fixture
def region_login(client, region_user):
    payload = dict(
        username=region_user.username,
        password=region_user.raw_password,
    )
    response = client.post("/api/users/login/", payload)
    return response.json()


@pytest.fixture
def district_login(client, district_user):
    payload = dict(
        username=district_user.username,
        password=district_user.raw_password,
    )
    response = client.post("/api/users/login/", payload)
    return response.json()
