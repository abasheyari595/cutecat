# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import re

from userbot import catub

from ..core.managers import edit_or_reply
from ..sql_helper.filter_sql import (
    add_filter,
    get_filters,
    remove_all_filters,
    remove_filter,
)
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "utils"


@catub.cat_cmd(incoming=True)
async def filter_incoming_handler(handler):  # sourcery no-metrics
    if handler.sender_id == handler.client.uid:
        return
    name = handler.raw_text
    filters = get_filters(handler.chat_id)
    if not filters:
        return
    a_user = await handler.get_sender()
    chat = await handler.get_chat()
    me = await handler.client.get_me()
    title = chat.title or "this chat"
    participants = await handler.client.get_participants(chat)
    count = len(participants)
    mention = f"[{a_user.first_name}](tg://user?id={a_user.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = a_user.first_name
    last = a_user.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{a_user.username}" if a_user.username else mention
    userid = a_user.id
    my_first = me.first_name
    my_last = me.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    for trigger in filters:
        pattern = r"( |^|[^\w])" + re.escape(trigger.keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            if trigger.f_mesg_id:
                msg_o = await handler.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id)
                )
                await handler.reply(
                    msg_o.message.format(
                        mention=mention,
                        title=title,
                        count=count,
                        first=first,
                        last=last,
                        fullname=fullname,
                        username=username,
                        userid=userid,
                        my_first=my_first,
                        my_last=my_last,
                        my_fullname=my_fullname,
                        my_username=my_username,
                        my_mention=my_mention,
                    ),
                    file=msg_o.media,
                )
            elif trigger.reply:
                await handler.reply(
                    trigger.reply.format(
                        mention=mention,
                        title=title,
                        count=count,
                        first=first,
                        last=last,
                        fullname=fullname,
                        username=username,
                        userid=userid,
                        my_first=my_first,
                        my_last=my_last,
                        my_fullname=my_fullname,
                        my_username=my_username,
                        my_mention=my_mention,
                    ),
                )


@catub.cat_cmd(
    pattern="^اضف رد ([\s\S]*)",
    command=("اضف رد", plugin_category),
    info={
        "header": "⌔︙لحفـظ رد للڪلمـة المعطـاة ⎙",
        "description": "⌔︙ إذا قـام أيّ مستخـدم بإرسـال تلك الڪلمة عندهـا سيقوم البـوت بالـردّ عليـه  💡",
        "option": {
            "{mention}": "⌔︙ لذكر المستخدم",
            "{title}": "⌔︙ للحصول على اسم الدردشة في الرسالة",
            "{count}": "⌔︙ للحصول على أعضاء المجموعة",
            "{first}": "⌔︙ لاستخدام اسم المستخدم الأول",
            "{last}": "⌔︙ لاستخدام اسم المستخدم الأخير",
            "{fullname}": "⌔︙ لاستخدام اسم المستخدم الكامل",
            "{userid}": "⌔︙ لاستخدام معرف المستخدم",
            "{username}": "⌔︙ لاستخدام اسم المستخدم الخاص بالمستخدم",
            "{my_first}": "⌔︙ لاستخدام اسمي الأول",
            "{my_fullname}": "⌔︙ لاستخدام اسمي الكامل",
            "{my_last}": "⌔︙ لاستخدام اسم عائلتي",
            "{my_mention}": "⌔︙ أن أذكر نفسي",
            "{my_username}": "⌔︙ لاستخدام اسم المستخدم الخاص بي.",
        },
        "note": "⌔︙لحفـظ الوسائـط/الملصقـات ڪردّ، يجـب عليـك بأن تقـوم بتعييـن الأمـر PRIVATE_GROUP_BOT_API_ID 💡 ",
        "usage": "{tr}اضف رد + الڪلمـة  ⎗",
    },
)
async def add_new_filter(new_handler):
    "⌔︙لحفـظ رد للڪلمـة المعطـاة ⎙"
    keyword = new_handler.pattern_match.group(1)
    string = new_handler.text.partition(keyword)[2]
    msg = await new_handler.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG:
            await new_handler.client.send_message(
                BOTLOG_CHATID,
                f"**⌔︙ اضـافه ردّ ⎗ :**\
            \n**⌔︙آيـدي الدردشـة 🆔 :** {new_handler.chat_id}\
            \n**⌔︙آثـار ⌬ :** {keyword}\
            \n\n**⌔︙تـم حفظ الرسـالة التاليـة ڪردّ على الكلمـة في الدردشـة، يرجـى عـدم حذفهـا ✻**",
            )
            msg_o = await new_handler.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=new_handler.chat_id,
                silent=True,
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                new_handler,
                "**⌔︙ لحفـظ الوسائـط ڪرد يتوجـب تعييـن - PRIVATE_GROUP_BOT_API_ID. 💡**",
            )
            return
    elif new_handler.reply_to_msg_id and not string:
        rep_msg = await new_handler.get_reply_message()
        string = rep_msg.text
    success = "**⌔︙تـم حفـظ الـرد {} بنجـاح ✓**"
    if add_filter(str(new_handler.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(new_handler, success.format(keyword, "added"))
    remove_filter(str(new_handler.chat_id), keyword)
    if add_filter(str(new_handler.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(new_handler, success.format(keyword, "Updated"))
    await edit_or_reply(new_handler, f"**⌔︙ حـدث خطـأ عنـد تعييـن الـردّ ✕ :** {keyword}")


@catub.cat_cmd(
    pattern="^جميع الردود$",
    command=("جميع الردود", plugin_category),
    info={
        "header": "⌔︙ لإظهـار جميع الـردود لهـذه الدردشـة  ⎙",
        "description": "⌔︙لإظهـار جميع ردود (البـوت) في هـذه الدردشـة ⎙",
        "usage": "{tr}جميع الردود",
    },
)
async def on_snip_list(event):
    "⌔︙لإظهـار جميع الـردود لهـذه الدردشـة ⎙"
    OUT_STR = "**⌔︙لايوجـد أيّ رد في هـذه الدردشـة  ✕**"
    filters = get_filters(event.chat_id)
    for filt in filters:
        if OUT_STR == "**⌔︙ لايوجـد أيّ رد في هـذه الدردشـة  ✕**":
            OUT_STR = "**⌔︙الـردود المتوفـرة في هـذه الدردشـة ⎙ :** \n"
        OUT_STR += "▷  `{}`\n".format(filt.keyword)
    await edit_or_reply(
        event,
        OUT_STR,
        caption="**⌔︙الـردود المتاحـة في الدردشـة الحاليـة ⎙ **",
        file_name="filters.text",
    )


@catub.cat_cmd(
    pattern="^مسح رد ([\s\S]*)",
    command=("مسح رد", plugin_category),
    info={
        "header": "⌔︙ لحـذف ذلك الـرد، يتوجب على المستخـدم إرسـال الڪلمـة  💡",
        "usage": "{tr}مسح رد + الڪلمـة",
    },
)
async def remove_a_filter(r_handler):
    "⌔︙مسح رد الڪلمـة المحـددة ✕"
    filt = r_handler.pattern_match.group(1)
    if not remove_filter(r_handler.chat_id, filt):
        await r_handler.edit("**⌔︙ الـرد  {}  غيـر موجـود ❗️**".format(filt))
    else:
        await r_handler.edit("**⌔︙تـم حـذف الـردّ  {}  بنجـاح ✓**".format(filt))


@catub.cat_cmd(
    pattern="^مسح جميع الردود$",
    command=("مسح جميع الردود", plugin_category),
    info={
        "header": "⌔︙ لحـذف جميـع ردود المجموعـة 💡.",
        "usage": "{tr}مسح جميع الردود",
    },
)
async def on_all_snip_delete(event):
    "⌔︙ لحـذف جميـع ردود المجموعـة 💡"
    filters = get_filters(event.chat_id)
    if filters:
        remove_all_filters(event.chat_id)
        await edit_or_reply(event, f"**⌔︙تـم حـذف ردود الدردشـة الحاليـة بنجـاح ✓**")
    else:
        await edit_or_reply(event, f"**⌔︙لايوجـد أيّ رد في هـذه المجموعـة ✕**")
