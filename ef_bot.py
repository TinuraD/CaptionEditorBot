from pyrogram import Client
from pyrogram import filters
from pyrogram import idle, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import Message
from pyrogram.errors import RPCError
import functools
from config import API_HASH, API_ID, BOT_TOKEN

bot = Client('EF-Caption',
                  api_id=var.API_ID,
                  api_hash=var.API_HASH,
                  bot_token=var.BOT_TOKEN)

def is_admin(func):
    @functools.wraps(func)
    async def oops(client,message):
        is_admin = False
        try:
            user = await message.chat.get_member(message.from_user.id)
            admin_strings = ("creator", "administrator")
            if user.status not in admin_strings:
                is_admin = False
            else:
                is_admin = True

        except ValueError:
            is_admin = True
        if is_admin:
            await func(client,message)
        else:
            await message.reply("Only Admins can execute this command!")
    return oops

def get_text(message: Message) -> [None, str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@bot.on_message(
    filters.command("send") & ~filters.edited & ~filters.bot)
@is_admin
async def send(client, message):
    if message.reply_to_message:
            reply = message.reply_to_message
            try:
                await reply.copy(message.chat.id)
            except RPCError as i:
                await message.reply(i)
                return

    else:
        args = get_text(message)
        await client.send_message(message.chat.id, text=args)

@bot.on_message(filters.private & ~filters.command(["start","help","edit"]))
async def copy(client, message):
    try:
        await message.copy(message.chat.id)
    except RPCError as i:
        await message.reply(i)
        return

@bot.on_message(
    filters.command("edit") & ~filters.edited & ~filters.bot)
@is_admin
async def loltime(client, message):
    lol = await message.reply("Processing please wait")
    cap = get_text(message)
    if not message.reply_to_message:
        await lol.edit("reply to any message to edit caption")
    reply = message.reply_to_message
    try:
        await reply.copy(message.chat.id,caption= cap)
        await lol.delete()
    except RPCError as i:
        await lol.edit(i)
        return

@bot.on_message(filters.command(["start"]))
async def start(client, message):
    await message.reply_text(
        text=f"I'm [Caption Editor](https://t.me/efcapeditbot) bot. I can edit captions of any media and anonymize any message. Use /help to know more.",
        disable_web_page_preview=False,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Join Group", url="https://t.me/slplatform"),
                    InlineKeyboardButton("Join Channel", url="https://t.me/efbots")
                ]
            ]
        ),
    )  

@bot.on_message(
    filters.command("help") & filters.private & ~filters.edited & ~filters.bot)    
async def hulp(client, message):
    lol = await message.reply("""
Caption Editor Help ❔

 • Forward or send any message to me, I will send it without forward tag.
 • /send <text> - Send Messages like me.
 • /send <reply> - I will send replied message.
 • /edit <caption> <reply to media> - I will edit caption of replied media

Note 📝
• In pm above message works for everyone.
• In a group, above commands only work for only admins.
""")

@bot.on_message(
    filters.command("help") & ~filters.private & ~filters.edited & ~filters.bot)    
async def help(client, message):
    lol = await message.reply("Send /help in my inbox to get help 😁")

bot.start()
idle()
