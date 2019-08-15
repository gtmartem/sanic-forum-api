from sanic.exceptions import NotFound, InvalidUsage

from forum_api import db_api
from forum_api.api.v1.helper import HTTPViewHelper
from forum_api.errors.exceptions import server_error_wrapper


class GetAllSectionsView(HTTPViewHelper):
    body_required = False
    json_required = False

    @server_error_wrapper
    async def get(self, request):
        sections = await db_api.get_all_sections()
        if sections:
            return sections
        raise NotFound("no sections")


class GetSectionsByPageView(HTTPViewHelper):
    body_required = False
    json_required = False

    @server_error_wrapper
    async def get(self, request, page_number):
        page_number = 1 if page_number in [0, 1] else page_number
        sections = await db_api.get_sections_by_page(page_number)
        if sections:
            return sections
        raise NotFound(f"no sections on {page_number} page")


class GetSectionByIdView(HTTPViewHelper):
    body_required = False
    json_required = False

    @server_error_wrapper
    async def get(self, request, section_id):
        section = await db_api.get_section_by_id(section_id)
        if section:
            return section
        raise NotFound(f"no section with {section_id} id")


class GetSectionsBySearchView(HTTPViewHelper):
    body_required = True
    json_required = ["search"]
    type_check = {"search": str}

    @server_error_wrapper
    async def get(self, request):
        print(request.json.get("search"))
        sections = await db_api.get_sections_by_search(request.json)
        if sections:
            return sections
        raise NotFound(f"no found sections by search: "
                       f"{request.json.get('search')}")


class PostSectionView(HTTPViewHelper):
    body_required = True
    json_required = ["title", "description"]
    type_check = {"title": str, "description": str}
    status = 201

    @server_error_wrapper
    async def post(self, request):
        section = await db_api.post_section(request.json)
        return section


class PutSectionView(HTTPViewHelper):
    body_required = True
    json_required = ["title", "description"]
    type_check = {"title": str, "description": str}

    @server_error_wrapper
    async def put(self, request, section_id):
        section = await db_api.put_section(request.json, section_id)
        if section:
            return section
        raise NotFound(f"no section with {section_id} id")


class DeleteSectionView(HTTPViewHelper):
    body_required = False
    json_required = False

    @server_error_wrapper
    async def delete(self, request, section_id):
        res = await db_api.delete_section(section_id)
        if res:
            return {"id": section_id}
        raise NotFound(f"no section with {section_id} id")
