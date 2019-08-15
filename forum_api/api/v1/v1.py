from sanic import Blueprint

from forum_api.api.v1.post.post import GetAllPostsView, \
    GetPostById, PostPostView, PutPostView, DeletePostView, \
    GetPostsByPageView, GetPostsBySearchView
from forum_api.api.v1.section.section import GetAllSectionsView, \
    GetSectionByIdView, PostSectionView, PutSectionView, DeleteSectionView, \
    GetSectionsByPageView, GetSectionsBySearchView
from forum_api.api.v1.comment.comment import GetAllCommentsView, \
    GetCommentById, PutCommentView, DeleteCommentView, PostCommentView

v1 = Blueprint("v1", url_prefix="/v1")

# section api:
v1.add_route(GetAllSectionsView.as_view(), uri="/sections",
             methods=["GET"])
v1.add_route(GetSectionsByPageView.as_view(), uri="/sections/<page_number:int>",
             methods=["GET"])
v1.add_route(GetSectionByIdView.as_view(), uri="/section/<section_id:int>",
             methods=["GET"])
v1.add_route(GetSectionsBySearchView.as_view(), uri="/sections/search",
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
v1.add_route(GetPostsByPageView.as_view(),
             uri="/section/<section_id:int>/posts/<page_number:int>",
             methods=["GET"])
v1.add_route(GetPostById.as_view(), uri="/post/<post_id:int>",
             methods=["GET"])
v1.add_route(GetPostsBySearchView.as_view(), uri="/posts/search",
             methods=["GET"])
v1.add_route(PostPostView.as_view(), uri="/section/<section_id:int>/post",
             methods=["POST"])
v1.add_route(PutPostView.as_view(), uri="/post/<post_id:int>",
             methods=["PUT"])
v1.add_route(DeletePostView.as_view(), uri="/post/<post_id:int>",
             methods=["DELETE"])

# comment api:
v1.add_route(GetAllCommentsView.as_view(), uri="/post/<post_id:int>/comments",
             methods=["GET"])
v1.add_route(GetCommentById.as_view(), uri="/comment/<comment_id:int>/",
             methods=["GET"])
v1.add_route(PostCommentView.as_view(), uri="/post/<post_id:int>/comment",
             methods=["POST"])
v1.add_route(PutCommentView.as_view(), uri="/comment/<comment_id:int>",
             methods=["PUT"])
v1.add_route(DeleteCommentView.as_view(), uri="/comment/<comment_id:int>",
             methods=["DELETE"])
