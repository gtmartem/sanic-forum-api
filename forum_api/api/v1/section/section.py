from sanic.response import json

from forum_api import db_api


async def get_all_sections_method(request):
    users = await db_api.get_all_sections()
    return json(users, status=200)


async def get_section_by_id_method(request, user_id):
    user = await db_api.get_section_by_id(user_id)
    return json(user, status=200)
