from telethon import events, Button,tl
from .  import utils
from .. import crud
            

# ==========calbacks==============

@events.register( events.CallbackQuery(pattern='M(\d+)'))
async def delete_movie_cb(m):
    mId = int(m.pattern_match.group( 1))
    
    await crud.delete_movie(mId)
    await m.edit( 'Movie/Series Deleted',buttons= Button.clear())
    raise events.StopPropagation

@events.register( events.CallbackQuery(pattern='E(\d+)'))
async def delete_epfile_cb(m):
    fId = int(m.pattern_match.group( 1))
    
    await crud.delete_ep_file(fId)
    await m.edit( 'File deleted',buttons= Button.clear())
    raise events.StopPropagation

@events.register( events.CallbackQuery(pattern='no'))
async def cancel_cb(m):
    await m.edit( 'Canceled',buttons= Button.clear())
    raise events.StopPropagation

