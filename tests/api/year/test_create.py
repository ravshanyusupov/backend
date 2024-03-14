import pytest


@pytest.mark.parametrize(
    "auth_client, payload,status_code, code",
    [
        ("cec_client", {"year": 2023}, 201, None),
        ("region_client", {"year": 2023}, 403, 1000),
    ],
)
@pytest.mark.django_db
def test_create(request, auth_client, payload, status_code, code, url_name):
    client = request.getfixturevalue(auth_client)
    url = url_name(__file__)

    response = client.post(url, payload)

    if code:
        assert response.json()[0]["code"] == code
    assert response.status_code == status_code
