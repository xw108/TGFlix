from sqlalchemy.sql import text
from .. import models
from ..core import db

tb = models.genre

async def get_genre_id( name:str):
    o= await db.fetch_val( tb.select().where( tb.c.slug == name.lower()))
    return o,name.lower()


async def delete_genre_by_id( id:int):
    await db.fetch_val( tb.delete().where( tb.c.id == id))


async def get_all_genres(s,l):
    q = tb.select().order_by( tb.c.name).limit( l).offset( s)
    return await db.fetch_all( q)


async def get_genre_matches( ids):
    if not ids:
        return []
    s = ' OR id = '.join( list( map(str,ids)))
    
    q = tb.select().where( text( f'id = {s};'))
        
    return await db.fetch_all( q)


async def insert_genere( name,slug,desc,url):
    q = tb.insert()
    v = { 'name' : name, 'slug' : slug, 'desc' : desc, 'cover_img' : url}
    return await db.execute(q,v)