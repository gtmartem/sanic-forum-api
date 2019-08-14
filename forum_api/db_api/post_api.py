import datetime

import aiopg
from psycopg2.extras import DictCursor
from sanic.exceptions import NotFound

from forum_api.db_api.__config import DB_URL


async def get_all_posts(section_id):
    query = """
    SELECT id, section_id, title, description, created_at, updated_at 
    FROM public.posts
    WHERE section_id = %(section_id)s
    ORDER BY updated_at DESC;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {"section_id": section_id})
            data = await cur.fetchall()
            if data:
                return [dict(u) for u in data]
            return None


async def get_posts_by_page(section_id, page_number):
    query = """
    SELECT id, section_id, title, description, created_at, updated_at 
    FROM public.posts
    WHERE section_id = %(section_id)s
    ORDER BY updated_at DESC
    LIMIT %(limit)s OFFSET %(offset)s;"""
    limit = 30
    offset = (page_number - 1) * limit
    params = dict(
        section_id=section_id,
        limit=limit,
        offset=offset
    )
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, params)
            data = await cur.fetchall()
            if data:
                return [dict(u) for u in data]
            return None


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
            return None


async def get_posts_by_search(request):
    query = """
    SELECT public.post.id, 
           public.post.title, 
           public.post.description, 
           public.post.created_at, 
           public.post.updated_at, 
           public.post.section_id,
           1 AS rank
    FROM public.posts_search
    LEFT JOIN public.posts 
    ON public.posts.id = public.posts_search.post_id
    WHERE public.posts_search.title @@ plainto_tsquery(%(search)s)
    ORDER BY rank;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {'search': request.get("search")})
            data = await cur.fetchone()
            if data:
                return dict(data)
            return None


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
    search_query = """
    INSERT 
    INTO public.posts_search (post_id, title)
    VALUES (%(post_id)s, 
            to_tsvector(%(title)s))
    RETURNING post_id;"""
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
            if data:
                serach_params = dict(
                    post_id=data.get("id"),
                    title=data.get("title")
                )
                await cur.execute(search_query, serach_params)
                return dict(data)
            return None


async def put_post(request, post_id):
    query = """
    UPDATE public.posts 
    SET title = %(title)s, 
        description = %(description)s, 
        updated_at = %(updated_at)s
    WHERE id = %(post_id)s
    RETURNING  id, section_id, title, description, created_at, updated_at;"""
    search_query = """
    UPDATE posts_search 
    SET title = to_tsvector(%(title)s)
    WHERE post_id = %(post_id)s;"""
    params = dict(
        title=request.get("title"),
        description=request.get("description"),
        updated_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        post_id=post_id
    )
    search_params = dict(post_id=post_id, title=request.get("title"))
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, params)
            data = await cur.fetchone()
            if data:
                await cur.execute(search_query, search_params)
                return dict(data)
            return None


async def delete_post(post_id):
    query = """
    DELETE FROM public.posts WHERE id = %(post_id)s
    RETURNING id;"""
    search_query = """
    DELETE FROM posts_search WHERE post_id = %(post_id)s;"""
    async with aiopg.connect(DB_URL) as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(query, {"post_id": post_id})
            res = await cur.fetchone()
            if res:
                cur.execute(search_query, {"post_id": post_id})
                return dict(res)
            return None
