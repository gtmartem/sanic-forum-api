from sanic.exceptions import NotFound, ServerError, InvalidUsage

from forum_api import db_api
from forum_api.api.v1.helper import HTTPViewHelper
from forum_api.errors.exceptions import server_error_wrapper


class GetAllCommentsView(HTTPViewHelper):
    body_required = False
    json_required = False

    @server_error_wrapper
    async def get(self, request, post_id):
        comments = await db_api.get_all_comments(post_id)
        if comments:
            tree = []
            self.create_comments_tree(comments, tree)
            return tree
        raise NotFound(f"no comments in post {post_id}")

    # очень наивная функция обхода элементов, так как для каждого элемента
    # происходит обход всего массива, т.е. n**2, можно делать копии и
    # удалять обойденные элементы, но тут вопрос просадок по памяти.
    # Так как комментариев вряд ли будет тысячи - обход,
    # для первой итерации, принимаем.
    def create_comments_tree(self, comments, tree, deep=1, parent_id=None):
        for leaf in comments:
            if leaf.get("level") == deep and leaf.get("parent_id") == parent_id:
                leaf["subtree"] = []
                tree.append(leaf)
                self.create_comments_tree(comments, leaf["subtree"],
                                          deep=deep+1, parent_id=leaf.get("id"))


class GetCommentById(HTTPViewHelper):
    body_required = False
    json_required = False

    @server_error_wrapper
    async def get(self, request, comment_id):
        comment = await db_api.get_comment_by_id(comment_id)
        if comment:
            return comment
        raise NotFound(f"no comment with {comment_id} id")


class PostCommentView(HTTPViewHelper):
    body_required = True
    json_required = ["title"]
    type_check = {"title": str}
    status = 201

    @server_error_wrapper
    async def post(self, request, post_id):
        try:
            state = await self.inherit_state(request)
        except (AssertionError, TypeError):
            raise InvalidUsage(
                "parent id:int or level:int for comment insertion needed")
        request = request.json.update(state)
        comment = await db_api.post_comment(request, post_id)
        if comment:
            return comment
        raise ServerError("server error")

    @staticmethod
    async def inherit_state(request):
        parent_id = request.get("parent_id", None)
        if not parent_id:
            return {"parent_id": None, "level": 1}
        else:
            level = await db_api.get_comment_level(parent_id)
            return {"parent_id": parent_id, "level": level}


class PutCommentView(HTTPViewHelper):
    body_required = True
    json_required = ["title"]
    type_check = {"title": str}

    @server_error_wrapper
    async def put(self, request, comment_id):
        comment = await db_api.put_comment(request.json, comment_id)
        if comment:
            return comment
        raise NotFound(f"no comment with {comment_id} id")


class DeleteCommentView(HTTPViewHelper):
    body_required = False
    json_required = False

    @server_error_wrapper
    async def delete(self, request, comment_id):
        await db_api.delete_comment(comment_id)
        return {"id": comment_id}
