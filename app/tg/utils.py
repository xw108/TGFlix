import re
from app import crud


async def proc_categories(c):
    il = []
    for i in c:
        id, n = await crud.get_genre_id( i)
        if id:
            il.append( int( id))
    return il         

async def process_msg_body( msg:str):
    msg     = msg.split('|')
    
    if len( msg) != 3:
        raise Exception
    t   = msg[0].strip()
    title = remove_season( t)
    cid  = await proc_categories( msg[1].strip().split(','))
    desc    = msg[2].strip()
    slug =  make_slu_base( title)
    return {'title' : title, 'genre' : cid, 'desc' : desc, 'slug' : slug, 't' : t}

def proc_genere_body( msg, haveImg = False):
    
    msg     = msg.replace('/genre','').split('|')
    
    if (haveImg and (len( msg) <= 1)):
        raise Exception
    if (not haveImg and (len( msg) != 3)):
        raise Exception
        
    name    = msg[0].strip()
    slug    = name.lower()
    desc    = msg[1].strip()
    url     = None if haveImg else msg[2].strip()

    return name, slug, desc, url

def get_season(title:str):
    m = re.search('(?i)[\s\.\-_,/](s|season|part)\s?\d+', title)
    if m:
        return int( re.search('\d+', m.group( 0)).group( 0))
    return 1

def get_episode(n:str):
    m = re.search('(?i)[\s\.\-_,0-9](e|episode)\s?\d+', n)
    if m:
        return int( re.search('\d+', m.group( 0)).group( 0))
    return 1

def remove_season(t):
    return re.sub(r'(?i)[\s\.\-_,]+(s|season|part)\s?\d+','',t).strip()


def make_slu_base(t):
    t = t.lower().strip()
    t = re.sub(r'\s+','_',t).strip()
    t = re.sub(r'[^a-zA-Z0-9_]+','_',t).strip()
    t = re.sub(r'(^_+|_+$)','',t).strip()
    return t
    
def get_resolution( t):
    r = re.search('(144|240|360|480|540|720|1080)p',t)
    return r.group( 0) if r else None


async def is_allowed_grp(ev)->bool:
    return bool(ev.is_group and await crud.is_channel_allowed( ev.chat.id))

def convert_size(s:int ,):
    s,e = round(s/(1024*1024),1),' MB'
    if s > 1023:
        s,e = round(s/(1024),1),' GB'
    return str(s)+e