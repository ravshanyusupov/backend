import pytest


@pytest.mark.parametrize(
    "user_client_string, url_name_string, status_code",
    [
        ("cec_client", "url_name", 200),
        ("region_client", "url_name", 404),
        ("district_client", "url_name", 404),
        ("client", "url_name", 401),
    ],
)
@pytest.mark.django_db
def test_inventory_unit_status(
    user_client_string, url_name_string, status_code, inventory_unit_factory, request
):
    inventory_unit = inventory_unit_factory.create()
    payload = {"id": inventory_unit.id}
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    response = user_client.post(url_name(__file__), payload)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_get_unavailable_inventory_unit(cec_client, url_name, inventory_unit_factory):
    inventory_unit = inventory_unit_factory.create()
    non_exists_id = inventory_unit.id + 1
    payload = {"id": non_exists_id}
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_fail_inventory_unit(district_client, url_name, inventory_unit_factory):
    inventory_unit = inventory_unit_factory.create()
    non_exists_id = inventory_unit.id
    payload = {"id": non_exists_id}
    response = district_client.post(url_name(__file__), payload)
    assert response.status_code == 404
