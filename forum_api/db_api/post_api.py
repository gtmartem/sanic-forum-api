import datetime

import aiopg
from psycopg2.extras import DictCursor

from forum_api.db_api.__config import DB_URL


async def get_all_posts(section_id):
    query = """
    SELECT id, section_id, title, description, created_at, updated_at 
    FROM public.posts
    WHERE section_id = %(section_id)s;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {"section_id": section_id})
            data = await cur.fetchall()
            return [dict(u) for u in data]


async def get_post_by_id(post_id):
    query = """
    SELECT id, section_id, title, description, created_at, updated_at 
    FROM public.posts
    WHERE id = %(post_id)s;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {'post_id': post_id})
            data = await cur.fetchone()
            if data:
                return dict(data)


async def post_post(request, section_id):
    query = """
    INSERT 
    INTO public.posts (title, section_id, description, created_at, updated_at)
    VALUES (%(title)s, 
            %(section_id)s,
            %(description)s, 
            %(created_at)s, 
            %(updated_at)s)
    RETURNING  id, section_id, title, description, created_at, updated_at;"""
    params = dict(
        section_id=section_id,
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


async def put_post(request, post_id):
    query = """
    UPDATE public.posts 
    SET title = %(title)s, 
        description = %(description)s, 
        updated_at = %(updated_at)s
    WHERE id = %(post_id)s
    RETURNING  id, section_id, title, description, created_at, updated_at;"""
    params = dict(
        title=request.get("title"),
        description=request.get("description"),
        updated_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        post_id=post_id
    )
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, params)
            data = await cur.fetchone()
            if data:
                return dict(data)


async def delete_post(post_id):
    query = """
    DELETE FROM public.posts WHERE id = %(post_id)s;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {"post_id": post_id})