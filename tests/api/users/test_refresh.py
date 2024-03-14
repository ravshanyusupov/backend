import pytest


@pytest.mark.parametrize(
    "user, code, status_code",
    [
        ("cec_login", None, 200),
        ("region_login", None, 200),
        ("district_login", None, 200),
        ("invalid_refresh_token", 1001, 401),
    ],
)
@pytest.mark.django_db
def test_refresh(request, user, code, status_code, url_name, client):
    user_token = "INVALIDUSERTOKEN"
    if not user == "invalid_refresh_token":
        user_token = request.getfixturevalue(user)["refresh"]
    payload = {"refresh": user_token}

    url = url_name(__file__)
    response = client.post(url, payload)

    assert response.status_code == status_code
    if code:
        assert response.json()[0]["code"] == code
