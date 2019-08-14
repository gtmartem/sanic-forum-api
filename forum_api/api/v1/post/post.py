from sanic.exceptions import NotFound, ServerError

from forum_api.errors.exceptions import server_error_wrapper
from forum_api.api.v1.helper import HTTPViewHelper
from forum_api import db_api


class GetAllPostsView(HTTPViewHelper):
    body_required = False
    json_required = False

    @server_error_wrapper
    async def get(self, request, section_id):
        posts = await db_api.get_all_posts(section_id)
        if posts:
            return posts
        raise NotFound(f"no posts in section {section_id}")


class GetPostsByPageView(HTTPViewHelper):
    body_required = False
    json_required = False

    @server_error_wrapper
    async def get(self, request, section_id, page_number):
        page_number = 1 if page_number in [0, 1] else page_number
        posts = await db_api.get_posts_by_page(section_id, page_number)
        if posts:
            return posts
        raise NotFound(f"no posts on {page_number} page")


class GetPostsBySearchView(HTTPViewHelper):
    body_required = True
    json_required = ["search"]
    type_check = {"search": str}

    @server_error_wrapper
    async def get(self, request):
        posts = await db_api.get_posts_by_search(request)
        if posts:
            return posts
        raise NotFound(f"no found posts by search: {request.get('search')}")


class GetPostById(HTTPViewHelper):
    body_required = False
    json_required = False

    @server_error_wrapper
    async def get(self, request, post_id):
        posts = await db_api.get_post_by_id(post_id)
        if posts:
            return posts
        raise NotFound(f"no post with {post_id} id")


class PostPostView(HTTPViewHelper):
    body_required = True
    json_required = ["title", "description"]
    type_check = {"title": str, "description": str}
    status = 201

    @server_error_wrapper
    async def post(self, request, section_id):
        post = await db_api.post_post(request.json, section_id)
        if post:
            return post
        raise ServerError("server error")


class PutPostView(HTTPViewHelper):
    body_required = True
    json_required = ["title", "description"]
    type_check = {"title": str, "description": str}

    @server_error_wrapper
    async def put(self, request, post_id):
        post = await db_api.put_post(request.json, post_id)
        if post:
            return post
        raise NotFound(f"no post with {post_id} id")


class DeletePostView(HTTPViewHelper):
    body_required = False
    json_required = False

    @server_error_wrapper
    async def delete(self, request, post_id):
        await db_api.delete_post(post_id)
        return {"id": post_id}
