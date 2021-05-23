from telethon import TelegramClient,events, Button,tl,utils as tu
from telethon.sessions import StringSession
from typing import Union
from app.core import CONFIG
from .utils import is_allowed_grp

client = TelegramClient(  StringSession( CONFIG.SESSION_STRING), CONFIG.TG_APP_ID, CONFIG.TG_APP_HASH)
client.parse_mode = 'md'


AllEv = Union[events.ChatAction,events.NewMessage,events.CallbackQuery]


@client.on(events.NewMessage)
async def dn_ensure_its_allowed_grp(ev):
    print('New message')
    if not await is_allowed_grp( ev):
        raise events.StopPropagation

@client.on(events.CallbackQuery)
async def cb_ensure_its_allowed_grp(ev):
    print('New Callback')
    if not await is_allowed_grp( ev):
        raise events.StopPropagation


# update
from .updates import ( add_group,remove_group)

client.add_event_handler( add_group)
client.add_event_handler( remove_group)

# callbacks
from .callbacks import delete_epfile_cb,delete_movie_cb,cancel_cb

client.add_event_handler( delete_epfile_cb)
client.add_event_handler( delete_movie_cb)
client.add_event_handler( cancel_cb)



from .cmds import (
    set_as_movie,
    set_as_series,
    set_movie_id,
    set_season,
    delete_file,
    delete_genere,
    delete_movie,
    toogle_file_visibility,
    toogle_movie_visibility,
    info,
    new_genere,
)

client.add_event_handler( set_as_movie)
client.add_event_handler( set_as_series)
client.add_event_handler( set_movie_id)
client.add_event_handler( set_season)
client.add_event_handler( delete_file)
client.add_event_handler( delete_genere)
client.add_event_handler( delete_movie)
client.add_event_handler( toogle_file_visibility)
client.add_event_handler( toogle_movie_visibility)
client.add_event_handler( info)
client.add_event_handler( new_genere)



from .fileop import new_episode,new_movie

client.add_event_handler( new_episode)
client.add_event_handler( new_movie)
