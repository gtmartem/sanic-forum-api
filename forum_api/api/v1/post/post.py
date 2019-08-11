from sanic.response import json

from forum_api import db_api


async def get_all_posts_method(request, section_id):
    section = await db_api.get_all_posts(section_id)
    return json(section, status=200)


async def get_post_by_id_method(request, post_id):
    section = await db_api.get_post_by_id(post_id)
    return json(section, status=200)


async def post_post_method(request, section_id):
    section = await db_api.post_post(request.json, section_id)
    return json(section, status=200)


async def put_post_method(request, post_id):
    section = await db_api.put_post(request.json, post_id)
    return json(section, status=200)


async def delete_post_method(request, post_id):
    await db_api.delete_post(post_id)
    return json(post_id, status=200)
