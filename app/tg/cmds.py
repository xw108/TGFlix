from telethon import events, Button,tl
from .  import utils
from .. import crud
from ..core import CONFIG
            


# =============cmds=================
@events.register( events.NewMessage(pattern='/ism'))
async def set_as_movie(m):
    cId = m.chat.id
    await crud.set_temp_is_series( cId, False)
    await m.reply( 'Done, You can upload movies now')
    raise events.StopPropagation

@events.register( events.NewMessage(pattern='/iss'))
async def set_as_series(m):
    cId = m.chat.id
    await crud.set_temp_is_series( cId, True)
    await m.reply( 'Done, You can upload series now')
    raise events.StopPropagation

@events.register( events.NewMessage(pattern='/(s|p)\s?(\d+)'))
async def set_season(m):
    cId = m.chat.id
    ses = int( m.pattern_match.group(2))
    if ses < 1:
        await m.reply( f'Season or part should be valid')
        raise events.StopPropagation

    await crud.set_temp_m_season( cId, ses)
    await m.reply( f'Done, You can upload season{ses} or part{ses}')
    raise events.StopPropagation

@events.register( events.NewMessage(pattern='/set\s?(\d+)'))
async def set_movie_id(m):
    cId = m.chat.id
    mId = int( m.pattern_match.group( 1))
    if mId < 1:
        await m.reply( f'Invalid movie id')
        raise events.StopPropagation

    mov = await crud.get_movie_by_id( mId)
    if not mov:
        await m.reply( f'Invalid movie id')
        raise events.StopPropagation

    await crud.set_temp_mdata( cId, mov['id'], mov['slug'],mov['is_series'] )
    await m.reply( f'Done, You can upload **{ mov["title"]}**')
    await info(m)
    raise events.StopPropagation

# set movie visibility
@events.register( events.NewMessage(pattern='/m(hide|show)\s?(\d+)'))
async def toogle_movie_visibility(m):
    cId = m.chat.id
    mId = int( m.pattern_match.group( 2))
    if mId < 1:
        await m.reply( f'Invalid movie id')
        raise events.StopPropagation

    mov = await crud.get_movie_by_id( mId)
    if not mov:
        await m.reply( f'Invalid movie id')
        raise events.StopPropagation
    hide = m.pattern_match.group( 1) == 'hide'

    await crud.set_movie_visibility(mov['id'], hide)
    await m.reply( f"Done, **{ mov['title']}** is now { 'hidden' if hide else 'visible'}.")
    raise events.StopPropagation

# set episode visibility
@events.register( events.NewMessage(pattern='/e(hide|show)\s?(\d+)'))
async def toogle_file_visibility(m):
    cId = m.chat.id
    mId = int( m.pattern_match.group( 2))
    if mId < 1:
        await m.reply( f'Invalid file id')
        raise events.StopPropagation

    epf = await crud.get_epfile_by_id( mId)
    if not epf:
        await m.reply( f'Invalid file id')
        raise events.StopPropagation

    hide = m.pattern_match.group( 1) == 'hide'

    await crud.set_epfile_visibility(epf['id'], hide)
    await m.reply( f"Done, **File** is now { 'hidden' if hide else 'visible'}.")
    raise events.StopPropagation

# get curent upload info for channel
@events.register( events.NewMessage(pattern='/info'))
async def info(m):
    cId = m.chat.id
    r   = await crud.get_tdata( cId)
    if r:
        d = await crud.get_movie_by_id(r['m_id'])
        t = f"In progress\n{ 'Series ' if r['is_series'] else 'Movie' } **{ (d['title']) }**.\nID : __{d['id']}__\nHidden : { 'Yep' if d['hide'] else 'Nope'}"

        if r['ses']:
            t += f"\n{'Season' if r['is_series'] else 'Part'} : **{r['ses']}**"
    else:
        t = 'Nothing in progress'
    await m.reply(t)
    raise events.StopPropagation

# delete episode file
@events.register( events.NewMessage(pattern='/edel\s?(\d+)'))
async def delete_file(m):
    cId = m.chat.id
    fId = int( m.pattern_match.group( 1))
    if fId < 1:
        await m.reply( f'Invalid file id')
        raise events.StopPropagation
        
    epf = await crud.get_epfile_by_id( fId)
    if not epf:
        await m.reply( f'Invalid file id')
        raise events.StopPropagation
    
    b = [ Button.inline('Proceed',f'E{fId}'), Button.inline('Cancel','no') ]
    await m.reply( 'Are you sure to delete this file?',buttons=b)
    raise events.StopPropagation

# delete movie
@events.register( events.NewMessage(pattern='/mdel\s?(\d+)'))
async def delete_movie(m):
    cId = m.chat.id
    mId = int( m.pattern_match.group( 1))
    if mId < 1:
        await m.reply( f'Invalid movie id')
        raise events.StopPropagation
        
    mov = await crud.get_movie_by_id( mId)
    if not mov:
        await m.reply( f'Invalid movie id')
        raise events.StopPropagation
    
    b = [ Button.inline('Proceed',f'M{mId}'), Button.inline('Cancel','no') ]
    await m.reply( f'Are you sure to delete **{ mov["title"] }**?\nall the associated files and images will be deleted too.',buttons=b)
    raise events.StopPropagation

# insert genere
@events.register( events.NewMessage(pattern='^/genre'))
async def new_genere( ev):
    if ev.message.document or ev.message.sticker or ev.message.gif or ev.message.video_note or ev.message.voice or ev.message.audio:
        await ev.reply( f'Only images allowed')
        raise events.StopPropagation

    cId = ev.chat.id
    pId = 1
    haveImg = False
    if ev.photo and isinstance( ev.photo, tl.types.Photo):
        pId = await crud.inser_photo( cId, ev.message.id)
        haveImg = True
    
    try:
        name,slug,desc,url  = utils.proc_genere_body( ev.message.message, haveImg)
    except Exception as e:
        await ev.reply( 'Invalid Genere format')
        raise events.StopPropagation

    c,s = await crud.get_genre_id( slug)

    if c:
        await ev.reply( 'Genere already exists in db')
        raise events.StopPropagation


    if haveImg:
        url = f'/file/img/{pId}.jpg'

    gId     = await crud.insert_genere( name,slug,desc,url)
    link    = CONFIG.APP_URL + '/genere/' + slug

    await ev.reply( f'New Genere [{name}]({link}) Added\nId : {gId}')
    raise events.StopPropagation

@events.register( events.NewMessage(pattern='^/gdel (\w+)$'))
async def delete_genere( ev):
    g  = str( ev.pattern_match.group( 1).strip().lower())
    c,s = await crud.get_genre_id( g)
    if not c:
        await ev.reply( f'Invalid genere')
        raise events.StopPropagation

    await crud.delete_genre_by_id( c)
    await ev.reply( f'Genere deleted')
    raise events.StopPropagation
