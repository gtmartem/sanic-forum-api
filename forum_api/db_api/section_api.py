import aiopg
from psycopg2.extras import DictCursor

DB_URL = 'postgresql://postgres:0a610292api@127.0.0.1:5430/forum'


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
