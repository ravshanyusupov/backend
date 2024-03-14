import orjson
from ninja.renderers import BaseRenderer


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        response_template = {
            "status": response_status,
            "data": data,
        }

        return orjson.dumps(response_template)
