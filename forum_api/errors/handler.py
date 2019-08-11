from sanic.response import json


async def error_handler(request, exception):
    return json({'success': False, 'error': exception.msg},
                status=exception.status)
