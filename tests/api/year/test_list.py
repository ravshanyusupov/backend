import pytest


@pytest.mark.parametrize(
    "auth_client, status_code, length",
    [
        ("cec_client", 200, 1),
        ("region_client", 200, 1),
        ("district_client", 200, 1),
    ],
)
@pytest.mark.django_db
def test_delete(
    request,
    auth_client,
    status_code,
    length,
    url_name,
    data,
):
    client = request.getfixturevalue(auth_client)
    url = url_name(__file__)

    response = client.post(url)

    assert len(response.json()) == length
    assert response.status_code == status_code


@pytest.fixture
def data(year_factory):
    instance = year_factory.create(year=2023)

    return instance
