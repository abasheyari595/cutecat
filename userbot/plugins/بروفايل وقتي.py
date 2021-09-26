# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import asyncio
import base64
import os
import random
import re
import shutil
import time
import urllib
from datetime import datetime

import requests
from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.errors import FloodWaitError
from telethon.tl import functions
from urlextract import URLExtract

from ..Config import Config
from ..helpers.utils import _format
from ..sql_helper.global_list import (
    add_to_list,
    get_collection_list,
    is_in_list,
    rm_from_list,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import (
    AUTONAME,
    BOTLOG,
    BOTLOG_CHATID,
    DEFAULT_BIO,
    _catutils,
    catub,
    edit_delete,
    logging,
)

plugin_category = "tools"

DEFAULTUSERBIO = DEFAULT_BIO or " قلوبنا مليئة برسائل ، لم تكتب "
DEFAULTUSER = AUTONAME or Config.ALIVE_NAME
LOGS = logging.getLogger(__name__)

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

autopic_path = os.path.join(os.getcwd(), "userbot", "original_pic.png")
digitalpic_path = os.path.join(os.getcwd(), "userbot", "digital_pic.png")
autophoto_path = os.path.join(os.getcwd(), "userbot", "photo_pfp.png")

digitalpfp = Config.DIGITAL_PIC or "https://telegra.ph/file/aeaebe33b1f3988a0b690.jpg"

EMOJI_TELETHON = gvarstatus("ALIVE_EMOJI") or "𖠕"
async def digitalpicloop():
    DIGITALPICSTART = gvarstatus("digitalpic") == "true"
    i = 0
    while DIGITALPICSTART:
        if not os.path.exists(digitalpic_path):
            downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        shutil.copy(digitalpic_path, autophoto_path)
        Image.open(autophoto_path)
        current_time = datetime.now().strftime("%I:%M")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        cat = str(base64.b64decode("dXNlcmJvdC9oZWxwZXJzL3N0eWxlcy9kaWdpdGFsLnR0Zg=="))[
            2:36
        ]
        fnt = ImageFont.truetype(cat, 200)
        drawn_text.text((350, 100), current_time, font=fnt, fill=(124, 252, 0))
        img.save(autophoto_path)
        file = await catub.upload_file(autophoto_path)
        try:
            if i > 0:
                await catub(
                    functions.photos.DeletePhotosRequest(
                        await catub.get_profile_photos("me", limit=1)
                    )
                )
            i += 1
            await catub(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            await asyncio.sleep(60)
        except BaseException:
            return
        DIGITALPICSTART = gvarstatus("digitalpic") == "true"


async def autoname_loop():
    AUTONAMESTART = gvarstatus("autoname") == "true"
    while AUTONAMESTART:
        HM = time.strftime("%I:%M")
        name = f"{EMOJI_TELETHON} {HM} || 𓆩 {DEFAULTUSER} 𓆪"
        LOGS.info(name)
        try:
            await catub(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(Config.CHANGE_TIME)
        AUTONAMESTART = gvarstatus("autoname") == "true"


async def autobio_loop():
    AUTOBIOSTART = gvarstatus("autobio") == "true"
    while AUTOBIOSTART:
        DMY = time.strftime("%d/%m/%Y")
        bio = f"{DEFAULTUSERBIO} 𓆩{DMY}𓆪"
        LOGS.info(bio)
        try:
            await catub(functions.account.UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(Config.CHANGE_TIME)
        AUTOBIOSTART = gvarstatus("autobio") == "true"


@catub.cat_cmd(
    pattern="^صوره وقتيه$",
    command=("صوره وقتيه", plugin_category),
    info={
        "header": "تغيير الصوره مع الوقت كل دقيقة",
        "description": "مسح الصوره القديمه وتحديث الصوره مع الوقت.\
             تستطيع تغيير الصوره عن طريق ضبط الڤار DIGITAL_PIC في هيروكو مع رابط تلكراف للصوره",
        "note": "للايقاف '.انهاء صوره وقتيه'",
        "usage": "{tr}صوره وقتيه",
    },
)
async def _(event):
    "تغيير الصوره مع الوقت"
    downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
        return await edit_delete(event, "**الصـورة الـوقتية شغـالة بالأصـل 🧸♥**")
    addgvar("digitalpic", True)
    await edit_delete(event, "**تم تفـعيل الصـورة الـوقتية بنجـاح ✅**")
    await digitalpicloop()


@catub.cat_cmd(
    pattern="^اسم وقتي$",
    command=("اسم وقتي", plugin_category),)
async def _(event):
    "تغيير الاسم مع الوقت"
    if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
        return await edit_delete(event, "**الاسـم الـوقتي شغـال بالأصـل 🧸♥**")
    addgvar("autoname", True)
    await edit_delete(event, "**تم تفـعيل الاسـم الـوقتي بنجـاح ✅**")
    await autoname_loop()


@catub.cat_cmd(
    pattern="^بايو تلقائي$",
    command=("بايو تلقائي", plugin_category),)
async def _(event):
    "لتحديث البايو مع التاريخ"
    if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
        return await edit_delete(event, "**الـبايو التلقائي شغـال بالأصـل 🧸♥**")
    addgvar("autobio", True)
    await edit_delete(event, "**تم تفـعيل البـايو التلقائي بنجـاح ✅**")
    await autobio_loop()


@catub.cat_cmd(
    pattern="^انهاء ([\s\S]*)",
    command=("انهاء", plugin_category),)
async def _(event):  # sourcery no-metrics
    "لايقاف تفعيل اوامر البروفايل التلقائي"
    input_str = event.pattern_match.group(1)
    if input_str == "صوره وقتيه":
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "**تم ايقاف الصوره الوقتيه بنـجاح ✅**")
        return await edit_delete(event, "**لم يتم تفعيل الصوره الوقتيه بالأصل 🧸♥**")
    if input_str == "اسم وقتي":
        if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
            delgvar("autoname")
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER)
            )
            return await edit_delete(event, "**تم ايقاف  الاسم الوقتي بنـجاح ✅**")
        return await edit_delete(event, "**لم يتم تفعيل الاسم الوقتي بالأصل 🧸♥**")
    if input_str == "بايو تلقائي":
        if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
            delgvar("autobio")
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "**  تم ايقاف البايو التلقائي بنـجاح ✅**")
        return await edit_delete(event, "**لم يتم تفعيل البايو التلقائي 🧸♥**")
    END_CMDS = [
        "صوره وقتيه",
        "اسم وقتي",
        "بايو تلقائي",
    ]
    if input_str not in END_CMDS:
        await edit_delete(
            event,
            f"عـذرا يجـب استـخدام الامـر بشـكل صحـيح 🧸♥",
            parse_mode=_format.parse_pre,
        )



catub.loop.create_task(digitalpicloop())
catub.loop.create_task(autoname_loop())
catub.loop.create_task(autobio_loop())
