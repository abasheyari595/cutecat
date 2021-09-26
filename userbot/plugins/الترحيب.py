# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

from telethon import events

from userbot import catub
from userbot.core.logger import logging

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.welcome_sql import (
    add_welcome_setting,
    get_current_welcome_settings,
    rm_welcome_setting,
    update_previous_welcome,
)
from . import BOTLOG_CHATID

plugin_category = "utils"
LOGS = logging.getLogger(__name__)


@catub.on(events.ChatAction)
async def _(event):  # sourcery no-metrics
    cws = get_current_welcome_settings(event.chat_id)
    if (
        cws
        and (event.user_joined or event.user_added)
        and not (await event.get_user()).bot
    ):
        if gvarstatus("clean_welcome") is None:
            try:
                await event.client.delete_messages(event.chat_id, cws.previous_welcome)
            except Exception as e:
                LOGS.warn(str(e))
        a_user = await event.get_user()
        chat = await event.get_chat()
        me = await event.client.get_me()
        title = chat.title or "this chat"
        participants = await event.client.get_participants(chat)
        count = len(participants)
        mention = "<a href='tg://user?id={}'>{}</a>".format(
            a_user.id, a_user.first_name
        )
        my_mention = "<a href='tg://user?id={}'>{}</a>".format(me.id, me.first_name)
        first = a_user.first_name
        last = a_user.last_name
        fullname = f"{first} {last}" if last else first
        username = f"@{a_user.username}" if a_user.username else mention
        userid = a_user.id
        my_first = me.first_name
        my_last = me.last_name
        my_fullname = f"{my_first} {my_last}" if my_last else my_first
        my_username = f"@{me.username}" if me.username else my_mention
        file_media = None
        current_saved_welcome_message = None
        if cws:
            if cws.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
                )
                file_media = msg_o.media
                current_saved_welcome_message = msg_o.message
            elif cws.reply:
                current_saved_welcome_message = cws.reply
        current_message = await event.reply(
            current_saved_welcome_message.format(
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
            file=file_media,
            parse_mode="html",
        )
        update_previous_welcome(event.chat_id, current_message.id)


@catub.cat_cmd(
    pattern="^ترحيب(?: |$)(.*)",
    command=("ترحيب", plugin_category),
    info={
        "الامر": "ترحيب",
        "الشرح": "امر الترحيب يقوم بالتحريب بجميع الاشخاص الذين يدخلون للمجموعه",
        "الاضافات": {
            "{mention}": "عمل تاك للمستخدم",
            "{title}": "لوضع اسم الدردشه مع الاسم",
            "{count}": "لوضع عدد الاعضاء",
            "{first}": "لوضع الاسم الاول للمستخدم ",
            "{last}": "لوضع الاسك الثاني للمستخدم",
            "{fullname}": "لوضع الاسم الكامل للمستخدم",
            "{userid}": "لوضع ايدي الشخص",
            "{username}": "لوضع معرف الشخص",
            "{my_first}": "لوضع الاسم الاول الخاص بك",
            "{my_fullname}": "لوضع الاسم الكامل الخاص بك",
            "{my_last}": "لوضع الاسم الثاني الخاص بك",
            "{my_mention}": "لعمل تاك لنفسك ",
            "{my_username}": "لاستخدام معرفك.",
        },
        "الاستخدام": [
            "{tr}ترحيب <رسالة التحريب>",
            "قم بالرد {tr}ترحيب على الرسالة او الصوره لوضعها رساله ترحيبيه",
        ],
        "الامثلة": "{tr}ترحيب نورِت .",
    },
)
async def save_welcome(event):
    "⌔︙لوضع رسالة ترحيبية في المجموعة 🔖"
    msg = await event.get_reply_message()
    string = "".join(event.text.split(maxsplit=1)[1:])
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙رسالة الترحيب 🔖 :\
                \n⌔︙ايدي الدردشة 🆔 : {event.chat_id}\
                \n⌔︙يتم حفظ الرسالة التالية كملاحظة ترحيبية لـ 🔖 : {event.chat.title}, ",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            return await edit_or_reply(
                event,
                "⌔︙ حفظ الصورة كرسالة ترحيبية يتطلب وضع الفار لـ  BOTLOG_CHATID ",
            )
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "**⌔︙تم حفظ الترحيب الخاص بهذه الدردشة بنجاح ✅**"
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("saved"))
    rm_welcome_setting(event.chat_id)
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("updated"))
    await edit_or_reply("⌔︙حدث خطأ أثناء وضع ترحيب في هذه المجموعة ⚠️")

@catub.cat_cmd(
    pattern="^مسح الترحيب$",
    command=("مسح الترحيب", plugin_category),
    info={
        "header": "مسح الترحيب",
        "الشرح": "⌔︙لحذف الرساله الترحيبية",
        "usage": "{tr}مسح الترحيب",
    },
)
async def del_welcome(event):
    "⌔︙لمسح الترحيب 🗑"
    if rm_welcome_setting(event.chat_id) is True:
        await edit_or_reply(event, "**⌔︙تم مسح الرساله الترحيبيه لهذه الدردشة بنجاح ✅**")
    else:
        await edit_or_reply(event, "**⌔︙لم يتم حفظ أي رساله ترحيبية هنا ⚠️**")

@catub.cat_cmd(
    pattern="^رسالة الترحيب$",
    command=("رسالة الترحيب", plugin_category),
    info={
        "header": "لرؤية رسالة الترحيب المضافه للدردشه",
        "usage": "{tr}رسالة الترحيب",
    },
)
async def show_welcome(event):
    "⌔︙لإظهار رسالة الترحيب الحالية في المجموعة 🔖"
    cws = get_current_welcome_settings(event.chat_id)
    if not cws:
        return await edit_or_reply(event, "**⌔︙لم يتم حفظ أي رساله ترحيبية هنا ⚠️**")
    if cws.f_mesg_id:
        msg_o = await event.client.get_messages(
            entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
        )
        await edit_or_reply(
            event, "**⌔︙أنا الآن أقوم بالترحيب بالمستخدمين الجدد مع هذه الرسالة ✅**"
        )
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws.reply:
        await edit_or_reply(
            event, "**⌔︙أنا الآن أقوم بالترحيب بالمستخدمين الجدد مع هذه الرسالة ✅**"
        )
        await event.reply(cws.reply)


@catub.cat_cmd(
    pattern="^(تشغيل|ايقاف) حذف رسالة الترحيب$",
    command=("(تشغيل|ايقاف) حذف رسالة الترحيب", plugin_category),
    info={
        "header": "لتشغيل أو ايقاف حذف رسالة الترحيب السابقة ⚠️.",
        "الشرح": "⌔︙ إذا كنت ترغب في حذف رسالة الترحيب السابقة عند انضمام عضو جديد وإرسال رسالة ترحيب جديدة ، فقم بتشغيلها عن طريق تشغيل حذف رسالة الترحيب  قم بإيقاف تشغيلها إذا كنت بحاجة الي ذلك",
        "usage": "{tr}تشغيل/ايقاف <حذف رسالة الترحيب>",
    },
)
async def del_welcome(event):
    "لتشغيل او ايقاف حذف رسالة الترحيب السابقة ⚠️."
    input_str = event.pattern_match.group(1)
    if input_str == "تشغيل":
        if gvarstatus("clean_welcome") is None:
            return await edit_delete(event, "**⌔︙تم تشغيلها بالفعل ✅**")
        delgvar("clean_welcome")
        return await edit_delete(
            event,
            "**⌔︙ من الآن رسالة الترحيب السابقة سيتم حذفها وسيتم إرسال رسالة الترحيب الجديدة ⚠️**",
        )
    if gvarstatus("clean_welcome") is None:
        addgvar("clean_welcome", "false")
        return await edit_delete(
            event, "**⌔︙من الآن لن يتم حذف رسالة الترحيب السابقة ⚠️**"
        )
    await edit_delete(event, "**⌔︙تم إيقافها بالفعل ✅**")
