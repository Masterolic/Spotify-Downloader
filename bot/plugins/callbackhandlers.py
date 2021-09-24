from pyrogram.errors import UserNotParticipant, FloodWait, QueryIdInvalid
from bot import UPDATES_CHANNEL
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from ..helpers.database import db

@Client.on_callback_query()
async def button(bot: Client, cmd: CallbackQuery):
    cb_data = cmd.data
    if "aboutbot" in cb_data:
        await cmd.message.edit(
            "I do not recommend you downloading song with this bot illegally. But Your if are poor like me then use. -,-\nJust Send Me Link Of Supported Site's.",
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Source Codes of Bot",
                                             url="https://github.com/rozari0")
                    ]
                ]
            )
        )

    elif "refreshForceSub" in cb_data:
        if UPDATES_CHANNEL:
            try:
                user = await bot.get_chat_member(int(UPDATES_CHANNEL), cmd.message.chat.id)
                if user.status == "kicked":
                    await cmd.message.edit(
                        text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/bang_mirror).",
                        parse_mode="markdown",
                        disable_web_page_preview=False
                    )
                    return
                elif user.status != 'kicked' and user.status !='left'and user.status !='left':
                    await cmd.message.edit(
                        text="Hello {}, You are Approve To Use This Bot".format(cmd.message.chat.first_name),
                        parse_mode="Markdown",
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("Support Group", url="https://t.me/bang_mirror"),
                                    InlineKeyboardButton("Bots Channel", url="https://t.me/ProjectRIO"),
                                    InlineKeyboardButton("About Bot",callback_data="aboutbot")
                                ],
                                [
                                    InlineKeyboardButton("Close",callback_data="closeMessage")
                                ]
                            ]
                        )
                    )

            except UserNotParticipant:
                invite_link = await bot.create_chat_invite_link(int(UPDATES_CHANNEL))
                await cmd.message.edit(
                    text="**You Still Didn't Join ☹️, Please Join My Updates Channel to use this Bot!**\n\n"
                         "Due to Overload, Only Channel Subscribers can use the Bot!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshForceSub")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await cmd.message.edit(
                    text="Something went Wrong. Contact my [Support Group](https://t.me/bang_mirror).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
    elif "closeMessage" in cb_data:
        await cmd.message.delete(True)

    try:
        await cmd.answer()
    except QueryIdInvalid:
        pass
