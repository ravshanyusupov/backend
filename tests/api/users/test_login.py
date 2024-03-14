import pytest


@pytest.mark.parametrize(
    "user, status_code, code",
    [
        ("cec_user", 200, None),
        ("region_user", 200, None),
        ("district_user", 200, None),
        ("invalid_user", 401, 2006),
    ],
)
@pytest.mark.django_db
def test_login(request, client, url_name, user, status_code, code):
    payload = dict(
        username="invalid_user",
        password="12345678",
    )

    if not (user == "invalid_user"):
        user_data = request.getfixturevalue(user)
        payload = dict(
            username=user_data.username,
            password=user_data.raw_password,
        )

    url = url_name(__file__)
    response = client.post(url, payload)
    assert response.status_code == status_code

    if code:
        assert response.json()[0]["code"] == code
