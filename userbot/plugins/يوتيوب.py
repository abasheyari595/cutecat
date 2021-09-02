# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import asyncio
import glob
import io
import os
import pathlib
import re
from datetime import datetime
from time import time

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import types
from telethon.utils import get_attributes
from wget import download
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from userbot import catub

from ..core import pool
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import progress, reply_id
from ..helpers.functions.utube import _mp3Dl, get_yt_video_id, get_ytthumb, ytsearch
from ..helpers.utils import _format
from . import hmention

BASE_YT_URL = "https://www.youtube.com/watch?v="
LOGS = logging.getLogger(__name__)
plugin_category = "misc"


video_opts = {
    "format": "best",
    "addmetadata": True,
    "key": "FFmpegMetadata",
    "writethumbnail": True,
    "prefer_ffmpeg": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
    "postprocessors": [
        {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
        {"key": "FFmpegMetadata"},
    ],
    "outtmpl": "%(title)s.mp4",
    "logtostderr": False,
    "quiet": True,
}


async def ytdl_down(event, opts, url):
    ytdl_data = None
    try:
        await event.edit("⌔︙يتم جلب البيانات إنتظر قليلا ⏳`")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await event.edit(f"`{DE}`")
    except ContentTooShortError:
        await event.edit("`⌔︙عُذرا هذا المحتوى قصير جدًا لتنزيله ⚠`")
    except GeoRestrictedError:
        await event.edit(
            "`⌔︙ هذا الفيديو غير متاح من موقعك الجغرافي بسبب القيود الجغرافية التي يفرضها موقع الويب 🌍`"
        )
    except MaxDownloadsReached:
        await event.edit("`⌔︙ تم الوصول إلى الحد الأقصى لعدد التنزيلات 🛑`")
    except PostProcessingError:
        await event.edit("`⌔︙ كان هناك خطأ أثناء المعالجة ⚠️`")
    except UnavailableVideoError:
        await event.edit("`⌔︙ الوسائط غير متوفرة بالتنسيق المطلوب ⚠️`")
    except XAttrMetadataError as XAME:
        await event.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        await event.edit("`⌔︙ حدث خطأ أثناء استخراج المعلومات يرجى وضعها بشكل صحيح ❗️`")
    except Exception as e:
        await event.edit(f"**خطأ ⚠️ : **\n__{e}__")
    return ytdl_data


async def fix_attributes(
    path, info_dict: dict, supports_streaming: bool = False, round_message: bool = False
) -> list:
    """⌔︙ تجنب الحالات المتعددة للميزة ✳️"""
    new_attributes = []
    video = False
    audio = False

    uploader = info_dict.get("uploader", "Unknown artist")
    duration = int(info_dict.get("duration", 0))
    suffix = path.suffix[1:]
    if supports_streaming and suffix != "mp4":
        supports_streaming = True

    attributes, mime_type = get_attributes(path)
    if suffix == "mp3":
        title = str(info_dict.get("title", info_dict.get("id", "Unknown title")))
        audio = types.DocumentAttributeAudio(
            duration=duration, voice=None, title=title, performer=uploader
        )
    elif suffix == "mp4":
        width = int(info_dict.get("width", 0))
        height = int(info_dict.get("height", 0))
        for attr in attributes:
            if isinstance(attr, types.DocumentAttributeVideo):
                duration = duration or attr.duration
                width = width or attr.w
                height = height or attr.h
                break
        video = types.DocumentAttributeVideo(
            duration=duration,
            w=width,
            h=height,
            round_message=round_message,
            supports_streaming=supports_streaming,
        )

    if audio and isinstance(audio, types.DocumentAttributeAudio):
        new_attributes.append(audio)
    if video and isinstance(video, types.DocumentAttributeVideo):
        new_attributes.append(video)

    for attr in attributes:
        if (
            isinstance(attr, types.DocumentAttributeAudio)
            and not audio
            or not isinstance(attr, types.DocumentAttributeAudio)
            and not video
            or not isinstance(attr, types.DocumentAttributeAudio)
            and not isinstance(attr, types.DocumentAttributeVideo)
        ):
            new_attributes.append(attr)
    return new_attributes, mime_type


@catub.cat_cmd(
    pattern="تحميل صوت(?:\s|$)([\s\S]*)",
    command=("تحميل صوت", plugin_category),
    info={
        "header": "⌔︙لتحميل مقطع صوتي من اليوتيوب ومواقع أخرى 🎙",
        "description": "تحميل المقطع الصوتي من الرابط المعطى (يدعم جميع المواقع التي تدعم youtube-dl) 📮",
        "examples": ["{tr}تحميل صوت <بالرد علي الرابط>", "{tr}تحميل صوت <الرابط>"],
    },
)
async def download_audio(event):
    """⌔︙لتحميل مقطع صوتي من اليوتيوب ومواقع أخرى 🎙."""
    url = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not url and rmsg:
        myString = rmsg.text
        url = re.search("(?P<url>https?://[^\s]+)", myString).group("url")
    if not url:
        return await edit_or_reply(event, "`⌔︙ يجب وضع رابط لتحميله  ❗`")
    catevent = await edit_or_reply(event, "`⌔︙ يتم الإعداد إنتظر قليلا  ⏱`")
    reply_to_id = await reply_id(event)
    try:
        vid_data = YoutubeDL({"no-playlist": True}).extract_info(url, download=False)
    except ExtractorError:
        vid_data = {"title": url, "uploader": "Catuserbot", "formats": []}
    startTime = time()
    retcode = await _mp3Dl(url=url, starttime=startTime, uid="320")
    if retcode != 0:
        return await event.edit(str(retcode))
    _fpath = ""
    thumb_pic = None
    for _path in glob.glob(os.path.join(Config.TEMP_DIR, str(startTime), "*")):
        if _path.lower().endswith((".jpg", ".png", ".webp")):
            thumb_pic = _path
        else:
            _fpath = _path
    if not _fpath:
        return await edit_delete(catevent, "غير قادر علي تحميل الاغنية 🚫")
    await catevent.edit(
        f"`⌔︙ يتم لتحميل الأغنية 🎙 :`\
        \n**{vid_data['title']}**\
        \n⌔︙بواسطة 📝 : *{vid_data['uploader']}*"
    )
    attributes, mime_type = get_attributes(str(_fpath))
    ul = io.open(pathlib.Path(_fpath), "rb")
    if thumb_pic is None:
        thumb_pic = str(
            await pool.run_in_thread(download)(await get_ytthumb(get_yt_video_id(url)))
        )
    uploaded = await event.client.fast_upload_file(
        file=ul,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(
                d,
                t,
                catevent,
                startTime,
                "trying to upload",
                file_name=os.path.basename(pathlib.Path(_fpath)),
            )
        ),
    )
    ul.close()
    media = types.InputMediaUploadedDocument(
        file=uploaded,
        mime_type=mime_type,
        attributes=attributes,
        force_file=False,
        thumb=await event.client.upload_file(thumb_pic) if thumb_pic else None,
    )
    await event.client.send_file(
        event.chat_id,
        file=media,
        caption=f"<b>اسم الملف 🧪: </b><code>{vid_data.get('title', os.path.basename(pathlib.Path(_fpath)))}</code>",
        reply_to=reply_to_id,
        parse_mode="html",
    )
    for _path in [_fpath, thumb_pic]:
        os.remove(_path)
    await catevent.delete()


@catub.cat_cmd(
    pattern="تحميل فيديو(?:\s|$)([\s\S]*)",
    command=("تحميل فيديو", plugin_category),
    info={
        "header": "⌔︙ لتحميل فيديو من مواقع عديدة مثل يوتيوب  📮",
        "description": "⌔︙ تحميل الفيديو من الرابط المعطى(يدعم جميع المواقع التي تدعم youtube-dl) 📮",
        "examples": [
            "{tr}تحميل فيديو <بالرد علي الرابط>",
            "{tr}تحميل فيديو <الرابط>",
        ],
    },
)
async def download_video(event):
    """⌔︙لتحميل فيديو من يوتيوب ومواقع اخرى عديدة 📮."""
    url = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not url and rmsg:
        myString = rmsg.text
        url = re.search("(?P<url>https?://[^\s]+)", myString).group("url")
    if not url:
        return await edit_or_reply(event, "⌔︙ عليك وضع رابـط اولا ليتم تنـزيله ❗")
    catevent = await edit_or_reply(event, "`⌔︙ يتم التحميل إنتظر قليلا  ⏱`")
    reply_to_id = await reply_id(event)
    ytdl_data = await ytdl_down(catevent, video_opts, url)
    if ytdl_down is None:
        return
    f = pathlib.Path(f"{ytdl_data['title']}.mp4".replace("|", "_"))
    catthumb = pathlib.Path(f"{ytdl_data['title']}.jpg".replace("|", "_"))
    if not os.path.exists(catthumb):
        catthumb = pathlib.Path(f"{ytdl_data['title']}.webp".replace("|", "_"))
    if not os.path.exists(catthumb):
        catthumb = None
    await catevent.edit(
        f"`⌔︙ التحضيـر للـرفع إنتظر ♻`\
        \n**{ytdl_data['title']}**\
        \n⌔︙بواسطة 📝 : *{ytdl_data['uploader']}*"
    )
    ul = io.open(f, "rb")
    c_time = time()
    attributes, mime_type = await fix_attributes(f, ytdl_data, supports_streaming=True)
    uploaded = await event.client.fast_upload_file(
        file=ul,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, catevent, c_time, "upload", file_name=f)
        ),
    )
    ul.close()
    media = types.InputMediaUploadedDocument(
        file=uploaded,
        mime_type=mime_type,
        attributes=attributes,
        thumb=await event.client.upload_file(catthumb) if catthumb else None,
    )
    await event.client.send_file(
        event.chat_id,
        file=media,
        reply_to=reply_to_id,
        caption=ytdl_data["title"],
    )
    os.remove(f)
    if catthumb:
        os.remove(catthumb)
    await event.delete()


@catub.cat_cmd(
    pattern="نتائج بحث(?: |$)(\d*)? ?(.*)",
    command=("نتائج بحث", plugin_category),
    info={
        "header": "⌔︙ للبحث عن فيديوات في اليوتيوب  🔍",
        "description": "⌔︙ يجلب نتائج بحث youtube مع المشاهدات والمدة مع عدد النتائج المطلوبة بشكل افتراضي ، فإنه يجلب 10 نتائج ⚜️",
        "examples": [
            "{tr}<نتائج بحث <استفسار",
            "{tr}<نتائج بحث <1-9> <استفسار",
        ],
    },
)
async def yt_search(event):
    "⌔︙للبحث عن فيديوات في اليوتيوب 🔍"
    if event.is_reply and not event.pattern_match.group(2):
        query = await event.get_reply_message()
        query = str(query.message)
    else:
        query = str(event.pattern_match.group(2))
    if not query:
        return await edit_delete(
            event, "**⌔︙ يرجى الرّد على الرسالة أو كتابة الرابط أولا  ⚠️**"
        )
    video_q = await edit_or_reply(event, "**⌔︙ يتم البحث عن المطلوب إنتظر قليلا  ⏱**")
    if event.pattern_match.group(1) != "":
        lim = int(event.pattern_match.group(1))
        if lim <= 0:
            lim = int(10)
    else:
        lim = int(10)
    try:
        full_response = await ytsearch(query, limit=lim)
    except Exception as e:
        return await edit_delete(video_q, str(e), time=10, parse_mode=_format.parse_pre)
    reply_text = f"**⌔︙ البحث 🔍 :**\n`{query}`\n\n**⌔︙  النتائج :**\n{full_response}"
    await edit_or_reply(video_q, reply_text)


@catub.cat_cmd(
    pattern="انستا (.*)",
    command=("انستا", plugin_category),
    info={
        "header": "⌔︙لتحميل فيديو/صورة من الإنستكرام 🌠",
        "description": "⌔︙ملاحظة، يتم تحميل الفيديوات/الصور العامة فقط ❗️",
        "examples": [
            "{tr}انستا <الرابط",
        ],
    },
)
async def kakashi(event):
    "⌔︙لتحميل فيديو/صورة من الإنستكرام 🌠"
    chat = "@instasavegrambot"
    link = event.pattern_match.group(1)
    if "www.instagram.com" not in link:
        await edit_or_reply(
            event, "**⌔︙ يجب كتابة رابط من الإنستكرام ليتم تحميله ❗️**"
        )
    else:
        start = datetime.now()
        catevent = await edit_or_reply(event, "**⌔︙ جاري التحميل إنتظر قليلا  ⏱**")
    async with event.client.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            response = await conv.get_response()
            msg = await conv.send_message(link)
            video = await conv.get_response()
            details = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("**⌔︙قم بفتح الحظر عن البوت ❗️ :** @instasavegrambot")
            return
        await catevent.delete()
        cat = await event.client.send_file(
            event.chat_id,
            video,
        )
        end = datetime.now()
        ms = (end - start).seconds
        await cat.edit(
            f"⌔︙تم التنزيل بواسطة : @YS9II",
            parse_mode="html",
        )
    await event.client.delete_messages(
        conv.chat_id, [msg_start.id, response.id, msg.id, video.id, details.id]
    )
