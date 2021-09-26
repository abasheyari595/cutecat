# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import asyncio
import base64
import io
import os
from pathlib import Path

from ShazamAPI import Shazam
from telethon import types
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url
from userbot import catub
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import name_dl, song_dl, video_dl, yt_search
from ..helpers.tools import media_type
from ..helpers.utils import _catutils, reply_id

plugin_category = "utils"
LOGS = logging.getLogger(__name__)

# =========================================================== #
#                           الفارات                           #
# =========================================================== #
SONG_SEARCH_STRING = "⌔︙جاري البحث عن الاغنية إنتظر رجاءًا  🎧"
SONG_NOT_FOUND = "⌔︙لم أستطع إيجاد هذه الأغنية  ⚠️"
SONG_SENDING_STRING = "⌔︙قم بإلغاء حظر البوت  🚫"
# =========================================================== #
#                                                             
# =========================================================== #


@catub.cat_cmd(
    pattern="^اغنية(320)?(?: |$)(.*)",
    command=("اغنية", plugin_category),
    info={
        "header": "للحصول علي الاغاني.",
        "description": "هذا الامر يقوم بالبحث عن الاغنيه علي اليوتيوب ويرسلها علي شكل مقطع صوتي 🌹🌹.",
        "flags": {
            "320": "اذا استخدمت song 320 فسوف تحصل علي جوده 320k او 128k",
        },
        "usage": "{tr}اغنية <اسم الاغنيه>",
        "examples": "{tr}اغنية ياليلة العيد",
    },
)
async def _(event):
    "⌔︙للبحث عن أغاني  🎧"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply:
        if reply.message:
            query = reply.message
    else:
        return await edit_or_reply(event, "**⌔︙ما الذي تريد أن أبحث عنه  ⁉️**")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    catevent = await edit_or_reply(event, "**⌔︙جاري تحميل الأغنية إنتظر قليلا  ⏳**")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"**⌔︙عـذرًا لم أستطع إيجاد الأغنية أو الفيديو لـ  ❌** `{query}`"
        )
    cmd = event.pattern_match.group(1)
    q = "320k" if cmd == "320" else "128k"
    song_cmd = song_dl.format(QUALITY=q, video_link=video_link)
    # thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    stderr = (await _catutils.runcmd(song_cmd))[1]
    if stderr:
        return await catevent.edit(f"**⌔︙ خـطأ  ⚠️ :** `{stderr}`")
    catname, stderr = (await _catutils.runcmd(name_cmd))[:2]
    if stderr:
        return await catevent.edit(f"**⌔︙ خـطأ  ⚠️ :** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    catname = os.path.splitext(catname)[0]
    # if stderr:
    #    return await catevent.edit(f"**Error :** `{stderr}`")
    song_file = Path(f"{catname}.mp3")
    if not os.path.exists(song_file):
        return await catevent.edit(
            f"**⌔︙عـذرًا لم أستطع إيجاد الأغنية أو الفيديو لـ  ❌** `{query}`"
        )
    await catevent.edit("**⌔︙لقد وجدت الاغنية إنتظر قليلا  ⏱**")
    catthumb = Path(f"{catname}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{catname}.webp")
    elif not os.path.exists(catthumb):
        catthumb = None

    await event.client.send_file(
        event.chat_id,
        song_file,
        force_document=False,
        caption=query,
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await catevent.delete()
    for files in (catthumb, song_file):
        if files and os.path.exists(files):
            os.remove(files)


async def delete_messages(event, chat, from_message):
    itermsg = event.client.iter_messages(chat, min_id=from_message.id)
    msgs = [from_message.id]
    async for i in itermsg:
        msgs.append(i.id)
    await event.client.delete_messages(chat, msgs)
    await event.client.send_read_acknowledge(chat)


@catub.cat_cmd(
    pattern="^اغنيه فيديو(?: |$)(.*)",
    command=("اغنيه فيديو", plugin_category),
    info={
        "header": "للحصول على أغاني الفيديو من اليوتيوب.",
        "description": "هذا الامر يقوم بالبحث عن الاغنيه علي اليوتيوب ويرسلها علي شكل فيديو 🌹🌹",
        "usage": "{tr}اغنيه فيديو <اسم الاغنيه>",
        "examples": "{tr}اغنيه فيديو ياحبيبتي يامصر",
    },
)
async def _(event):
    "⌔︙للبحث عن فيديوات أغاني  🎥"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        if reply.message:
            query = reply.messag
    else:
        return await edit_or_reply(event, "**⌔︙قم بوضع الأمر وبجانبه إسم الأغنية  🖇**")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    catevent = await edit_or_reply(event, "**⌔︙لقد وجدت الفيديو المطلوب إنتظر قليلا  ⏱ ...**")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"**⌔︙ عـذرًا لم أستطع إيجاد أي فيديو او صوت متعلق بـ ❌** `{query}`"
        )
    # thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    video_cmd = video_dl.format(video_link=video_link)
    stderr = (await _catutils.runcmd(video_cmd))[1]
    if stderr:
        return await catevent.edit(f"**⌔︙ خـطأ  ⚠️ :** `{stderr}`")
    catname, stderr = (await _catutils.runcmd(name_cmd))[:2]
    if stderr:
        return await catevent.edit(f"**⌔︙ خـطأ  ⚠️ :** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    # if stderr:
    #    return await catevent.edit(f"**Error :** `{stderr}`")
    catname = os.path.splitext(catname)[0]
    vsong_file = Path(f"{catname}.mp4")
    if not os.path.exists(vsong_file):
        vsong_file = Path(f"{catname}.mkv")
    elif not os.path.exists(vsong_file):
        return await catevent.edit(
            f"**⌔︙ عـذرًا لم أستطع إيجاد أي فيديو او صوت متعلق بـ ❌** `{query}`"
        )
    await catevent.edit("**⌔︙لقد وجدت الفديو المطلوب انتظر قليلا  ⏳**")
    catthumb = Path(f"{catname}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{catname}.webp")
    elif not os.path.exists(catthumb):
        catthumb = None
    await event.client.send_file(
        event.chat_id,
        vsong_file,
        force_document=False,
        caption=query,
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await catevent.delete()
    for files in (catthumb, vsong_file):
        if files and os.path.exists(files):
            os.remove(files)


@catub.cat_cmd(
    pattern="^تعريف$",
    command=("تعريف", plugin_category),
    info={
        "header": "للبحث عن اسم الاغنية من خلال المقطع الصوتي.",
        "description": "يجب أن يكون طول ملف الموسيقى حوالي 10 ثوان لاستخدام البرنامج المساعد.",
        "usage": "{tr}تعريف",
    },
)
async def _(event):
    "**⌔︙قم بالرد على الرسالة الصوتية لعكس البحث عن هذه الأغنية  ♻️** ."
    if not event.reply_to_msg_id:
        return await edit_delete(event, "```**⌔︙قم بالرد على الرسالة الصوتية لعكس البحث عن هذه الأغنية  ♻️**")
    reply_message = await event.get_reply_message()
    chat = "@auddbot"
    catevent = await edit_or_reply(event, "**⌔︙جاري تعريف المقطع الصوتي  📲**")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(reply_message)
            check = await conv.get_response()
            if not check.text.startswith("Audio received"):
                return await catevent.edit(
                    "⚠️ خطأ أثناء تعريف المقطع الصوتي ❌. حاول استخدام رسالة صوتية قصيره ٥-١٠ ثواني."
                )
            await catevent.edit("⌔︙ انتظر يتم تعريف المقطع الصوتي 📲")
            result = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("⌔︙ قم بالغاء حظر(@auddbot) وحاول مرة اخري")
            return
    namem = f"**اسم الاغنيه‏‏ : **`{result.text.splitlines()[0]}`\
        \n\n**التفاصيل : **__{result.text.splitlines()[2]}__"
    await catevent.edit(namem)
