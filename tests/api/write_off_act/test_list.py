import pytest


@pytest.mark.parametrize(
    "client_str, data_length, result_length",
    [("cec_client", 50, 10), ("region_client", 100, 0), ("district_client", 1, 0)],
)
@pytest.mark.django_db
def test_list_write_off_act(
    write_off_act_factory,
    url_name,
    client_str,
    data_length,
    result_length,
    request,
    example_file,
):
    write_off_act_factory.create_batch(data_length, file=example_file)
    url = url_name(__file__)
    client = request.getfixturevalue(client_str)
    response = client.post(url)
    result = response.json()["items"]
    assert response.status_code == 200
    assert len(result) == result_length


@pytest.mark.parametrize(
    "client_str, data_length, result_length",
    [
        ("write_off_act_region_client", 10, 40),
        ("write_off_act_district_client", 30, 20),
        ("cec_client", 50, 50),
    ],
)
@pytest.mark.django_db
def test_list_write_off_act_filter(
    write_off_act_factory,
    url_name,
    client_str,
    data_length,
    result_length,
    request,
    example_file,
):
    write_off_act_factory.create_batch(data_length, file=example_file)
    url = f"{url_name(__file__)}?size=100"
    client = request.getfixturevalue(client_str)
    response = client.post(url)
    result = response.json()["items"]

    assert response.status_code == 200
    assert len(result) == result_length


@pytest.mark.parametrize(
    "client_str, data_length, result_length",
    [
        ("write_off_act_region_client", 10, 5),
        ("write_off_act_district_client", 30, 5),
        ("cec_client", 50, 5),
    ],
)
@pytest.mark.django_db
def test_list_write_off_act_filter_pagination(
    write_off_act_factory,
    url_name,
    client_str,
    data_length,
    result_length,
    request,
    example_file,
):
    write_off_act_factory.create_batch(data_length, file=example_file)
    url = f"{url_name(__file__)}?size=5"
    client = request.getfixturevalue(client_str)
    response = client.post(url)
    result = response.json()["items"]

    assert response.status_code == 200
    assert len(result) == result_length
