from typing import Any
from django.conf import settings
from ninja_lib.import_folder import dynamic_import_from_folder
from ninja.constants import NOT_SET
from ninja import NinjaAPI

from .auth import CustomAsyncJWTAuth


def load_api(api_instance):
    module_list = dynamic_import_from_folder(settings.API_DIRECTORY)

    for api in module_list:
        module_instance = api["module"]
        module_name = api["module_name"].split(".")

        endpoint_path = "/".join(module_name[2:]) + "/"

        if not getattr(module_instance, "handler", None):
            raise Exception(f"Handler not found in {api['module_name']}")

        url_name = ".".join(module_name[1:])
        handler_method = module_instance.handler
        permissions = getattr(module_instance, "permissions", None)

        api_instance.post(
            endpoint_path,
            response=getattr(module_instance, "response", NOT_SET),
            auth=getattr(module_instance, "auth", CustomAsyncJWTAuth(permissions=permissions)),
            operation_id=getattr(module_instance, "operation_id", None),
            summary=getattr(module_instance, "summary", None),
            description=getattr(module_instance, "description", None),
            tags=getattr(module_instance, "tags", [module_name[2:][0]]),
            deprecated=getattr(module_instance, "deprecated", None),
            by_alias=getattr(module_instance, "by_alias", False),
            exclude_unset=getattr(module_instance, "exclude_unset", False),
            exclude_defaults=getattr(module_instance, "exclude_defaults", False),
            exclude_none=getattr(module_instance, "exclude_none", False),
            url_name=getattr(module_instance, "url_name", url_name),
            include_in_schema=getattr(module_instance, "include_in_schema", True),
            openapi_extra=getattr(module_instance, "openapi_extra", None),
        )(handler_method)
