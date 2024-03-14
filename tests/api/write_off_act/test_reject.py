import datetime
import pytest
from tests.faker import fake
from src.apps.inventory.models import WriteOffAct


@pytest.mark.parametrize(
    "user_client_string, url_name_string, status_code",
    [
        ("district_client", "url_name", 403),
        ("region_client", "url_name", 403),
        ("cec_client", "url_name", 200),
        ("client", "url_name", 401),
    ],
)
@pytest.mark.django_db
def test_reject_write_off_act_status(
    user_client_string,
    url_name_string,
    status_code,
    write_off_act_factory,
    request,
    example_file,
):
    instance = write_off_act_factory.create(file=example_file)
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    payload = {"id": instance.id}
    response = user_client.post(url_name(__file__), payload)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_region_reject_write_off_act_success(url_name, write_off_act_data_for_region):
    auth_client = write_off_act_data_for_region["auth_client"]
    instance = write_off_act_data_for_region["instance"]
    payload = {"id": instance.id}
    response = auth_client.post(url_name(__file__), payload)
    assert response.status_code == 200
    assert response.json()["status"] == WriteOffAct.REJECTED


@pytest.mark.django_db
def test_region_reject_rejected_write_off_act(url_name, write_off_act_data_for_region):
    auth_client = write_off_act_data_for_region["auth_client"]
    instance = write_off_act_data_for_region["instance"]
    payload = {"id": instance.id}
    auth_client.post(url_name(__file__), payload)
    response = auth_client.post(url_name(__file__), payload)
    assert response.status_code == 403
    assert response.json()[0]["code"] == 4005
    assert response.json()[0]["name_uz"] == "Ta'rif qilingan aktni o'zgartira olmaysiz"


@pytest.mark.django_db
def test_cec_reject_write_off_act_success(
    url_name, cec_client, write_off_act_factory, example_file
):
    instance = write_off_act_factory.create(file=example_file)
    payload = {"id": instance.id}
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 200
    assert response.json()["status"] == WriteOffAct.REJECTED


@pytest.mark.django_db
def test_cec_reject_rejected_write_off_act(
    url_name, cec_client, write_off_act_factory, example_file
):
    instance = write_off_act_factory.create(file=example_file)
    payload = {"id": instance.id}
    cec_client.post(url_name(__file__), payload)
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 403
    assert response.json()[0]["code"] == 4005
    assert response.json()[0]["name_uz"] == "Ta'rif qilingan aktni o'zgartira olmaysiz"


@pytest.mark.django_db
def test_region_reject_approved_write_off_act(
    url_name, cec_client, write_off_act_data_for_region
):
    auth_client = write_off_act_data_for_region["auth_client"]
    instance = write_off_act_data_for_region["instance"]
    payload = {"id": instance.id}
    cec_client.post("/api/write_off_act/approve/", payload)
    response = auth_client.post(url_name(__file__), payload)
    assert response.status_code == 403
    assert response.json()[0]["code"] == 4005
    assert response.json()[0]["name_uz"] == "Ta'rif qilingan aktni o'zgartira olmaysiz"


@pytest.mark.django_db
def test_cec_reject_approved_write_off_act(
    url_name, cec_client, write_off_act_factory, example_file
):
    instance = write_off_act_factory.create(file=example_file)
    payload = {"id": instance.id}
    cec_client.post("/api/write_off_act/approve/", payload)
    response = cec_client.post(url_name(__file__), payload)
    assert response.status_code == 403
    assert response.json()[0]["code"] == 4005
    assert response.json()[0]["name_uz"] == "Ta'rif qilingan aktni o'zgartira olmaysiz"
