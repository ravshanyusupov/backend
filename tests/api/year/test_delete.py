import pytest


@pytest.mark.parametrize(
    "auth_client, status_code, code",
    [("cec_client", 204, None), ("region_client", 403, 1000)],
)
@pytest.mark.django_db
def test_delete(
    request,
    auth_client,
    status_code,
    code,
    url_name,
    data,
):
    client = request.getfixturevalue(auth_client)
    url = url_name(__file__)
    payload = {"id": data.id}

    response = client.post(url, payload)

    if code:
        assert response.json()[0]["code"] == code
    assert response.status_code == status_code


@pytest.fixture
def data(year_factory):
    instance = year_factory.create(year=2023)

    return instance
