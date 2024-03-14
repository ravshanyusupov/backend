import pytest


@pytest.mark.parametrize(
    "auth_client_str, status_code, code",
    [
        ("district_client", 200, None),
        ("region_client", 200, None),
        ("cec_client", 200, None),
        ("client", 401, 1001),
    ],
)
@pytest.mark.django_db
def test_me(request, auth_client_str, status_code, code, url_name):
    auth_client = request.getfixturevalue(auth_client_str)
    url = url_name(__file__)

    response = auth_client.post(url)

    if code:
        assert response.json()[0]["code"] == code
    assert response.status_code == status_code
