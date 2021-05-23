from telethon import events, Button,tl
from .  import utils
from .. import crud
from ..core import CONFIG

@events.register(events.ChatAction(func= lambda e: e.user_joined or e.user_added))
async def add_group(ev):


    cId = ev.chat.id
    u =  await ev.get_added_by()
    if not u:
        await ev.reply('I wasnt added proprely,please kick and re-add')
        raise events.StopPropagation
    
    if ( u.id != CONFIG.ADMIN_UID):
        await ev.reply('Only admin should add me.')
        raise events.StopPropagation

    await crud.add_new_channel(cId)
    await ev.reply('I have been added to this channel.From now on i will listen to all the messages')
    msg = f'Added to group [{ ev.chat.title }](tg://openmessage?chat_id={cId})'
    await ev.client.send_message( CONFIG.ADMIN_UID, msg)
    raise events.StopPropagation
    # if ev.user_joined and user_kicked

@events.register(events.ChatAction(func= lambda e: e.user_kicked))
async def remove_group(ev):



    cId = ev.chat.id
    u =  await ev.get_added_by()

    r = await crud.remove_channel(cId)
    
    msg = f'Removed from group [{ ev.chat.title }](tg://openmessage?chat_id={cId})'
    await ev.client.send_message( CONFIG.ADMIN_UID, msg)
    # await ev.reply('I have been added to this channel.From now on i will listen to all the messages')
    raise events.StopPropagation