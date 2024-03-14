import pytest


@pytest.mark.parametrize(
    "auth_client, status_code, code, found",
    [
        ("cec_client", 204, None, True),
        ("cec_client", 404, 1002, False),
        ("region_client", 403, 1000, True),
    ],
)
@pytest.mark.django_db
def test_delete(
    request, auth_client, status_code, code, found, url_name, fake_category
):
    client = request.getfixturevalue(auth_client)
    url = url_name(__file__)
    payload = {"id": fake_category.id}

    if not found:
        payload["id"] = 1000

    response = client.post(url, payload)

    if code:
        response.json()[0]["code"] == code
    assert response.status_code == status_code
