import pytest


@pytest.mark.parametrize(
    "auth_client, status_code, total, filters",
    [
        ("cec_client", 200, 1, ""),
        ("region_client", 200, 1, ""),
        ("district_client", 200, 1, ""),
        ("district_client", 200, 0, "?search=Litsey"),
    ],
)
@pytest.mark.django_db
def test_list(
    request, auth_client, status_code, filters, total, url_name, fake_category
):
    client = request.getfixturevalue(auth_client)
    url = url_name(__file__)
    response = client.post(url + filters)

    assert response.status_code == status_code
    assert len(response.json()) == total
