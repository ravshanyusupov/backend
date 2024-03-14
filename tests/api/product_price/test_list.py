import pytest


@pytest.mark.parametrize(
    "auth_client, status_code, total, filters",
    [
        ("cec_client", 200, 1, ""),
        ("region_client", 200, 1, ""),
        ("district_client", 200, 1, ""),
        ("district_client", 200, 0, "?product_id=100"),
    ],
)
@pytest.mark.django_db
def test_list(
    request, auth_client, status_code, filters, total, url_name, product_price
):
    client = request.getfixturevalue(auth_client)
    url = url_name(__file__)
    response = client.post(url + filters)

    assert response.status_code == status_code
    assert len(response.json()) == total
