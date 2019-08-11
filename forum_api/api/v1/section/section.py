from sanic.response import json

from forum_api import db_api


async def get_all_sections_method(request):
    section = await db_api.get_all_sections()
    return json(section, status=200)


async def get_section_by_id_method(request, user_id):
    section = await db_api.get_section_by_id(user_id)
    return json(section, status=200)


async def post_section_method(request):
    section = await db_api.post_section(request.json)
    return json(section, status=200)


async def put_section_method(request, section_id):
    section = await db_api.put_section(request.json, section_id)
    return json(section, status=200)


async def delete_section_method(request, section_id):
    await db_api.delete_section(section_id)
    return json(section_id, status=200)
