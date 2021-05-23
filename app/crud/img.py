from .. import models
from ..core import db

tb = models.img

async def inser_photo(cId,mId):
    
    q = tb.insert()
    v = {'ch_id':cId, 'msg_id' : mId}
    return await db.execute(q,v)


async def get_pic(id:int):
    q = tb.select().where(tb.c.id == id)
    return await db.fetch_one(q)
