import datetime

import aiopg
from psycopg2.extras import DictCursor
from sanic.exceptions import InvalidUsage, NotFound

from forum_api.db_api.__config import DB_URL


async def get_all_sections():
    query = """
    SELECT id, title, description, created_at, updated_at 
    FROM public.sections
    ORDER BY updated_at DESC;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query)
            data = await cur.fetchall()
            if data:
                return [dict(u) for u in data]
            return None


async def get_sections_by_page(page_number):
    query = """
    SELECT id, title, description, created_at, updated_at 
    FROM public.sections
    ORDER BY updated_at DESC
    LIMIT %(limit)s OFFSET %(offset)s;"""
    limit = 30
    offset = (page_number - 1) * limit
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {"limit": limit, "offset": offset})
            data = await cur.fetchall()
            if data:
                return [dict(u) for u in data]
            return None


async def get_section_by_id(section_id):
    query = """
    SELECT id, title, description, created_at, updated_at 
    FROM public.sections
    WHERE id = %(section_id)s;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {'section_id': section_id})
            data = await cur.fetchone()
            if data:
                return dict(data)
            return None


async def get_sections_by_search(request):
    query = """
    SELECT public.sections.id, 
           public.sections.title, 
           public.sections.description, 
           public.sections.created_at, 
           public.sections.updated_at, 
           1 AS rank
    FROM public.sections_search
    LEFT JOIN public.sections 
    ON public.sections.id = public.sections_search.section_id
    WHERE public.sections_search.title @@ plainto_tsquery(%(search)s)
    ORDER BY rank;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {'search': request.get("search")})
            data = await cur.fetchone()
            if data:
                return dict(data)
            return None


async def post_section(request):
    query = """
    INSERT 
    INTO sections (title, description, created_at, updated_at)
    VALUES (%(title)s, %(description)s, %(created_at)s, %(updated_at)s)
    RETURNING  id, title, description, created_at, updated_at;"""
    search_query = """
    INSERT 
    INTO public.sections_search (section_id, title)
    VALUES (%(section_id)s, 
            to_tsvector(%(title)s))
    RETURNING section_id;"""
    params = dict(
        title=request.get("title", None),
        description=request.get("description", None),
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        updated_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, params)
            data = await cur.fetchone()
            if data:
                serach_params = dict(
                    section_id=data.get("id"),
                    title=data.get("title")
                )
                await cur.execute(search_query, serach_params)
                return dict(data)
            return None


async def put_section(request, section_id):
    query = """
    UPDATE sections 
    SET title = %(title)s, 
        description = %(description)s, 
        updated_at = %(updated_at)s
    WHERE id = %(section_id)s
    RETURNING  id, title, description, created_at, updated_at;"""
    search_query = """
    UPDATE sections_search 
    SET title = to_tsvector(%(title)s)
    WHERE section_id = %(section_id)s;"""
    params = dict(
        title=request.get("title"),
        description=request.get("description"),
        updated_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        section_id=section_id
    )
    search_params = dict(section_id=section_id, title=request.get("title"))
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, params)
            data = await cur.fetchone()
            if data:
                await cur.execute(search_query, search_params)
                return dict(data)
            return None


async def delete_section(section_id):
    query = """
    DELETE FROM sections WHERE id = %(section_id)s
    RETURNING id;"""
    search_query = """
    DELETE FROM sections_search WHERE section_id = %(section_id)s;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {"section_id": section_id})
            res = await cur.fetchone()
            if res:
                cur.execute(search_query, {"section_id": section_id})
                return dict(res)
            return None

