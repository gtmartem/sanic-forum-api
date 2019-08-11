import datetime

import aiopg
from psycopg2.extras import DictCursor

from forum_api.db_api.config import DB_URL


async def get_all_sections():
    query = """
    SELECT id, title, description, created_at, updated_at 
    FROM public.sections;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query)
            data = await cur.fetchall()
            return [dict(u) for u in data]


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


async def post_section(request):
    query = """
    INSERT 
    INTO sections (title, description, created_at, updated_at)
    VALUES (%(title)s, %(description)s, %(created_at)s, %(updated_at)s)
    RETURNING  id, title, description, created_at, updated_at;"""
    params = dict(
        title=request.get("title"),
        description=request.get("description"),
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        updated_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, params)
            data = await cur.fetchone()
            return dict(data)


async def put_section(request, section_id):
    query = """
    UPDATE sections 
    SET title = %(title)s, 
        description = %(description)s, 
        updated_at = %(updated_at)s
    WHERE id = %(section_id)s
    RETURNING  id, title, description, created_at, updated_at;"""
    params = dict(
        title=request.get("title"),
        description=request.get("description"),
        updated_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        section_id=section_id
    )
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, params)
            data = await cur.fetchone()
            if data:
                return dict(data)


async def delete_section(section_id):
    query = """
    DELETE FROM posts WHERE id = %(section_id)s"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {"section_id": section_id})
