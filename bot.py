# =========================================
# TELEGRAM ADVANCED GROUP MANAGER BOT
# FULL VERSION
# =========================================

# INSTALL:
# pip install python-telegram-bot==20.7

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from telegram.constants import (
    ChatPermissions,
    ChatMemberStatus,
)

import asyncio
import re

# =========================================
# BOT TOKEN
# =========================================

TOKEN = "8927671568:AAEIs-A6sS3H2KljAHpQ3hBvwYyYhnobPUo"

# =========================================
# DATABASE MEMORY
# =========================================

warnings_db = {}
group_lang = {}
afk_users = {}

# =========================================
# MULTI LANGUAGE
# =========================================

LANG = {

    "vi": {

        "menu": "📌 MENU QUẢN TRỊ",

        "link_deleted":
        "🚫 Bạn không được gửi link trong nhóm.",

        "muted":
        "🔇 Đã mute",

        "unmuted":
        "🔊 Đã mở mute",

        "banned":
        "⛔ Đã ban",

        "warn":
        "⚠️ Cảnh cáo",

        "autoban":
        "🚫 Đã tự động ban vì đủ 3 cảnh cáo.",

        "resetwarn":
        "✅ Đã reset cảnh cáo.",

        "welcome":
        "👋 Chào mừng bạn đến nhóm!",

        "afk":
        "💤 Đã bật AFK",

        "afk_off":
        "✅ Đã tắt AFK",

        "lang_changed":
        "🌍 Đã đổi ngôn ngữ",

    },

    "en": {

        "menu": "📌 ADMIN MENU",

        "link_deleted":
        "🚫 You cannot send links here.",

        "muted":
        "🔇 Muted",

        "unmuted":
        "🔊 Unmuted",

        "banned":
        "⛔ Banned",

        "warn":
        "⚠️ Warning",

        "autoban":
        "🚫 Auto banned after 3 warnings.",

        "resetwarn":
        "✅ Warnings reset.",

        "welcome":
        "👋 Welcome to the group!",

        "afk":
        "💤 AFK enabled",

        "afk_off":
        "✅ AFK disabled",

        "lang_changed":
        "🌍 Language changed",

    }
}

# =========================================
# GET LANG
# =========================================

def get_lang(chat_id):
    return group_lang.get(chat_id, "vi")

# =========================================
# START
# =========================================

async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 Advanced Manager Bot Online"
    )

# =========================================
# MENU
# =========================================

async def menu(update: Update,
               context: ContextTypes.DEFAULT_TYPE):

    lang = get_lang(update.effective_chat.id)

    keyboard = [

        [
            InlineKeyboardButton(
                "🔇 Mute",
                callback_data="mute"
            ),

            InlineKeyboardButton(
                "🔊 Unmute",
                callback_data="unmute"
            )
        ],

        [
            InlineKeyboardButton(
                "⛔ Ban",
                callback_data="ban"
            ),

            InlineKeyboardButton(
                "⚠️ Warn",
                callback_data="warn"
            )
        ],

        [
            InlineKeyboardButton(
                "🌍 Language",
                callback_data="lang"
            ),

            InlineKeyboardButton(
                "💤 AFK",
                callback_data="afk"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(
        keyboard
    )

    await update.message.reply_text(
        LANG[lang]["menu"],
        reply_markup=reply_markup
    )

# =========================================
# CALLBACK BUTTON
# =========================================

async def button_handler(update: Update,
                         context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        f"✅ Button: {query.data}"
    )

# =========================================
# AUTO DELETE LINKS
# ONLY ADMIN CAN SEND LINKS
# =========================================

async def auto_delete_links(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    if not update.message.text:
        return

    text = update.message.text

    link_pattern = (
        r"(https?://\S+|"
        r"t\.me/\S+|"
        r"www\.\S+)"
    )

    if re.search(link_pattern, text):

        member = await context.bot.get_chat_member(
            update.effective_chat.id,
            update.effective_user.id
        )

        if member.status in [
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ]:
            return

        await asyncio.sleep(1)

        try:

            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=update.message.message_id
            )

            lang = get_lang(
                update.effective_chat.id
            )

            await update.effective_chat.send_message(
                LANG[lang]["link_deleted"]
            )

        except:
            pass

# =========================================
# MUTE
# =========================================

async def mute(update: Update,
               context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        return

    user = update.message.reply_to_message.from_user

    permissions = ChatPermissions(
        can_send_messages=False
    )

    await context.bot.restrict_chat_member(
        chat_id=update.effective_chat.id,
        user_id=user.id,
        permissions=permissions
    )

    lang = get_lang(update.effective_chat.id)

    await update.message.reply_text(
        f"{LANG[lang]['muted']} "
        f"{user.first_name}"
    )

# =========================================
# UNMUTE
# =========================================

async def unmute(update: Update,
                 context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        return

    user = update.message.reply_to_message.from_user

    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True
    )

    await context.bot.restrict_chat_member(
        chat_id=update.effective_chat.id,
        user_id=user.id,
        permissions=permissions
    )

    lang = get_lang(update.effective_chat.id)

    await update.message.reply_text(
        f"{LANG[lang]['unmuted']} "
        f"{user.first_name}"
    )

# =========================================
# BAN
# =========================================

async def ban(update: Update,
              context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        return

    user = update.message.reply_to_message.from_user

    await context.bot.ban_chat_member(
        chat_id=update.effective_chat.id,
        user_id=user.id
    )

    lang = get_lang(update.effective_chat.id)

    await update.message.reply_text(
        f"{LANG[lang]['banned']} "
        f"{user.first_name}"
    )

# =========================================
# WARN SYSTEM
# =========================================

async def warn(update: Update,
               context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        return

    user = update.message.reply_to_message.from_user

    user_id = user.id

    if user_id not in warnings_db:
        warnings_db[user_id] = 0

    warnings_db[user_id] += 1

    count = warnings_db[user_id]

    lang = get_lang(update.effective_chat.id)

    if count >= 3:

        await context.bot.ban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id
        )

        await update.message.reply_text(
            f"{user.first_name} "
            f"{LANG[lang]['autoban']}"
        )

        warnings_db[user_id] = 0

    else:

        await update.message.reply_text(
            f"{LANG[lang]['warn']} "
            f"{count}/3"
        )

# =========================================
# RESET WARN
# =========================================

async def resetwarn(update: Update,
                    context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        return

    user = update.message.reply_to_message.from_user

    warnings_db[user.id] = 0

    lang = get_lang(update.effective_chat.id)

    await update.message.reply_text(
        LANG[lang]["resetwarn"]
    )

# =========================================
# SET LANGUAGE
# =========================================

async def setlang(update: Update,
                  context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 1:

        await update.message.reply_text(
            "/setlang vi\n"
            "/setlang en"
        )

        return

    lang = context.args[0]

    if lang not in LANG:
        return

    group_lang[
        update.effective_chat.id
    ] = lang

    await update.message.reply_text(
        LANG[lang]["lang_changed"]
    )

# =========================================
# AFK
# =========================================

async def afk(update: Update,
              context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    afk_users[user_id] = True

    lang = get_lang(update.effective_chat.id)

    await update.message.reply_text(
        LANG[lang]["afk"]
    )

# =========================================
# REMOVE AFK
# =========================================

async def remove_afk(update: Update,
                     context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id in afk_users:

        del afk_users[user_id]

        lang = get_lang(
            update.effective_chat.id
        )

        await update.message.reply_text(
            LANG[lang]["afk_off"]
        )

# =========================================
# WELCOME NEW MEMBER
# =========================================

async def welcome(update: Update,
                  context: ContextTypes.DEFAULT_TYPE):

    lang = get_lang(update.effective_chat.id)

    for user in update.message.new_chat_members:

        await update.message.reply_text(
            f"{LANG[lang]['welcome']} "
            f"{user.first_name}"
        )

# =========================================
# MAIN
# =========================================

app = ApplicationBuilder().token(
    TOKEN
).build()

# COMMANDS

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("menu", menu)
)

app.add_handler(
    CommandHandler("mute", mute)
)

app.add_handler(
    CommandHandler("unmute", unmute)
)

app.add_handler(
    CommandHandler("ban", ban)
)

app.add_handler(
    CommandHandler("warn", warn)
)

app.add_handler(
    CommandHandler("resetwarn", resetwarn)
)

app.add_handler(
    CommandHandler("setlang", setlang)
)

app.add_handler(
    CommandHandler("afk", afk)
)

# BUTTONS

app.add_handler(
    CallbackQueryHandler(button_handler)
)

# AUTO LINK DELETE

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        auto_delete_links
    )
)

# REMOVE AFK WHEN USER TALKS

app.add_handler(
    MessageHandler(
        filters.TEXT,
        remove_afk
    )
)

# WELCOME

app.add_handler(
    MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        welcome
    )
)

# =========================================
# RUN BOT
# =========================================

print("BOT ONLINE")

app.run_polling()
