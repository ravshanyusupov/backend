import pytest


@pytest.mark.parametrize(
    "user_client_string, url_name_string, status_code",
    [
        ("cec_client", "url_name", 403),
        ("region_client", "url_name", 403),
        ("district_client", "url_name", 403),
        ("client", "url_name", 401),
    ],
)
@pytest.mark.django_db
def test_create_inventory_unit_status_code(
    request,
    user_client_string,
    url_name_string,
    status_code,
    product_factory,
    storage_place_factory,
):
    product = product_factory.create()
    storage_place = storage_place_factory.create()
    payload = {
        "product_id": product.id,
        "storage_place_id": storage_place.id,
        "commissioning_year": 2020,
        "inventory_number": "12123123911",
    }
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    response = user_client.post(url_name(__file__), payload)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_create_inventory_unit_data(inventory_unit_create_data, url_name):
    auth_client = inventory_unit_create_data["auth_client"]
    inventory_data = inventory_unit_create_data["inventory_unit_data"]
    response = auth_client.post(url_name(__file__), inventory_data)
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["product"]["id"] == inventory_data["product_id"]
    assert response_data["storage_place"]["id"] == inventory_data["storage_place_id"]
    assert response_data["commissioning_year"] == inventory_data["commissioning_year"]
    assert response_data["inventory_number"] == inventory_data["inventory_number"]


@pytest.mark.django_db(transaction=True)
def test_create_inventory_unit_for_non_exists_product(
    inventory_unit_create_data, url_name
):
    auth_client = inventory_unit_create_data["auth_client"]
    inventory_unit_data = inventory_unit_create_data["inventory_unit_data"]
    non_exists_id = inventory_unit_data["product_id"] + 100
    inventory_unit_data.update({"product_id": non_exists_id})

    response = auth_client.post(url_name(__file__), inventory_unit_data)
    assert response.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_create_inventory_unit_for_non_exists_storage_place(
    inventory_unit_create_data, url_name
):
    auth_client = inventory_unit_create_data["auth_client"]
    inventory_unit_data = inventory_unit_create_data["inventory_unit_data"]
    non_exists_id = inventory_unit_data["storage_place_id"] + 100
    inventory_unit_data.update({"storage_place_id": non_exists_id})
    response = auth_client.post(url_name(__file__), inventory_unit_data)
    assert response.status_code == 400
