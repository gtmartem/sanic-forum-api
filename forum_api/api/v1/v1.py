from sanic import Blueprint

from forum_api.api.v1.section.section import \
    get_all_sections_method, \
    get_section_by_id_method, \
    post_section_method, \
    put_section_method, \
    delete_section_method
from forum_api.api.v1.post.post import \
    get_all_posts_method, \
    get_post_by_id_method, \
    post_post_method, \
    put_post_method, \
    delete_post_method
from forum_api.api.v1.comment.comment import \
    get_all_comments_method, \
    get_comment_by_id_method, \
    post_comment_method, \
    put_comment_method, \
    delete_comment_method

v1 = Blueprint("v1", url_prefix="/v1")

# section api:
v1.add_route(get_all_sections_method, uri="/sections",
             methods=["GET"])
v1.add_route(get_section_by_id_method, uri="/section/<section_id>",
             methods=["GET"])
v1.add_route(post_section_method, uri="/section",
             methods=["POST"])
v1.add_route(put_section_method, uri="/section/<section_id>",
             methods=["PUT"])
v1.add_route(delete_section_method, uri="/section/<section_id>",
             methods=["DELETE"])

# post api:
v1.add_route(get_all_posts_method, uri="/section/<section_id>",
             methods=["GET"])
v1.add_route(get_post_by_id_method, uri="/post/<post_id>",
             methods=["GET"])
v1.add_route(post_post_method, uri="/section/<section_id>/post",
             methods=["POST"])
v1.add_route(put_post_method, uri="/post/<post_id>",
             methods=["PUT"])
v1.add_route(delete_post_method, uri="/post/<post_id>",
             methods=["DELETE"])

# comment api:
v1.add_route(get_all_comments_method, uri="/post/<post_id>",
             methods=["GET"])
v1.add_route(get_comment_by_id_method, uri="/comment/<comment_id>/",
             methods=["GET"])
v1.add_route(post_comment_method, uri="/post/<post_id>/comment",
             methods=["POST"])
v1.add_route(put_comment_method, uri="/comment/<comment_id>",
             methods=["PUT"])
v1.add_route(delete_comment_method, uri="/comment/<comment_id>",
             methods=["DELETE"])
