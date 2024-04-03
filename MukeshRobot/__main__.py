import importlib
import re
import time
import asyncio
from platform import python_version as y
from sys import argv
from pyrogram import __version__ as pyrover
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as telever
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tlhver

import MukeshRobot.modules.no_sql.users_db as sql
from MukeshRobot import (
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    OWNER_ID,
    START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)
from MukeshRobot.modules import ALL_MODULES
from MukeshRobot.modules.helper_funcs.chat_status import is_user_admin
from MukeshRobot.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time
PM_START_TEX = """
ʜᴇʟʟᴏ `{}`, ᴀᴘᴀ ᴋᴀʙᴀʀ ᴋᴀᴋ \nᴛᴜɴɢɢᴜ ʙᴇɴᴛᴀʀ ʏᴀ . . . 
"""


PM_START_TEXT = """ 
*ʜᴇʏ* {} 
*ɪ'ᴍ {} ɢᴀ ᴀᴅᴀ ʏᴀɴɢ sᴘᴇsɪᴀʟ sᴀᴍᴀ ᴀᴊᴀ ᴋᴇᴋ ʙᴏᴛ ᴍᴜsɪᴄ ʟᴀᴇɴ
ʙᴏᴛ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇʟᴏʟᴀ ᴅᴀɴ ᴍᴇᴍᴜᴛᴀʀ ᴍᴜꜱɪᴋ
ᴅɪɢʀᴜᴘ ᴀɴᴅᴀ ᴅᴇɴɢᴀɴ ʙᴇʀʙᴀɢᴀɪ ꜰɪᴛᴜʀ*
─────────────────
   *➻ ᴜsᴇʀs »* {}
   *➻ ᴄʜᴀᴛs »* {}
─────────────────
*ᴅᴇᴠ: @Foundermidnight

ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴅɪ ʙᴀᴡᴀʜ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇᴛᴀʜᴜɪ ᴍᴏᴅᴜʟ ᴅᴀɴ ᴄᴏᴍᴍᴀɴᴅꜱ ⚠️*
"""

buttons = [
        [
            InlineKeyboardButton(text="ᴊᴀᴊᴀɴᴀɴ ᴛᴇʟᴇ 📩", callback_data="Music_bot"),
        ],
        [
            InlineKeyboardButton(text="ᴄᴏᴍᴍᴀɴᴅs ⁉️", callback_data="donation_help"),
            InlineKeyboardButton(text="ᴍᴀɴᴀɢᴇᴍᴇɴᴛ 💈", callback_data="mukesh_support"),
        ],
        [
            InlineKeyboardButton(text="ᴅᴇᴠ 👑", callback_data="expert_help"),
            InlineKeyboardButton(text="ᴅᴏɴᴀꜱɪ💰", callback_data="Main_help"),
        ],
    [
        InlineKeyboardButton(
            text="ᴛᴀᴍʙᴀʜ ᴋᴇ ɢᴄ ᴀᴍᴘᴀs ʟᴜ ➕",
            url=f"https://t.me/{dispatcher.bot.username}?startgroup=true",
        ),
    ],
]

HELP_STRINGS = f"""
» *{BOT_NAME}  ᴋʟɪᴋ ᴀᴊᴀ ᴋᴀᴋ ʙᴜᴛᴛᴏɴ ɴʏᴀ ᴋᴀʟᴏ ᴍᴀᴜ ᴛᴀᴜ ᴛᴇɴᴛᴀɴɢ ᴍᴏᴅᴜʟᴇ ᴘᴇʀɪɴᴛᴀʜ ɴʏᴀ*"""

DONATE_STRING = f"""ʜᴇʏ ʙᴀʙʏ,
  ʜᴀᴩᴩʏ ᴛᴏ ʜᴇᴀʀ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴅᴏɴᴀᴛᴇ.

ʏᴏᴜ ᴄᴀɴ ᴅɪʀᴇᴄᴛʟʏ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ @Legend\_coder ғᴏʀ ᴅᴏɴᴀᴛɪɴɢ ᴏʀ ʏᴏᴜ ᴄᴀɴ ᴠɪsɪᴛ ᴍʏ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ @the\_support\_chat ᴀɴᴅ ᴀsᴋ ᴛʜᴇʀᴇ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪᴏɴ."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("MukeshRobot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_photo(
        chat_id=chat_id,
        photo=START_IMG,
        caption=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard,
    )

def start(update: Update, context: CallbackContext):
    args = context.args
    global uptime
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
                    ),
                )
            elif args[0].lower() == "markdownhelp":
                IMPORTED["exᴛʀᴀs"].markdown_help_sender(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rᴜʟᴇs" in IMPORTED:
                IMPORTED["rᴜʟᴇs"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            
            x=update.effective_message.reply_sticker(
                "CAACAgUAAxkBAAI33mLYLNLilbRI-sKAAob0P7koTEJNAAIOBAACl42QVKnra4sdzC_uKQQ")
            x.delete()
            usr = update.effective_user
            lol = update.effective_message.reply_text(
                PM_START_TEX.format(usr.first_name), parse_mode=ParseMode.MARKDOWN
            )
            time.sleep(0.4)
            lol.edit_text("❤")
            time.sleep(0.5)
            lol.edit_text("⚡")
            time.sleep(0.3)
            lol.edit_text("ꜱᴛᴀʀᴛɪɴɢ... ")
            time.sleep(0.4)
            lol.delete()
            
            update.effective_message.reply_photo(START_IMG,PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME,sql.num_users(),sql.num_chats()),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_photo(
            START_IMG,
            caption="ɴᴛ ꭙ͢ ᴛᴜʜᴀɴ ᴀʟɪᴠᴇ ʙᴀʙʏ  !\n<b>ɢᴡ ʙᴇʟᴜᴍ ᴛɪᴅᴜʀ ᴅᴀʀɪ​:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
        )


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "» *ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ​​* *{}* :\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_caption(text,
                parse_mode=ParseMode.MARKDOWN,
                
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="help_back"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/Berlinmusic_support")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass


def Mukesh_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "mukesh_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_caption(f"*ʜᴀɪ ᴍᴇᴋ,*\n  *ɪɴɪ ᴀᴅᴀʟᴀʜ {dispatcher.bot.first_name}*"
            "\n*ʙᴏᴛ ᴍᴀɴᴀɢᴇ + ᴍᴜꜱɪᴄ + ɢᴇɴᴇʀᴀᴛᴇᴅ ꜱᴛʀɪɴɢ*"
            "\n*ʙᴏᴛ ʙɪᴀꜱᴀ ᴀᴊᴀ ꜱᴀᴍᴀ ᴋʏᴋ ʏᴀɴɢ ʟᴀɪɴ.*"
            "\n\n────────────────────"
            f"\n*➥ ᴜᴩᴛɪᴍᴇ »* {uptime}"
            f"\n*➥ ᴜsᴇʀs »* {sql.num_users()}"
            f"\n*➥ ᴄʜᴀᴛs »* {sql.num_chats()}"
            "\n────────────────────"
            "\n*➥ ᴅᴇᴠᴇʟᴏᴘᴇʀ : @Foundermidnight.*"
            f"\n\n*➥ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴅɪ ʙᴀᴡᴀʜ ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ɪɴꜰᴏ ᴛᴇɴᴛᴀɴɢ ᴘᴇɴɢɢᴜɴᴀᴀɴ ʙᴏᴛ {dispatcher.bot.first_name}.*",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
        [
            InlineKeyboardButton(text="ᴊᴀᴊᴀɴᴀɴ ᴛᴇʟᴇ 📩", callback_data="Music_bot"),
        ],
        [
            InlineKeyboardButton(text="ᴄᴏᴍᴍᴀɴᴅs ⁉️", callback_data="donation_help"),
            InlineKeyboardButton(text="ᴍᴀɴᴀɢᴇᴍᴇɴᴛ 💈", callback_data="mukesh_support"),
        ],
        [
            InlineKeyboardButton(text="ᴅᴇᴠ 👑", callback_data="expert_help"),
            InlineKeyboardButton(text="ᴅᴏɴᴀꜱɪ💰", callback_data="Main_help"),
        ],
    [
        InlineKeyboardButton(
            text="➕ ᴛᴀᴍʙᴀʜᴋᴀɴ ɢᴡ ᴋᴇ ɢʀᴏᴜᴘ ʟᴜ ➕",
            url=f"https://t.me/{dispatcher.bot.username}?startgroup=true",
        ),
    ]

]
            ),
        )
    elif query.data == "mukesh_support":
        query.message.edit_caption("**ᴅɪʙᴀᴡᴀʜ ɪɴɪ ʙᴇʙᴇʀᴀᴘᴀ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴅᴀɴ ᴇᴅɪᴛᴏʀ ᴛᴇʟᴇɢʀᴀᴍ [ɴᴛ x ᴛᴜʜᴀɴ](https://t.me/Foundermidnight).**"
            f"\n\nꜱɪʟᴀʜᴋᴀɴ ᴋʟɪᴋ ʙᴜᴛᴛᴏɴ ᴅɪ ʙᴀᴡᴀʜ..",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ᴅᴏɴᴀꜱɪ💰", callback_data="Music_extra"),
                    ],
                    [
                        InlineKeyboardButton(text="ᴍᴀɴᴀɢᴇᴍᴇɴᴛ", callback_data="basic_help"),
                    ],
                    [
                        InlineKeyboardButton(text="ᴏʀᴅᴇʀ ᴠᴠɪᴘ ʙᴏᴋᴇᴘ", callback_data="source_"),
                    ],
                    [
                        InlineKeyboardButton(text="◁ ᴋᴇᴍʙᴀʟɪ", callback_data="mukesh_"),
                    ],
                ]
            ),
        )
    elif query.data == "mukesh_back":
        first_name = update.effective_user.first_name 
        query.message.edit_caption(PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME,sql.num_users(),sql.num_chats()),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
        )
def MukeshRobot_Main_Callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Main_help":
        query.message.edit_caption("**✮ ᴍɪɴɪᴍᴀʟ ɴʏᴜᴍʙᴀɴɢ ʟᴀʜ ᴛᴏᴅ ᴀɢᴀʀ ʙᴏᴛɴʏᴀ ɪᴅᴜᴘ ᴛᴇʀᴜꜱ**" 
        f"\n\nᴋʟɪᴋ ᴀᴊᴀ ʙᴜᴛᴛᴏɴ ᴅᴀɴᴀ ᴅɪʙᴀᴡᴀʜ ᴅɪᴛᴜɴɢɢᴜ ꜱᴜᴍʙᴀɴɢᴀɴʏᴀ..",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ᴅᴀɴᴀ💰", url=f"https://link.dana.id/qr/ag3zovr2"),
                    ],
                    [
                        InlineKeyboardButton(text="◁ ᴋᴇᴍʙᴀʟɪ", callback_data="mukesh_"),
                    ],
                ]
            ),
        )
    elif query.data=="basic_help":
        query.message.edit_caption(
"""✮ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ɪɴɪ ᴅɪ ʙᴜᴀᴛ ʙᴇʀᴛᴜᴊᴜᴀɴ ʜᴀᴠᴇ ꜰᴜɴ ᴅᴀɴ ꜱᴀʟɪɴɢ ᴍᴇʀᴀɴɢᴋᴜʟ, ᴅɪꜱɪɴɪ ɢᴀʙᴀᴅᴀ ʏᴀɴɢ ɴᴀᴍᴀɴʏᴀ ᴘᴇᴛɪɴɢɢɪ" ꜱᴇᴍᴜᴀ ʀᴀᴛᴀ ᴋᴏɴᴛᴏʟ

ʟᴜ ʙɪꜱᴀ ᴊᴏɪɴ ɢʀᴏᴜᴘꜱ ᴅɪʙᴀᴡᴀʜ, ᴋᴀʟᴏ ᴍᴀᴜ ɴɢᴇ ᴀᴅᴍɪɴ ʟᴀɴɢꜱᴜɴɢ ᴘᴄᴘᴄ ᴀᴊᴀ ɴᴛ :
""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ғᴏᴜɴᴅᴇʀ", callback_data="Music_admin"),
                    ],
                    [ 
                        InlineKeyboardButton(text="ᴍɪᴅɴɪɢʜᴛ sᴇx", url=f"https://t.me/+sgGJJiq6lgw0ODA1"),
                        InlineKeyboardButton(text="ɢɪʀʟɴɪɢʜᴛ", url=f"https://t.me/+xWMHhocgchlhMDA1"),
                        InlineKeyboardButton(text="ʜᴇʟʟs ᴀɴɢᴇʟs", url=f"https://t.me/+470sYYvVO3FhYTg1"),
                    ],
                    [
                         InlineKeyboardButton(text="◁ ᴋᴇᴍʙᴀʟɪ", callback_data="Music_"),
                    ],
                ]
            ),
            )
    elif query.data=="mukesh_back":
        query.message.edit_caption("""ᴅɪʙᴀᴡᴀʜ ᴀᴅᴀʟᴀʜ ɴᴀᴍᴀ ɴᴀᴍᴀ ғᴏᴜɴᴅᴇʀ ᴅɪᴍᴀsɪɴɢ" ɢʀᴏᴜᴘ ᴄʜᴀᴛ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ.
        """,parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ɴᴛ", url=f"https://t.me/FounderMidnight"),
                    ],
                    [ 
                        InlineKeyboardButton(text="◁ ᴋᴇᴍʙᴀʟɪ", callback_data="basic_help"),
                    ],
                ]
            ),
            )                                        
    elif query.data=="advance_help":
        query.message.edit_caption("**✮ ᴍɪɴɪᴍᴀʟ ɴʏᴜᴍʙᴀɴɢ ʟᴀʜ ᴛᴏᴅ ᴀɢᴀʀ ʙᴏᴛɴʏᴀ ɪᴅᴜᴘ ᴛᴇʀᴜꜱ**"
        f"\n\nᴋʟɪᴋ ᴀᴊᴀ ʙᴜᴛᴛᴏɴ ᴅᴀɴᴀ ᴅɪʙᴀᴡᴀʜ ᴅɪᴛᴜɴɢɢᴜ ꜱᴜᴍʙᴀɴɢᴀɴʏᴀ..",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ᴅᴀɴᴀ💰", url=f"https://link.dana.id/qr/ag3zovr2"),
                    ],
                    [
                        InlineKeyboardButton(text="◁ ᴋᴇᴍʙᴀʟɪ", callback_data="donation_help"),
                    ],
                ]
            ),
        )
    elif query.data=="expert_help":
        query.message.edit_caption("**ᴋᴀʟᴏ ʙᴏᴛɴʏᴀ ʙᴇʀᴍᴀꜱᴀʟᴀʜ ᴋᴀʟɪᴀɴ ʙɪꜱᴀ ʜᴜʙᴜɴɢɪ ᴋᴏɴᴛᴀᴋ ᴅɪʙᴀᴡᴀʜ ɪɴɪ, ᴏᴋᴇ ᴍᴇᴋ.**"
        f"\n\nᴊᴀɴɢᴀɴ ʟᴜᴘᴀ ᴘᴀᴋᴇ ꜱᴀʟᴀᴍ ᴍᴇᴋ ᴋᴀʟᴏ ᴘᴄ ᴏʀᴀɴɢ ɪᴛᴜ.",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="• ɴᴛ ꭙ͢ ᴛᴜʜᴀɴ ʟᴜ •", url=f"https://t.me/Foundermidnight"),
                        InlineKeyboardButton(text="• ᴀssɪsᴛᴀɴᴛ ɴᴛ •", url=f"https://t.me/FounderGirlnight"),
                    ],
                    [
                        InlineKeyboardButton(text="◁ ᴋᴇᴍʙᴀʟɪ", callback_data="mukesh_"),
                    ]
                ]
            ),
            )
    elif query.data=="donation_help":
        query.message.edit_caption("**ʟᴜ ᴛɪɴɢɢᴀʟ ᴘɪʟɪʜ + ᴋʟɪᴋ ᴍᴀᴜ ᴋᴀᴛᴇɢᴏʀɪ ʏᴀɴɢ ᴍᴀɴᴀ ᴍᴇᴋ, ᴋᴀʟᴏ ʟᴏ ʙɪɴɢᴜɴɢ ᴋᴇ [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ](https://t.me/Berlinmusic_support),**"
            f"\n\nᴋᴀʟᴏ ᴍᴀᴜ ᴅᴏɴᴀꜱɪ ᴋʟɪᴋ ᴀᴊᴀ ʙᴜᴛᴛᴏɴ ᴅᴏɴᴀꜱɪ ʏᴀ.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ᴅᴏɴᴀꜱɪ💰", callback_data="advance_help"),
                    ],
                    [
                        InlineKeyboardButton(text="ᴍᴀɴᴀɢᴇ🗂", callback_data="help_back"),
                        InlineKeyboardButton(text="ᴍᴜꜱɪᴄ🎧", callback_data="Music_play"),
                    ],
                    [
                        InlineKeyboardButton(text="•ᴋᴇᴍʙᴀʟɪ•", callback_data="mukesh_"),
                    ],
                ]
            ),
            )  
def Source_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_caption(
            f"""
𝙻𝙸𝚂𝚃 𝙶𝚁𝚄𝙿 𝚅𝙸𝙿 𝙱𝙾𝙺𝙴𝙿 

𝚃𝙰𝙻𝙴𝙽𝚃 = 50𝙺
𝙸𝙽𝙳𝙾 = 50𝙺
𝙲𝙰𝙼𝙿𝚄𝚁𝙰𝙽 = 50𝚔
𝙱𝙾𝙲𝙸𝙻 = 50𝚔
𝙱𝙳𝚂𝙼 = 50𝙺
𝙷𝙴𝙽𝚃𝙰𝙸 = 50𝙺
𝙿𝙴𝙻𝙰𝙹𝙰𝚁 50𝙺
𝙷𝙸𝙹𝙰𝙱 = 30𝙺
𝙹𝙰𝚅 = 30𝙺 
𝙾𝙼𝙴𝚃𝚅 & 𝙻𝙸𝚅𝙴 𝚂𝚃𝚁𝙴𝙰𝙼𝙸𝙽𝙶 = 30𝙺

𝗣𝗘𝗥𝗣𝗔𝗞𝗘𝗧 ! ! !

𝙿𝙰𝙺𝙴𝚃 𝙲𝙴𝚁𝙸𝙰
250𝙺 7 𝙶𝚁𝚄𝙿
𝚐𝚛𝚞𝚙 𝚒𝚗𝚍𝚘 + 𝚐𝚛𝚞𝚙 𝚝𝚊𝚕𝚎𝚗𝚝

𝙿𝙰𝙺𝙴𝚃 𝙼𝙰𝙽𝙸𝚂
200𝙺 5 𝙶𝚁𝚄𝙿
𝚐𝚛𝚞𝚙 𝚒𝚗𝚍𝚘 + 𝚐𝚛𝚞𝚙 𝚝𝚊𝚕𝚎𝚗𝚝

𝙿𝙰𝙺𝙴𝚃 𝙷𝙾𝙽𝙴𝚈
150𝙺 4 𝙶𝚁𝚄𝙿 
𝚐𝚛𝚞𝚙 𝚒𝚗𝚍𝚘 + 𝚐𝚛𝚞𝚙 𝚝𝚊𝚕𝚎𝚗𝚝

𝙿𝙰𝙺𝙴𝚃 𝙶𝙰𝙽𝚃𝙴𝙽𝙶
100𝙺 3 𝙶𝚁𝚄𝙿 
𝚐𝚛𝚞𝚙 𝚒𝚗𝚍𝚘 + 𝚐𝚛𝚞𝚙 𝚝𝚊𝚕𝚎𝚗𝚝
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="• ᴀᴅᴍɪɴ 1", url=f"https://t.me/Foundermidnight"),
                    ],
                    [
                         InlineKeyboardButton(text="◁ ᴋᴇᴍʙᴀʟɪ", callback_data="mukesh_support"),
                    ]
                ]
            ),
            )          
    elif query.data == "source_back":
        first_name = update.effective_user.first_name
        query.message.edit_caption(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME,sql.num_users(),sql.num_chats()),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            
        )

        
def Music_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Music_":
        query.message.edit_caption("**ᴅɪʙᴀᴡᴀʜ ɪɴɪ ʙᴇʙᴇʀᴀᴘᴀ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴅᴀɴ ᴠᴄs ʀᴇᴀʟ ᴏʀᴛʀᴇs.).**"
        f"\n\nꜱɪʟᴀʜᴋᴀɴ ᴋʟɪᴋ ʙᴜᴛᴛᴏɴ ᴅɪ ʙᴀᴡᴀʜ..",
        
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                         InlineKeyboardButton(text="ᴅᴏɴᴀꜱɪ💰", callback_data="Music_extra"),
                    ],
                    [
                         InlineKeyboardButton(text="ᴍᴀɴᴀɢᴇᴍᴇɴᴛ", callback_data="basic_help"),
                    ],
                    [
                         InlineKeyboardButton(text="ᴏʀᴅᴇʀ ᴠᴠɪᴘ ʙᴏᴋᴇᴘ", callback_data="source_"),
                    ],
                    [
                        InlineKeyboardButton(text="◁ ᴋᴇᴍʙᴀʟɪ", callback_data="mukesh_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_admin":
        query.message.edit_caption("""✮ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ɪɴɪ ᴅɪ ʙᴜᴀᴛ ʙᴇʀᴛᴜᴊᴜᴀɴ ʜᴀᴠᴇ ꜰᴜɴ ᴅᴀɴ ꜱᴀʟɪɴɢ ᴍᴇʀᴀɴɢᴋᴜʟ ᴅɪʙᴀᴡᴀʜ ᴀᴅᴀʟᴀʜ ɴᴀᴍᴀ ɴᴀᴍᴀ ғᴏᴜɴᴅᴇʀ ᴅɪᴍᴀsɪɴɢ" ɢʀᴏᴜᴘ ᴄʜᴀᴛ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ.
        """,parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ɴᴛ", url=f"https://t.me/FounderMidnight"),
                    ],
                    [ 
                        InlineKeyboardButton(text="◁ ᴋᴇᴍʙᴀʟɪ", callback_data="basic_help"),
                    ],
                ]
            ),
            )
    elif query.data == "Music_play":
        query.message.edit_caption(f"*» ᴘʟᴀʏ ᴄᴏᴍᴍᴀɴᴅꜱ «*"
            f"""
/play or /vplay  - ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ʙᴏᴛ ɴʏᴀ ᴅᴀɴ ᴍᴇᴍᴜᴛᴀʀ ᴋᴀɴ ʟᴀɢᴜ ꜱᴇꜱᴜᴀɪ ʏᴀɴɢ ᴅɪ ʀᴇQᴜᴇꜱᴛ ᴋᴀɴ.

/cplay or /cvplay  -  ᴜɴᴛᴜᴋ ᴍᴇᴍᴜᴛᴀʀ ᴍᴜꜱɪᴄ ᴏʀ ᴠɪᴅᴇᴏ ᴅɪ ᴄʜᴀɴɴᴇʟ ʏᴀɴɢ ꜱᴜᴅᴀʜ ᴅɪ ꜱᴀᴍʙᴜɴɢᴋᴀɴ ᴋᴇ ᴅᴀʟᴀᴍ ɢʀᴏᴜᴘ ᴄʜᴀᴛ.

/channelplay [ᴄʜᴀᴛ ᴜꜱᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ] ᴏʀ [ᴅɪꜱᴀʙʟᴇ] - ᴄᴏɴɴᴇᴄᴛ ᴋᴀɴ ᴅᴜʟᴜ ᴄʜᴀɴɴᴇʟ ᴋᴇᴅᴀʟᴀᴍ ɢʀᴏᴜᴘ ʏᴀɴɢ ꜱᴜᴅᴀʜ ᴅɪ ʙᴜᴀᴛ ʟᴀʟᴜ ᴋᴇᴛɪᴋ /ᴄʜᴀɴɴᴇʟᴘʟᴀʏ (ɪᴅ ᴄʜᴀɴɴᴇʟ ᴏʀ ᴜꜱᴇʀɴᴀᴍᴇ ᴄʜᴀɴɴᴇʟ) ᴅɪ ᴅᴀʟᴀᴍ ɢʀᴏᴜᴘꜱ ʏɢ ꜱᴜᴅᴀʜ ᴅɪ ᴋᴀɪᴛᴋᴀɴ ᴋᴇ ᴄʜᴀɴɴᴇʟ ᴛᴇʀꜱᴇʙᴜᴛ..


*ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ*
 ʙᴏᴛ  ꜱᴇʀᴠᴇʀ ᴘʟᴀʏʟɪꜱᴛꜱ:
/playlist  -  ᴄᴇᴋ ᴘʟᴀʏʟɪꜱᴛ ʏᴀɴɢ ꜱᴜᴅᴀʜ ᴅɪ ꜱᴛᴏᴄᴋ ꜱᴇʙᴇʟᴜᴍɴʏᴀ.
/deleteplaylist - ᴍᴇɴɢʜᴀᴘᴜꜱ ᴘʟᴀʏʟɪꜱᴛ ʏᴀɴɢ ꜱᴜᴅᴀʜ ᴅɪ ꜱɪᴍᴘᴀɴ.
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="◁ ᴋᴇᴍʙᴀʟɪ", callback_data="donation_help"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_bot":
        query.message.edit_caption("""» ʙᴇʀɪᴋᴜᴛ ɪɴɪ ᴀᴅᴀʟᴀʜ sᴛᴏʀᴇ JᴀJᴀɴᴀɴ ᴛᴇʟᴇɢʀᴀᴍ + ᴅɪᴀᴍᴏɴᴅ ᴍʟ, ᴋᴀʟɪᴀɴ ᴋʟɪᴋ ᴀJᴀ ʙᴜᴛᴛᴏɴ ᴅɪʙᴀᴡᴀʜ Jɪᴋᴀ ɪɴɢɪɴ ᴍᴇᴍʙᴇʟɪ ᴅɪ sᴛᴏʀᴇ ᴋᴀᴍɪ, ᴛᴇʀɪᴍᴀ ᴋᴀsɪʜ sᴇʟᴀᴍᴀᴛ ʙᴇʀʙᴇʟᴀɴJᴀ.
""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=" sᴛᴏʀᴇ ᴢᴇᴡᴇɴsʏ ", url=f"https://t.me/zewensy"),
                    ],
                    [
                        InlineKeyboardButton(text=" ᴅɪᴀᴍᴏɴᴅ ᴍʟ ", url=f"https://t.me/atnesstore/26"),
                        InlineKeyboardButton(text=" ᴛᴇʟᴘʀᴇᴍ ", url=f"https://t.me/atnesstore/2"),
                    ],
                    [
                        InlineKeyboardButton(text=" ɴᴏᴋᴏs ", url=f"https://t.me/atnesstore/65"),
                        InlineKeyboardButton(text=" ᴜʙᴏᴛ ", url=f"https://t.me/atnesstore/2"),
                    ],
                    [
                        InlineKeyboardButton(text="◁ ᴋᴇᴍʙᴀʟɪ", callback_data="mukesh_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_extra":
        query.message.edit_caption("**✮ ᴍɪɴɪᴍᴀʟ ɴʏᴜᴍʙᴀɴɢ ʟᴀʜ ᴛᴏᴅ ᴀɢᴀʀ ʙᴏᴛɴʏᴀ ɪᴅᴜᴘ ᴛᴇʀᴜꜱ**"
        f"\n\nᴋʟɪᴋ ᴀᴊᴀ ʙᴜᴛᴛᴏɴ ᴅᴀɴᴀ ᴅɪʙᴀᴡᴀʜ ᴅɪᴛᴜɴɢɢᴜ ꜱᴜᴍʙᴀɴɢᴀɴʏᴀ..",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ᴅᴀɴᴀ💰", url=f"https://link.dana.id/qr/ag3zovr2"),
                    ],
                    [
                        InlineKeyboardButton(text="◁ ᴋᴇᴍʙᴀʟɪ", callback_data="Music_"),
                    ],
                ]
            ),
        )
    elif query.data == "Music_back":
        first_name = update.effective_user.first_name
        query.message.edit_caption(PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,

        )


def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_photo(START_IMG,
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=" ʜᴇʟᴘ ​",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_photo(START_IMG,"» Wʜᴇʀᴇ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴏᴘᴇɴ ᴛʜᴇ sᴇᴛᴛɪɴɢs ᴍᴇɴᴜ?.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=" ʙᴜᴋᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ",
                            url="https://t.me/{}?start=help".format(context.bot.username),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text=" ʙᴜᴋᴀ ᴅɪsɪɴɪ",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="◁", callback_data="help_back"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/Berlinmusic_support")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="◁",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text("""Hi there! There are quite a few settings for {} - go ahead and pick what "
                you're interested in.""".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(text=
                """Hi there! There are quite a few settings for {} - go ahead and pick what 
                you're interested in.""".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text("""Hi there! There are quite a few settings for {} - go ahead and pick what 
                you're interested in.""".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ᴛʜɪs ᴄʜᴀᴛ's sᴇᴛᴛɪɴɢs ᴀs ᴡᴇʟʟ ᴀs ʏᴏᴜʀs"
            msg.reply_photo(START_IMG,text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="sᴇᴛᴛɪɴɢs​",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "ᴋʟɪᴋ ᴅɪsɪɴɪ ᴋᴀʟᴏ ʟᴜ ᴍᴀᴜ ᴄᴇᴋ sᴇᴛᴛɪɴɢᴀɴ ʟᴜ"

    else:
        send_settings(chat.id, user.id, True)


def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != 6024180996:
            update.effective_message.reply_text(
                f"» ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴩᴇʀ ᴏғ {dispatcher.bot.first_name} sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ɪs [ɢɪᴛʜᴜʙ](https://github.com/petinggi)"
                f"\n\nʙᴜᴛ ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴅᴏɴᴀᴛᴇ ᴛᴏ ᴛʜᴇ ᴩᴇʀsᴏɴ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴜɴɴɪɴɢ ᴍᴇ : [ʜᴇʀᴇ]({DONATE_STRING})",
                parse_mode=ParseMode.MARKDOWN,
                
            )

    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                
            )

            update.effective_message.reply_text(
                "ɪ'ᴠᴇ ᴘᴍ'ᴇᴅ ʏᴏᴜ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪɴɢ ᴛᴏ ᴍʏ ᴄʀᴇᴀᴛᴏʀ!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ғɪʀsᴛ ᴛᴏ ɢᴇᴛ ᴅᴏɴᴀᴛɪᴏɴ ɪɴғᴏʀᴍᴀᴛɪᴏɴ."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():
    global x
    x=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="➕ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ➕",
                            url="https://t.me/groupcontrollertgbot?startgroup=true"
                            )
                       ]
                ]
                     )
    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.send_photo(
                f"@Berlinmusic_support",
                photo=f"https://telegra.ph//file/3163a7f6a49b9c42e6c52.jpg",
                caption=f"""
✨ɴᴛ ᴍᴀɴᴀɢᴇ ɪs ᴀʟɪᴠᴇ ʙᴀʙʏ.
━━━━━━━━━━━━━
๏ **ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ʙʏ :** [ɴᴛ](tg://user?id=994039943)

๏ ** ғᴏᴜɴᴅᴇʀ :** [ᴍɪᴅɴɪɢʜᴛ](https://t.me/hellsangelsarea)
━━━━━━━━━━━━━
""",reply_markup=x,
                parse_mode=ParseMode.MARKDOWN,
            )
        except Unauthorized:
            LOGGER.warning(
                f"Bot isn't able to send message to @{SUPPORT_CHAT}, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)
    start_handler = CommandHandler("start", start, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(
        help_button, pattern=r"help_.*", run_async=True
    )

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(
        settings_button, pattern=r"stngs_", run_async=True
    )

    about_callback_handler = CallbackQueryHandler(
        Mukesh_about_callback, pattern=r"mukesh_", run_async=True
    )
    source_callback_handler = CallbackQueryHandler(
        Source_about_callback, pattern=r"source_", run_async=True
    )
    music_callback_handler = CallbackQueryHandler(
        Music_about_callback, pattern=r"Music_",run_async=True
    )
    mukeshrobot_main_handler = CallbackQueryHandler(
        MukeshRobot_Main_Callback, pattern=r".*_help",run_async=True)
    donate_handler = CommandHandler("donate", donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(music_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)
    dispatcher.add_handler(mukeshrobot_main_handler)
    dispatcher.add_error_handler(error_callback)
    dispatcher.add_handler(source_callback_handler)
    LOGGER.info("Using long polling.")
    updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
