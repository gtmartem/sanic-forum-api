from sanic import Blueprint

from forum_api.api.v1.post.post import GetAllPostsView, GetPostsByPage, \
    GetPostById, PostPostView, PutPostView, DeletePostView
from forum_api.api.v1.section.section import GetAllSectionsView, \
    GetSectionByIdView, PostSectionView, PutSectionView, DeleteSectionView, \
    GetSectionsByPage

from forum_api.api.v1.comment.comment import \
    get_all_comments_method, \
    get_comment_by_id_method, \
    post_comment_method, \
    put_comment_method, \
    delete_comment_method

v1 = Blueprint("v1", url_prefix="/v1")

# section api:
v1.add_route(GetAllSectionsView.as_view(), uri="/sections",
             methods=["GET"])
v1.add_route(GetSectionsByPage.as_view(), uri="/sections/<page_number:int>",
             methods=["GET"])
v1.add_route(GetSectionByIdView.as_view(), uri="/section/<section_id:int>",
             methods=["GET"])
v1.add_route(PostSectionView.as_view(), uri="/section",
             methods=["POST"])
v1.add_route(PutSectionView.as_view(), uri="/section/<section_id:int>",
             methods=["PUT"])
v1.add_route(DeleteSectionView.as_view(), uri="/section/<section_id:int>",
             methods=["DELETE"])

# post api:
v1.add_route(GetAllPostsView.as_view(), uri="/section/<section_id:int>/posts",
             methods=["GET"])
v1.add_route(GetPostsByPage.as_view(),
             uri="/section/<section_id: int>/posts/<page_number:int>",
             methods=["GET"])
v1.add_route(GetPostById.as_view(), uri="/post/<post_id:int>",
             methods=["GET"])
v1.add_route(PostPostView.as_view(), uri="/section/<section_id:int>/post",
             methods=["POST"])
v1.add_route(PutPostView.as_view(), uri="/post/<post_id:int>",
             methods=["PUT"])
v1.add_route(DeletePostView.as_view(), uri="/post/<post_id:int>",
             methods=["DELETE"])

# comment api:
v1.add_route(get_all_comments_method, uri="/post/<post_id>/comments",
             methods=["GET"])
v1.add_route(get_comment_by_id_method, uri="/comment/<comment_id>/",
             methods=["GET"])
v1.add_route(post_comment_method, uri="/post/<post_id>/comment",
             methods=["POST"])
v1.add_route(put_comment_method, uri="/comment/<comment_id>",
             methods=["PUT"])
v1.add_route(delete_comment_method, uri="/comment/<comment_id>",
             methods=["DELETE"])
