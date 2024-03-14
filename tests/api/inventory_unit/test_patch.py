import pytest


@pytest.mark.parametrize(
    "user_client_string, url_name_string, status_code",
    [
        ("district_client", "url_name", 403),
        ("region_client", "url_name", 403),
        ("cec_client", "url_name", 403),
        ("client", "url_name", 401),
    ],
)
@pytest.mark.django_db
def test_patch_inventory_unit_status(
    user_client_string, url_name_string, status_code, inventory_unit_factory, request
):
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    inventory_unit = inventory_unit_factory.create()
    payload = {"id": inventory_unit.id, "commissioning_year": 2022}
    response = user_client.post(url_name(__file__), payload)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_patch_inventory_unit_data(url_name, inventory_unit_create_data):
    auth_client = inventory_unit_create_data["auth_client"]
    inventory_unit_data = inventory_unit_create_data["inventory_unit_data"]
    response = auth_client.post(url_name(__file__), inventory_unit_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == inventory_unit_data["id"]
    assert response_data["product"]["id"] == inventory_unit_data["product_id"]
    assert (
        response_data["storage_place"]["id"] == inventory_unit_data["storage_place_id"]
    )
    assert response_data["district"]["id"] == inventory_unit_data["district_id"]
    assert (
        response_data["commissioning_year"] == inventory_unit_data["commissioning_year"]
    )
    assert response_data["inventory_number"] == inventory_unit_data["inventory_number"]


@pytest.mark.django_db(transaction=True)
def test_patch_inventory_unit_non_exists_product(url_name, inventory_unit_create_data):
    auth_client = inventory_unit_create_data["auth_client"]
    inventory_unit_data = inventory_unit_create_data["inventory_unit_data"]
    non_exists_id = inventory_unit_data["product_id"] + 100
    inventory_unit_data.update({"product_id": non_exists_id})
    response = auth_client.post(url_name(__file__), inventory_unit_data)
    assert response.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_patch_inventory_unit_non_exists_storage_place(
    url_name, inventory_unit_create_data
):
    auth_client = inventory_unit_create_data["auth_client"]
    inventory_unit_data = inventory_unit_create_data["inventory_unit_data"]
    non_exists_id = inventory_unit_data["storage_place_id"] + 100
    inventory_unit_data.update({"storage_place_id": non_exists_id})
    response = auth_client.post(url_name(__file__), inventory_unit_data)
    assert response.status_code == 400
