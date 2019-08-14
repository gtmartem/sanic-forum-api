from sanic.response import json


async def error_handler(request, exception):
    error_body = {
        "success": False,
        "error": str(exception)
    }
    return json(error_body, status=exception.status_code)
