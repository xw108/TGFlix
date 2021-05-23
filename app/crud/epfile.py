from .. import models
from ..core import db

tb = models.epFile

async def check_slug_exists(s):
    q = tb.select().where( tb.c.slug == s)
    return await db.fetch_one(q)


async def inser_ep_file(cId,mId,eps, slug,movie, ses, res = None, size = None):
    i = 0
    ts = slug
    while True:
        if not await check_slug_exists( slug):
            break
        i += 1
        slug = ts + '-' + str(i)
        

    q = tb.insert()
    v = { 'msg_id' : mId, 'ch_id' : cId, 'eps' : eps , 'size' : size,
         'slug' : slug, 'movie_id' : movie, 'ses' : ses, 'qlty' : res}
    return await db.execute(q,v)


async def get_movie_seasons(mId):
    # return None
    q = '''SELECT ses , COUNT( DISTINCT eps) as ep_count FROM files 
        WHERE movie_id = :movie_id 
        GROUP BY ses ORDER BY ses ASC ;'''
    return await db.fetch_all( ( q), values= { 'movie_id' : mId})


async def get_movie_parts(mId):
    # q = tb.select( columns= 'eps').where(tb.c.ses == 0).where( tb.c.movie_id == mId)
    q = '''SELECT ses , COUNT( DISTINCT qlty) + (CASE bool_or(qlty is null) WHEN true THEN 1 ELSE 0 END) 
            as ep_count FROM files
            WHERE eps = 1 AND movie_id = :movie_id 
            GROUP BY ses ORDER BY ses ASC;'''
    return await db.fetch_all( q, values= { 'movie_id' : mId})

async def get_movie_episodes(mId, ses):
    q = '''SELECT eps , COUNT( DISTINCT qlty) + (CASE bool_or(qlty is null) WHEN true THEN 1 ELSE 0 END) as res_count FROM files
            WHERE movie_id = :movie_id AND ses = :ses AND hide = false
            GROUP BY eps ORDER BY eps ASC;'''
    return await db.fetch_all( q, values= { 'movie_id' : mId, 'ses' : ses})

async def get_movie_episode_files(mId,s,e):
    q = tb.select().where( tb.c.movie_id == mId )\
            .where( tb.c.ses == s)\
            .where( tb.c.eps == e)\
            .order_by( tb.c.size.desc(),tb.c.qlty.desc())
    return await db.fetch_all( q)

async def get_epfile_by_id( id):
    q = tb.select().where( tb.c.id == id)
    return await db.fetch_one(q)

async def get_epfile_by_slug( s):
    q = tb.select().where( tb.c.slug == s).where( tb.c.hide == False)
    return await db.fetch_one(q)


async def set_epfile_visibility( id, hide = False):
    q = tb.update().where( tb.c.id == id).values(hide = hide)
    return await db.execute(q)


async def delete_ep_file( id):
    q = tb.delete().where( tb.c.id == id)
    await db.execute(q)