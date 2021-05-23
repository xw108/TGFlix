from sqlalchemy import  any_,text
from .. import models
from ..core import db

tb = models.movies

async def check_mslug_exists( s):
    q = tb.select().where( tb.c.slug == s)
    return await db.fetch_one(q)


async def insert_movie( v):
    i = 0
    ts = v['slug']
    while True:
        if not await check_mslug_exists( v['slug']):
            break
        i += 1
        v['slug'] = ts + '_' + str(i)
    q = tb.insert()
    return await db.execute(q,v)


async def get_movies( s,l):

    q = tb.select().where( tb.c.hide == False).offset(s)\
        .where( tb.c.is_series ==  False)\
        .limit(l).order_by( tb.c.title.asc())
    return await db.fetch_all(q)



async def get_all_by_genre( id:int,s:int,l:int):
    q = tb.select().where( tb.c.hide == False)\
        .where(id == any_(tb.c.genre))\
        .offset(s).limit(l).order_by( tb.c.title.asc())
    return await db.fetch_all(q)


async def get_movies_by_genre( id:int,s:int,l:int):

    q = tb.select().where( tb.c.hide == False).where(id == any_(tb.c.genre))\
        .offset(s).limit(l).order_by( tb.c.title.asc())
    return await db.fetch_all(q)

async def get_movie_by_slug( s):
    q = tb.select().where( tb.c.slug == s).where( tb.c.hide == False)\
        .where( tb.c.is_series ==  False)
    return await db.fetch_one(q)

async def get_series( s,l):

    q = tb.select().where( tb.c.hide == False).offset(s)\
        .where( tb.c.is_series ==  True)\
        .limit(l).order_by( tb.c.title.asc())
    return await db.fetch_all(q)

async def get_series_by_slug( s):
    q = tb.select().where( tb.c.slug == s).where( tb.c.hide == False)\
        .where( tb.c.is_series ==  True)
    return await db.fetch_one(q)

async def get_movie_by_id( id:int):
    q = tb.select().where( tb.c.id == id)
    return await db.fetch_one(q)

async def set_movie_visibility( mId:int, hide = False):
    q = tb.update().where( tb.c.id == mId).values(hide = hide)
    await db.execute( q)

async def delete_movie( id):
    q = tb.delete().where( tb.c.id == id)
    await db.execute(q)

async def search_movies(title,s,l):
    import re
    title = re.sub('(!|#|$|&|<|>|;|:)','',title)
    q = "SELECT * FROM movies WHERE to_tsvector( title) @@ to_tsquery(  :title) \
        ORDER BY title OFFSET :skip LIMIT :limt;"
    v = {'title':title, 'skip': s,'limt':l}
    return await db.fetch_all(q,v)