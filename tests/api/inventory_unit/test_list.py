import pytest


@pytest.mark.parametrize(
    "client_str, data_length, result_length",
    [("cec_client", 50, 10), ("region_client", 100, 0), ("district_client", 1, 0)],
)
@pytest.mark.django_db
def test_list_inventory_unit(
    inventory_unit_factory, url_name, client_str, data_length, result_length, request
):
    inventory_unit_factory.create_batch(data_length)
    url = url_name(__file__)
    client = request.getfixturevalue(client_str)
    response = client.post(url)
    result = response.json()["items"]

    assert response.status_code == 200
    assert len(result) == result_length


@pytest.mark.django_db
def test_inventory_unit_for_district(
    inventory_unit_factory, url_name, inventory_unit_district_client
):
    inventory_unit_factory.create_batch(50)
    response = inventory_unit_district_client.post(f"{url_name(__file__)}?size=5")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 5


@pytest.mark.django_db
def test_inventory_unit_for_region(
    inventory_unit_factory, url_name, inventory_unit_region_client
):
    inventory_unit_factory.create_batch(30)
    response = inventory_unit_region_client.post(f"{url_name(__file__)}?size=50")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 40


@pytest.mark.django_db
def test_inventory_unit_visible(inventory_unit_factory, url_name, cec_client):
    for _ in range(10):
        inventory_unit_factory.create(visible=False)
    response = cec_client.post(f"{url_name(__file__)}")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 0
