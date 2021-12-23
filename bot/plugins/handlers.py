from pyrogram import Client, filters
import aiohttp
from bot import LOG_GROUP,UPDATES_CHANNEL
from ..helpers.force_sub_handler import handle_force_sub
from ..helpers.database import db


@Client.on_message(filters.command('start') & filters.private)
async def start(client, message):
    if UPDATES_CHANNEL is not None:
        back = await handle_force_sub(client, message)
        if back == 400:
            return
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(str(message.from_user.id))
    await message.reply(
        f"**Hello {message.chat.first_name}!**\nSend me Spotify, Deezer, JioSaavn or Youtube link.\n\n")

@Client.on_message(filters.command('help') & filters.private)
async def help(client, message):
    await message.reply(
        '**Just Send Me Spotify, Deezer, JioSaavn Youtube or Youtube Music Link!**'
    )
