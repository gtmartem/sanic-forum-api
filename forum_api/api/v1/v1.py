from sanic import Blueprint

from forum_api.api.v1.section.section import \
    get_all_sections_method, \
    get_section_by_id_method


v1 = Blueprint("v1", url_prefix="/v1")
v1.add_route(get_all_sections_method, uri="/sections", methods=["GET"])
v1.add_route(get_section_by_id_method, uri="/section/<section_id>",
             methods=["GET"])

