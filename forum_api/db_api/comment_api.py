import datetime

import aiopg
from psycopg2.extras import DictCursor

from forum_api.db_api.__config import DB_URL


async def get_all_comments(post_id):
    query = """
    SELECT id, post_id, title, level, parent_id, created_at
    FROM public.comments
    WHERE post_id = %(post_id)s
    ORDER BY created_at;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {"post_id": post_id})
            data = await cur.fetchall()
            if data:
                return [dict(u) for u in data]
            return None


async def get_comment_by_id(comment_id):
    query = """
    SELECT id, post_id, title, level, parent_id, created_at 
    FROM public.comments
    WHERE id = %(comment_id)s;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {'comment_id': comment_id})
            data = await cur.fetchone()
            if data:
                return dict(data)
            return None


async def post_comment(request, post_id):
    query = """
    INSERT 
    INTO public.comments (post_id, title, level, parent_id, created_at)
    VALUES (%(post_id)s, %(title)s, %(level)s, %(parent_id)s, %(created_at)s)
    RETURNING  id, post_id, title, level, parent_id, created_at;"""
    params = dict(
        post_id=post_id,
        title=request.get("title"),
        level=request.get("level"),
        parent_id=request.get("parent_id"),
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, params)
            data = await cur.fetchone()
            if data:
                return dict(data)
            return None


async def get_comment_level(parent_id):
    query = """
    SELECT level
    FROM public.comments
    WHERE id = %(parent_id)s;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {'parent_id': parent_id})
            data = await cur.fetchone()
            if data:
                return dict(data)
            return None


async def put_comment(request, comment_id):
    query = """
    UPDATE public.comments 
    SET title = %(title)s, 
        level = %(level)s, 
        parent_id = %(parent_id)s
    WHERE id = %(comment_id)s
    RETURNING  id, post_id, title, level, parent_id, created_at;"""
    params = dict(
        title=request.get("title"),
        level=request.get("level"),
        parent_id=request.get("parent_id"),
        comment_id=comment_id
    )
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, params)
            data = await cur.fetchone()
            if data:
                return dict(data)
            return None


async def delete_comment(comment_id):
    query = """
    DELETE FROM public.comments WHERE id = %(comment_id)s
    RETURNING id;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {"comment_id": comment_id})
            res = await cur.fetchone()
            if res:
                return dict(res)
            return None
