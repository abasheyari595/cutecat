import time

from prettytable import PrettyTable

# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.tools import media_type
from ..helpers.utils import _format
from . import humanbytes

plugin_category = "utils"


TYPES = [
    "Photo",
    "Audio",
    "Video",
    "Document",
    "Sticker",
    "Gif",
    "Voice",
    "Round Video",
]


def weird_division(n, d):
    return n / d if d else 0





@catub.cat_cmd(
    pattern="^معلومات تخزين المجموعه(?:\s|$)([\s\S]*)",
    command=("معلومات تخزين المجموعه", plugin_category),
    info={
        "header": "يوضح لك الوسائط الكامله / ملخص الملفات الخاصه بهذا المستخدم في تلك المجموعة.",
        "description": "اعتبارا من الآن تقتصر على آخر 10000 رسالة من هذا الشخص في المجموعة المستخدمة",
        "usage": "{tr}معلومات تخزين المجموعه",
        "examples": "{tr}معلومات تخزين المجموعه",
    },
)
async def _(event):  # sourcery no-metrics
    "معلومات تخزين المجموعه."
    reply = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    if reply and input_str:
        try:
            entity = int(input_str)
        except ValueError:
            entity = input_str
        userentity = reply.sender_id
    elif reply:
        entity = event.chat_id
        userentity = reply.sender_id
    elif input_str:
        entity = event.chat_id
        try:
            userentity = int(input_str)
        except ValueError:
            userentity = input_str
    else:
        entity = event.chat_id
        userentity = event.sender_id
    starttime = int(time.monotonic())
    x = PrettyTable()
    totalcount = totalsize = msg_count = 0
    x.title = "File Summary"
    x.field_names = ["Media", "Count", "File size"]
    largest = "   <b>أكبر حجم</b>\n"
    try:
        chatdata = await event.client.get_entity(entity)
    except Exception as e:
        return await edit_delete(
            event, f"<b>⌔︙خطـأ ⚠️ : </b><code>{str(e)}</code>", 5, parse_mode="HTML"
        )
    try:
        userdata = await event.client.get_entity(userentity)
    except Exception as e:
        return await edit_delete(
            event, f"<b>⌔︙خطـأ ⚠️ : </b><code>{str(e)}</code>", time=5, parse_mode="HTML"
        )
    if type(chatdata).__name__ == "Channel":
        if chatdata.username:
            link = f"<a href='t.me/{chatdata.username}'>{chatdata.title}</a>"
        else:
            link = chatdata.title
    else:
        link = f"<a href='tg://user?id={chatdata.id}'>{chatdata.first_name}</a>"
    catevent = await edit_or_reply(
        event,
        f"<code>⌔︙حسـاب عـدد الملفـات وحجـم الملـف حسـب ✦ </code>{_format.htmlmentionuser(userdata.first_name,userdata.id)}<code> in Group </code><b>{link}</b>\n<code>This may take some time also depends on number of user messages</code>",
        parse_mode="HTML",
    )

    media_dict = {
        m: {"file_size": 0, "count": 0, "max_size": 0, "max_file_link": ""}
        for m in TYPES
    }
    async for message in event.client.iter_messages(
        entity=entity, limit=None, from_user=userentity
    ):
        msg_count += 1
        media = media_type(message)
        if media is not None:
            media_dict[media]["file_size"] += message.file.size
            media_dict[media]["count"] += 1
            if message.file.size > media_dict[media]["max_size"]:
                media_dict[media]["max_size"] = message.file.size
                if type(chatdata).__name__ == "Channel":
                    media_dict[media][
                        "max_file_link"
                    ] = f"https://t.me/c/{chatdata.id}/{message.id}"
                else:
                    media_dict[media][
                        "max_file_link"
                    ] = f"tg://openmessage?user_id={chatdata.id}&message_id={message.id}"
            totalsize += message.file.size
            totalcount += 1
    for mediax in TYPES:
        x.add_row(
            [
                mediax,
                media_dict[mediax]["count"],
                humanbytes(media_dict[mediax]["file_size"]),
            ]
        )
        if media_dict[mediax]["count"] != 0:
            largest += f"  •  <b><a href='{media_dict[mediax]['max_file_link']}'>{mediax}</a>  : </b><code>{humanbytes(media_dict[mediax]['max_size'])}</code>\n"
    endtime = int(time.monotonic())
    if endtime - starttime >= 120:
        runtime = str(round(((endtime - starttime) / 60), 2)) + " minutes"
    else:
        runtime = str(endtime - starttime) + " seconds"
    avghubytes = humanbytes(weird_division(totalsize, totalcount))
    avgruntime = (
        str(round((weird_division((endtime - starttime), totalcount)) * 1000, 2))
        + " ms"
    )
    totalstring = f"<code><b> ⌔︙إجمالـي الملفـات ✦ : </b>       | {str(totalcount)}\
                  \n <b> ⌔︙الحجـم الإجمالـي للملـف ✦ : </b>   | {humanbytes(totalsize)}\
                  \n <b> حجم الملف  : </b>    | {avghubytes}\
                  \n</code>"
    runtimestring = f"<code><b> ⌔︙وقـت التشغيـل ✦ :</b>            | {runtime}\
                    \n <b> وقـت التشغيـل لڪل ملـف ✦ :</b>   | {avgruntime}\
                    \n</code>"
    line = "<code>+--------------------+-----------+</code>\n"
    result = f"<b>⌔︙المجموعـة ✦ : {link}\nUser : {_format.htmlmentionuser(userdata.first_name,userdata.id)}\n\n"
    result += f"<code><b>⌔︙مجمـوع الرسائـل ✦ :</b> {msg_count}</code>\n"
    result += "<b>⌔︙ملخـص الملـف ✦ : </b>\n"
    result += f"<code>{str(x)}</code>\n"
    result += f"{largest}"
    result += line + totalstring + line + runtimestring + line
    await catevent.edit(result, parse_mode="HTML", link_preview=False)
