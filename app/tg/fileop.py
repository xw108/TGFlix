from telethon import events, Button,tl
from .  import utils
from .. import crud
from ..core import CONFIG
            

# ============ file ===============

@events.register(events.NewMessage(incoming=True))
async def new_episode( ev):
    
    if not ev.message.document or ev.message.sticker or ev.message.gif or ev.message.video_note or ev.message.voice or ev.message.audio:
        return


    cId = ev.chat.id
    fn  = str(ev.message.file.name or 'randum')
    mId = ev.message.id

    tdata = await crud.get_tdata( cId)
    if not tdata or tdata['m_id'] is None:
        await ev.reply('No movies data present.upload a movie first')
        raise events.StopPropagation

    movie   = tdata['m_id']
    isS     = tdata['is_series']
    slug    = tdata['slug_base']
    eps     = utils.get_episode( fn) if isS else 1
    ses     = tdata['ses']
    res     = utils.get_resolution( fn)
    fsize   = utils.convert_size( ev.message.file.size)


    if isS:
        slug += f"-S{ ses}"
        if eps != 0:
            slug += f"E{ eps}"
    elif ses > 1:
        slug += f"-part{ ses}"

    if res:
        slug += '-'+res
    
    eId = None
    try:
        eId = await crud.inser_ep_file( cId, mId, eps, slug, movie, ses, res, fsize)
    except Exception:
        pass

    if eId:
        m = f'File added\nId : {eId}\n'
        if isS:
            m += f'Season : {ses}\nEp : {eps}'
        elif ses > 1:
            m += f'Part : {ses}'

        await ev.reply( m)
    else: 
        await ev.reply('something went wrong!')

    raise events.StopPropagation

@events.register(events.NewMessage(incoming=True))
async def new_movie(event):
    if not event.message.message or event.message.document or event.message.sticker or\
        event.message.gif or event.message.video_note or event.message.voice or event.message.audio:
        return
        
    try:
        d = await utils.process_msg_body( event.message.message)
    except Exception as e:
        await event.reply( 'Invalid format')
        raise events.StopPropagation

    cId = event.chat.id
    pId = 1
    isS = True
    
    if event.photo and isinstance( event.photo, tl.types.Photo):
        pId = await crud.inser_photo( cId, event.message.id)

    tdata = await crud.get_tdata( cId)
    if tdata and not tdata['is_series']:
        isS = False

    try:
        s = utils.get_season( d['t'])
        del d['t']
        d['cover_img']  = pId
        d['is_series']  = isS
        r = await crud.insert_movie( d)
        await crud.set_temp_data( cId, r, s, d['slug'] )

        link = CONFIG.APP_URL + '/movie/' + d['slug']
        t = f"{ 'Series ' if isS else 'Movie' } **[{ (d['title']) }]({ link})** added.\nID : __{r}__"
        
        await event.reply( t )
    except Exception as e:

        await event.reply( 'Something went wrong :')
        
        
    raise events.StopPropagation