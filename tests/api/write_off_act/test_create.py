import datetime
import uuid

import pytest

from tests.faker import fake
from django.test.client import MULTIPART_CONTENT
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.parametrize(
    "user_client_string, url_name_string, status_code",
    [
        ("region_client", "url_name", 403),
        ("cec_client", "url_name", 403),
        ("client", "url_name", 401),
    ],
)
@pytest.mark.django_db
def test_create_write_off_act_status(
    request, user_client_string, url_name_string, status_code, write_off_act_create_data
):
    user_client = request.getfixturevalue(user_client_string)
    url_name = request.getfixturevalue(url_name_string)
    response = user_client.post(
        url_name(__file__),
        write_off_act_create_data,
        content_type=MULTIPART_CONTENT,
    )
    assert response.status_code == status_code


@pytest.mark.django_db
def test_create_write_off_act_success(inventory_unit_create_data, url_name):
    auth_client = inventory_unit_create_data["auth_client"]
    inventory_unit = inventory_unit_create_data["inventory_unit"]
    inventory_unit_2 = inventory_unit_create_data["inventory_unit_2"]
    file = SimpleUploadedFile(
        "file.pdf", b"file_content", content_type="application/pdf"
    )

    payload = {
        "name_uz": "akt_1",
        "inventory_numbers": [
            inventory_unit.inventory_number,
            inventory_unit_2.inventory_number,
        ],
        "file": file,
    }
    response = auth_client.post(
        url_name(__file__), payload, content_type=MULTIPART_CONTENT
    )
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["name_uz"] == payload["name_uz"]
    assert (
        response_data["inventory_numbers"][0]["inventory_number"]
        in payload["inventory_numbers"]
    )


@pytest.mark.django_db
def test_create_write_off_act_fail_wrong_inventory_unit(
    inventory_unit_create_data, url_name, inventory_unit_factory
):
    auth_client = inventory_unit_create_data["auth_client"]
    inventory_unit = inventory_unit_create_data["inventory_unit"]
    inventory_unit_2 = inventory_unit_create_data["inventory_unit_2"]
    file = SimpleUploadedFile(
        "file.pdf", b"file_content", content_type="application/pdf"
    )
    inventory_unit_3 = inventory_unit_factory.create()
    payload = {
        "name_uz": "akt_1",
        "inventory_numbers": [
            inventory_unit.inventory_number,
            inventory_unit_2.inventory_number,
            inventory_unit_3.inventory_number,
        ],
        "file": file,
    }
    response = auth_client.post(
        url_name(__file__), payload, content_type=MULTIPART_CONTENT
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_write_off_act_fail_empty_inventory_unit(url_name, district_client):
    file = SimpleUploadedFile(
        "file.pdf", b"file_content", content_type="application/pdf"
    )

    payload = {
        "name_uz": "akt_1",
        "inventory_numbers": [str(uuid.uuid4())],
        "file": file,
    }
    response = district_client.post(
        url_name(__file__), payload, content_type=MULTIPART_CONTENT
    )
    assert response.status_code == 400
