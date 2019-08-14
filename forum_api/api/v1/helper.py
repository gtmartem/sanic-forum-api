from sanic.response import json
from json import loads
from sanic.views import HTTPMethodView
from sanic.exceptions import InvalidUsage


class HTTPViewHelper(HTTPMethodView):

    body_required = None
    json_required = None
    type_check = None
    status = 200

    async def dispatch_request(self, request, *args, **kwargs):
        self.validate_request(request)
        result = await super().dispatch_request(request, *args, **kwargs)
        return self.prepared_response(result)

    def validate_request(self, request):
        if not request.body and self.body_required:
            raise InvalidUsage("empty body")
        if self.json_required:
            for k in self.json_required:
                if k not in loads(request.body):
                    raise InvalidUsage(f"{k} not in body")
        if self.type_check:
            for k in self.type_check.keys():
                try:
                    self.type_check[k](request.get(k))
                except TypeError:
                    raise InvalidUsage(
                        f"{request.get(k)}'s type must be {self.type_check[k]}")

    def prepared_response(self, result):
        return json(result, status=self.status)
