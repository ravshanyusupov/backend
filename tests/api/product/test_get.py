import pytest


@pytest.mark.parametrize(
    "auth_client, status_code, code, found",
    [
        ("cec_client", 200, None, True),
        ("region_client", 200, None, True),
        ("district_client", 200, None, True),
        ("district_client", 404, 1002, False),
    ],
)
@pytest.mark.django_db
def test_get(request, auth_client, status_code, code, found, url_name, product):
    client = request.getfixturevalue(auth_client)
    url = url_name(__file__)
    payload = {"id": product.id}

    if not found:
        payload["id"] = 1000

    response = client.post(url, payload)

    if code:
        response.json()[0]["code"] == code
    assert response.status_code == status_code
