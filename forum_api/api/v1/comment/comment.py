from sanic.response import json

from forum_api import db_api


async def get_all_comments_method(request, post_id):
    section = await db_api.get_all_comments(post_id)
    return json(section, status=200)


async def get_comment_by_id_method(request, comment_id):
    section = await db_api.get_comment_by_id(comment_id)
    return json(section, status=200)


async def post_comment_method(request, post_id):
    section = await db_api.post_comment(request.json, post_id)
    return json(section, status=200)


async def put_comment_method(request, comment_id):
    section = await db_api.put_comment(request.json, comment_id)
    return json(section, status=200)


async def delete_comment_method(request, comment_id):
    await db_api.delete_comment(comment_id)
    return json(comment_id, status=200)
