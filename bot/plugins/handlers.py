from pyrogram import Client, filters
import aiohttp
from bot import UPDATES_CHANNEL
from ..helpers.force_sub_handler import handle_force_sub
from ..helpers.database import db


@Client.on_message(filters.command('start') & filters.private)
async def start(client, message):
    if UPDATES_CHANNEL is not None:
        back = await handle_force_sub(client, message)
        if back == 400:
            return
    if not db.is_user_exist(message.from_user.id):
        await db.add_user(str(message.from_user.id))
    await message.reply(
        f"**Hello {message.chat.first_name}!**\nSend me spotify or youtube link.\n\n")


@Client.on_message(filters.command('memberlist') & filters.private)
async def memberlist(client,message):
    users = await client.get_chat_members("@ProjectRIO")
    subscribers = []
    for user in users:
        subscribers.append(user['user']['id'])
    if message.from_user['id'] in subscribers:
        print("Oh! Your are in chat.")

@Client.on_message(filters.command('help') & filters.private)
async def help(client, message):
    await message.reply(
        f"**Just Send Me Youtube or Spotify Link! Youtube Music Also Supported.**")
