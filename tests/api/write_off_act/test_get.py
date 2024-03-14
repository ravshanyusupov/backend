import pytest
from src.apps.inventory.models import WriteOffAct


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
def test_get_write_off_act_status(
    user_client_string,
    url_name_string,
    status_code,
    write_off_act_factory,
    request,
    example_file,
):
    instance = write_off_act_factory.create(file=example_file)
    payload = {"id": instance.id}
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    response = user_client.post(url_name(__file__), payload)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "write_off_act_data_str, url_name_string, status_code",
    [
        ("write_off_act_data_for_region", "url_name", 200),
        ("write_off_act_data_for_district", "url_name", 200),
    ],
)
@pytest.mark.django_db
def test_get_write_off_act_filter(
    write_off_act_data_str, url_name_string, status_code, request
):
    write_off_act_data = request.getfixturevalue(write_off_act_data_str)
    url_name = request.getfixturevalue(url_name_string)
    auth_client = write_off_act_data["auth_client"]
    instance = write_off_act_data["instance"]
    response = auth_client.post(url_name(__file__), {"id": instance.id})
    
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "write_off_act_data_str, status_code",
    [
        ("write_off_act_data_for_region", 200),
        ("write_off_act_data_for_district", 200),
    ],
)
@pytest.mark.django_db
def test_get_write_off_act_file(
    request, write_off_act_data_str, status_code, url_name, client
):
    write_off_act_data = request.getfixturevalue(write_off_act_data_str)
    auth_client = write_off_act_data["auth_client"]
    instance = write_off_act_data["instance"]

    url = url_name(__file__)

    with instance.file.open(mode="rb") as file:
        binary_content = file.read()

    response = auth_client.post(url, {"id": instance.id})

    assert response.status_code == status_code

    file_response = client.get(response.json().get("file", None))

    received_content = b"".join(file_response.streaming_content)

    assert received_content == binary_content
