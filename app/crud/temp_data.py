from .. import models
from ..core import db

tb = models.tempdata

async def set_temp_data( cId, mId, ses,slug):

    q = tb.select().where( tb.c.c_id == cId)
    if await db.execute(q):
        q = tb.update().where( tb.c.c_id == cId)
        v = {'m_id' : mId, 'ses' : ses, 'slug_base' : slug}
        await db.execute(q,v)
    else:
        q = tb.insert()
        v = {'c_id' : cId, 'm_id' : mId, 'ses' : ses, 'slug_base' : slug}
        await db.execute(q,v)


async def set_temp_mdata( cId, mId, slug, isS):
    q = tb.update().where( tb.c.c_id == cId)
    v = {'m_id' : mId, 'is_series' : isS, 'slug_base' : slug}
    await db.execute(q,v)

async def set_temp_m_id( cId, mId:int):
    q = tb.update().where( tb.c.c_id == cId).values( m_id = mId)
    # v = {'c_id' : cId, 'm_id' : mId}
    await db.execute(q)


async def set_temp_m_season( cId, s:int):
    q = tb.update().where( tb.c.c_id == cId).values( ses = s)
    # v = {'c_id' : cId, 'm_id' : mId}
    await db.execute(q)


async def set_temp_m_slug( cId, s:str):
    q = tb.update().where( tb.c.c_id == cId).values( slug_base = s)
    # v = {'c_id' : cId, 'm_id' : mId}
    await db.execute(q)

async def set_temp_is_series( cId, v:bool):
    q = tb.update().where( tb.c.c_id == cId).values( is_series = v)
    # v = {'c_id' : cId, 'm_id' : mId}
    await db.execute(q)

async def get_tdata( cId):
    q = tb.select().where( tb.c.c_id == cId)
    return await db.fetch_one(q)
