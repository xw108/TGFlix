from .. import models
from ..core import db

tb = models.tgchannel

async def is_channel_allowed( id):
    q = tb.select().where( tb.c.channel_id == id)
    return await db.execute(q)

async def add_new_channel( id:int):
    q = tb.insert()
    v = { 'channel_id':id}
    return await db.execute(q,v)

async def remove_channel( id:int):
    q = tb.delete().where( tb.c.channel_id == id)
    return await db.execute(q)
