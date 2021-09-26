# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import re

from telethon.utils import get_display_name

from userbot import catub

from ..core.managers import edit_or_reply
from ..sql_helper import blacklist_sql as sql
from ..utils import is_admin

plugin_category = "admin"


@catub.cat_cmd(incoming=True, groups_only=True)
async def on_new_message(event):
    name = event.raw_text
    snips = sql.get_chat_blacklist(event.chat_id)
    catadmin = await is_admin(event.client, event.chat_id, event.client.uid)
    if not catadmin:
        return
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            try:
                await event.delete()
            except Exception:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"**⌔︙ ليس لدي إذن صلاحية في هذا الدردشه {get_display_name(await event.get_chat())}.\
                     من اجل إزالة كلمات الممنوعه من هذه المجموعة **",
                )
                for word in snips:
                    sql.rm_from_blacklist(event.chat_id, word.lower())
            break


@catub.cat_cmd(
    pattern="^منع(?:\s|$)([\s\S]*)",
    command=("منع", plugin_category),
    info={
        "header": "لإضافة كلمات قائمة السوداء إلى قاعدة البيانات",
        "description": "سيتم إضافة الكلمة أو الكلمات المعينة إلى القائمة السوداء في الدردشة المحددة إذا كان أي مستخدم يرسل ثم يتم حذف الرسالة.",
        "note": "إذا قمت بإضافة أكثر من كلمة واحدة في الوقت المناسب عبر هذا، فتذكر أنه يجب إعطاء كلمة جديدة في سطر جديد ليس [sex fuck]. يجب أن يكون كما\
            \n[sex \n fuck]",
        "usage": "{tr}منع <word(s)>",
        "examples": ["{tr}منع fuck", "{tr}منع fuck\nsex"],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "لإضافة كلمات قائمة السوداء إلى قاعدة البيانات"
    text = event.pattern_match.group(1)
    to_blacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )

    for trigger in to_blacklist:
        sql.add_to_blacklist(event.chat_id, trigger.lower())
    await edit_or_reply(
        event,
        "**⌔︙ تم اضافة  {} الكلمة في قائمة المنع بنجاح ✅**".format(
            len(to_blacklist)
        ),
    )


@catub.cat_cmd(
    pattern="^الغاء منع(?:\s|$)([\s\S]*)",
    command=("الغاء منع", plugin_category),
    info={
        "header": "لإزالة كلمات القائمة السوداء من قاعدة البيانات",
        "description": "سيتم إزالة الكلمة أو الكلمات المعينة من القائمة السوداء في الدردشة المحددة",
        "note": "إذا كنت تقوم بإزالة أكثر من كلمة واحدة في الوقت المناسب عبر هذا، فتذكر أنه يجب إعطاء كلمة جديدة في سطر جديد ليس [fuck sex]. يجب أن يكون كما\
            \n[fuck \n sex]",
        "usage": "{tr}الغاء منع <word(s)>",
        "examples": ["{tr}الغاء منع fuck", "{tr}الغاء منع fuck\nsex"],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "لإزالة كلمات القائمة السوداء من قاعدة البيانات."
    text = event.pattern_match.group(1)
    to_unblacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )
    successful = sum(
        bool(sql.rm_from_blacklist(event.chat_id, trigger.lower()))
        for trigger in to_unblacklist
    )
    await edit_or_reply(
        event, f"**⌔︙ تم الغاء منع كلمة - {successful} / {len(to_unblacklist)} من قائمه الممنوعات ✅.**"
    )


@catub.cat_cmd(
    pattern="^قائمة المنع$",
    command=("قائمة المنع", plugin_category),
    info={
        "header": "لإظهار كلمات القائمة السوداء",
        "description": "يوضح لك قائمة كلمات القائمة السوداء في تلك الدردشة المحددة",
        "usage": "{tr}قائمة المنع",
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "لإظهار كلمات القائمة السوداء في تلك الدردشة المحددة"
    all_blacklisted = sql.get_chat_blacklist(event.chat_id)
    OUT_STR = "**⌔︙ قائمة المنع في الدردشة الحالية  ⚜️ :**\n"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"👉 {trigger} \n"
    else:
        OUT_STR = "**⌔︙ لا توجد محادثات في القائمة السوداء في الروبوت الخاص بك ⁉️**"
    await edit_or_reply(event, OUT_STR)
