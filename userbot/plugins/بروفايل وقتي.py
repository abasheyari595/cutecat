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
DEFAULTUSERBIO = DEFAULT_BIO or "الحـمـد الله دائـمآ وأبـدآ"
DEFAULTUSER = AUTONAME or Config.ALIVE_NAME
LOGS = logging.getLogger(__name__)

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

autopic_path = os.path.join(os.getcwd(), "userbot", "original_pic.png")
digitalpic_path = os.path.join(os.getcwd(), "userbot", "digital_pic.png")
autophoto_path = os.path.join(os.getcwd(), "userbot", "photo_pfp.png")

digitalpfp = Config.DIGITAL_PIC or "https://telegra.ph/file/aeaebe33b1f3988a0b690.jpg"

COLLECTION_STRINGS = {
    "batmanpfp_strings": [
        "awesome-batman-wallpapers",
        "batman-arkham-knight-4k-wallpaper",
        "batman-hd-wallpapers-1080p",
        "the-joker-hd-wallpaper",
        "dark-knight-joker-wallpaper",
    ],
    "thorpfp_strings": [
        "thor-wallpapers",
        "thor-wallpaper",
        "thor-iphone-wallpaper",
        "thor-wallpaper-hd",
    ],
}


async def autopicloop():
    AUTOPICSTART = gvarstatus("صوره وقتيه") == "true"
    if AUTOPICSTART and Config.DEFAULT_PIC is None:
        if BOTLOG:
            return await catub.send_message(
                BOTLOG_CHATID,
                "⌔︙حـدث خـطأ، مـن أجـل وظيفـة الصـورة التلقائيـة، يلزمـك تعييـن ڤـار DEFAULT_PIC في ڤـارات موقـع  هيروڪـو 💡",
            )
        return
    if gvarstatus("صوره وقتيه") is not None:
        try:
            counter = int(gvarstatus("autopic_counter"))
        except Exception as e:
            LOGS.warn(str(e))
    while AUTOPICSTART:
        if not os.path.exists(autopic_path):
            downloader = SmartDL(Config.DEFAULT_PIC, autopic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        shutil.copy(autopic_path, autophoto_path)
        im = Image.open(autophoto_path)
        file_test = im.rotate(counter, expand=False).save(autophoto_path, "PNG")
        current_time = datetime.now().strftime("  Time: %I:%M \n  Date: %d.%m.%y ")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
        drawn_text.text((150, 250), current_time, font=fnt, fill=(124, 252, 0))
        img.save(autophoto_path)
        file = await catub.upload_file(autophoto_path)
        try:
            await catub(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            counter += counter
            await asyncio.sleep(Config.CHANGE_TIME)
        except BaseException:
            return
        AUTOPICSTART = gvarstatus("صوره وقتيه") == "true"


async def custompfploop():
    CUSTOMPICSTART = gvarstatus("CUSTOM_PFP") == "true"
    i = 0
    while CUSTOMPICSTART:
        if len(get_collection_list("CUSTOM_PFP_LINKS")) == 0:
            LOGS.error("**⌔︙ لا توجـد صـور ملـف شخصـي للتعييـن !**")
            return
        pic = random.choice(list(get_collection_list("CUSTOM_PFP_LINKS")))
        urllib.request.urlretrieve(pic, "donottouch.jpg")
        file = await catub.upload_file("donottouch.jpg")
        try:
            if i > 0:
                await catub(
                    functions.photos.DeletePhotosRequest(
                        await catub.get_profile_photos("me", limit=1)
                    )
                )
            i += 1
            await catub(functions.photos.UploadProfilePhotoRequest(file))
            os.remove("donottouch.jpg")
            await asyncio.sleep(Config.CHANGE_TIME)
        except BaseException:
            return
        CUSTOMPICSTART = gvarstatus("CUSTOM_PFP") == "true"


async def digitalpicloop():
    DIGITALPICSTART = gvarstatus("تجديد الصوره") == "true"
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
        DIGITALPICSTART = gvarstatus("تجديد الصوره") == "true"


async def bloom_pfploop():
    BLOOMSTART = gvarstatus("تجديد الصوره الملونه") == "true"
    if BLOOMSTART and Config.DEFAULT_PIC is None:
        if BOTLOG:
            return await catub.send_message(
                BOTLOG_CHATID,
                "**⌔︙حـدث خـطأ، مـن أجـل وظيفـة الصـورة التلقائيـة، يلزمـك تعييـن ڤـار DEFAULT_PIC في ڤـارات موقـع  هيروڪـو 💡**",
            )
        return
    while BLOOMSTART:
        if not os.path.exists(autopic_path):
            downloader = SmartDL(Config.DEFAULT_PIC, autopic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        # RIP Danger zone Here no editing here plox
        R = random.randint(0, 256)
        B = random.randint(0, 256)
        G = random.randint(0, 256)
        FR = 256 - R
        FB = 256 - B
        FG = 256 - G
        shutil.copy(autopic_path, autophoto_path)
        image = Image.open(autophoto_path)
        image.paste((R, G, B), [0, 0, image.size[0], image.size[1]])
        image.save(autophoto_path)
        current_time = datetime.now().strftime("\n Time: %I:%M:%S \n \n Date: %d/%m/%y")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 60)
        ofnt = ImageFont.truetype(FONT_FILE_TO_USE, 250)
        drawn_text.text((95, 250), current_time, font=fnt, fill=(FR, FG, FB))
        drawn_text.text((95, 250), "      😈", font=ofnt, fill=(FR, FG, FB))
        img.save(autophoto_path)
        file = await catub.upload_file(autophoto_path)
        try:
            await catub(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            await asyncio.sleep(Config.CHANGE_TIME)
        except BaseException:
            return
        BLOOMSTART = gvarstatus("تجديد الصوره الملونه") == "true"


async def autoname_loop():
    AUTONAMESTART = gvarstatus("اسم وقتي") == "true"
    while AUTONAMESTART:
        HM = time.strftime("%I:%M")
        name = f"🍀 {DEFAULTUSER}↺{HM}"
        LOGS.info(name)
        try:
            await catub(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(Config.CHANGE_TIME)
        AUTONAMESTART = gvarstatus("اسم وقتي") == "true"


async def autobio_loop():
    AUTOBIOSTART = gvarstatus("بايو تلقائي") == "true"
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
        AUTOBIOSTART = gvarstatus("بايو تلقائي") == "true"


async def animeprofilepic(collection_images):
    rnd = random.randint(0, len(collection_images) - 1)
    pack = collection_images[rnd]
    pc = requests.get("http://getwallpapers.com/collection/" + pack).text
    f = re.compile(r"/\w+/full.+.jpg")
    f = f.findall(pc)
    fy = "http://getwallpapers.com" + random.choice(f)
    if not os.path.exists("f.ttf"):
        urllib.request.urlretrieve(
            "https://github.com/rebel6969/mym/raw/master/Rebel-robot-Regular.ttf",
            "f.ttf",
        )
    img = requests.get(fy)
    with open("donottouch.jpg", "wb") as outfile:
        outfile.write(img.content)
    return "donottouch.jpg"


async def autopfp_start():
    if gvarstatus("autopfp_strings") is not None:
        AUTOPFP_START = True
        string_list = COLLECTION_STRINGS[gvarstatus("autopfp_strings")]
    else:
        AUTOPFP_START = False
    i = 0
    while AUTOPFP_START:
        await animeprofilepic(string_list)
        file = await catub.upload_file("donottouch.jpg")
        if i > 0:
            await catub(
                functions.photos.DeletePhotosRequest(
                    await catub.get_profile_photos("me", limit=1)
                )
            )
        i += 1
        await catub(functions.photos.UploadProfilePhotoRequest(file))
        await _catutils.runcmd("rm -rf donottouch.jpg")
        await asyncio.sleep(Config.CHANGE_TIME)
        AUTOPFP_START = gvarstatus("autopfp_strings") is not None


@catub.cat_cmd(
    pattern="باتمان$",
    command=("باتمان", plugin_category),
    info={
        "header": "⌔︙تغييـر صـورة الملـف الشخصـي مع صـور ثـور عشوائيـة ڪل دقيقـة",
        "description": "⌔︙تغييـر صـورة الملـف الشخصـي مع صـور ثـور عشوائيـة ڪل دقيقـة، إذا ڪنت تريد تغيير الوقت، عندها يتوجب عليك تعيين ڤـار CHANGE_TIME في موقـع هيرڪـو والوقـت (بالثوانـي) بيـن ڪل تغييـر للصـورة الشخصيـة 💡",
        "note": "T⌔︙لإيقـاف هـذا، قـم بإرسـال الأمـر  ⩥ : ايقاف باتمان",
        "usage": "{tr}باتمان",
    },
)
async def _(event):
    "⌔︙لتعييـن صـور باتمـان عشوائيـة 🦇"
    if gvarstatus("autopfp_strings") is not None:
        pfp_string = gvarstatus("autopfp_strings")[:-8]
        return await edit_delete(event, f"⌔︙ {pfp_string} ** إنّـه يعمـل بالفعـل !**")
    addgvar("autopfp_strings", "batmanpfp_strings")
    await event.edit("**⌔︙جـاري بـدأ صـور باتمـان ✓**")
    await autopfp_start()


@catub.cat_cmd(
    pattern="ثور$",
    command=("ثور", plugin_category),
    info={
        "header": "⌔︙تغييـر صـورة الملـف الشخصـي ڪل دقيقـة مع صـورة مخصصـة مع الوقـت 𒀭",
        "description": "⌔︙إذا ڪنت تريد تغيير الوقـت المخصص لكل صـورة جديـدة، عندها يتوجـب عليك تعييـن ڤـار CHANGE_TIME في موقـع هيرڪـو والوقـت (بالثوانـي) بيـن ڪل تغييـر للصـورة الشخصيـة 💡",
        "note": "⌔︙لإيقـاف هـذا، قـم بإرسـال الأمـر  ⩥ : ايقاف ثور",
        "usage": "{tr}ثور",
    },
)
async def _(event):
    "⌔︙لتعييـن صـور ثـور عشوائيـة"
    if gvarstatus("autopfp_strings") is not None:
        pfp_string = gvarstatus("autopfp_strings")[:-8]
        return await edit_delete(event, f"⌔︙ {pfp_string} ** إنّـه يعمـل بالفعـل !** ")
    addgvar("autopfp_strings", "thorpfp_strings")
    await event.edit("**⌔︙جـاري بـدأ صور ثور ✓**")
    await autopfp_start()


@catub.cat_cmd(
    pattern="صوره وقتيه ?([\s\S]*)",
    command=("صوره وقتيه", plugin_category),
    info={
        "header": "⌔︙تغييـر صـورة الملـف الشخصـي ڪل دقيقـة مع صـورة مخصصـة مع الوقـت 𒀭",
        "description": "⌔︙إذا ڪنت تريد تغيير الوقـت المخصص لكل صـورة جديـدة، عندها يتوجـب عليك تعييـن ڤـار CHANGE_TIME في موقـع هيرڪـو والوقـت (بالثوانـي) بيـن ڪل تغييـر للصـورة الشخصيـة 💡",
        "options": "⌔︙يمڪنك إعطـاء إدخـال عدد صحيح مع الأمـر مثل 40،55،75 .. إلخ بحيـث يتم تدويـر صورتـك الشخصيـة بتـلك الزاويـة المحـدده ⦩",
        "note": "⌔︙لتشغيـل هـذا الأمـر، تحتـاج إلى ضبـط ڤـار DEFAULT_PIC في موقـع هيروڪـو،لإيقـاف هـذا، قـم بإرسـال الأمـر  ⩥ : .ايقاف صوره وقتيه",
        "usage": [
            "{tr}صوره وقتيه",
            "{tr}صوره وقتيه + أيّ عـدد صحيـح",
        ],
    },
)
async def _(event):
    "⌔︙لتعييـن وقـت على صـورة ملفـك الشخصـي ⏱"
    if Config.DEFAULT_PIC is None:
        return await edit_delete(
            event,
            "**⌔︙حـدث خـطأ، مـن أجـل وظيفـة الصـورة التلقائيـة، يلزمـك تعييـن ڤـار DEFAULT_PIC في ڤـارات موقـع  هيروڪـو 💡**",
            parse_mode=_format.parse_pre,
        )
    downloader = SmartDL(Config.DEFAULT_PIC, autopic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    input_str = event.pattern_match.group(1)
    if input_str:
        try:
            input_str = int(input_str)
        except ValueError:
            input_str = 60
    elif gvarstatus("autopic_counter") is None:
        addgvar("autopic_counter", 30)
    if gvarstatus("autopic") is not None and gvarstatus("autopic") == "true":
        return await edit_delete(event, f"**⌔︙الصـورة الوقـتيـه مفعّلـة بالفعـل !**")
    addgvar("صوره وقتيه", True)
    if input_str:
        addgvar("autopic_counter", input_str)
    await edit_delete(event, f"**⌔︙ تـمّ بـدأ الصـورة الوقـتيـه بواسطـة المـالك ✓**")
    await autopicloop()


@catub.cat_cmd(
    pattern="تجديد الصوره$",
    command=("تجديد الصوره", plugin_category),
    info={
        "header": "⌔︙يحـدّث صـورة ملفـك الشخصـي ڪل دقيقـة مـع وضـع وقـت عليـها 💡",
        "description": "⌔︙يحـذف صـورة الملـف الشخصـي القديمـة وقـم بتحـديث صـورة الملـف الشخصـي مـع صـورة جديـدة مـع مـرور الوقـت، يمڪنـك تغييـر هـذه الصـورة عن طريـق ضبـط ڤـار DIGITAL_PIC في موقـع هيروڪـو بإستخـدام رابـط صـورة التلڪـراف 💡",
        "note": "⌔︙لإيقـاف هـذا، قـم بإرسـال الأمـر  ⩥ :  '.ايقاف تجديد الصوره'",
        "usage": "{tr}تجديد الصوره",
    },
)
async def _(event):
    "⌔︙لتعييـن لـون صـورة عشوائـي مع وضـع وقـت لصـورة الملـف الشخصـي 💡"
    downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvarstatus("تجديد الصوره") is not None and gvarstatus("تجديد الصوره") == "true":
        return await edit_delete(event, f"**⌔︙تجديد الصوره مفعّلـة بالفعـل !**")
    addgvar("تجديد الصوره", True)
    await edit_delete(event, f"**⌔︙تـمّ بـدأ الصـورة الديجيتـال بواسطـة المستخـدم ✓**")
    await digitalpicloop()


@catub.cat_cmd(
    pattern="تجديد الصوره الملونه$",
    command=("تجديد الصوره الملونه", plugin_category),
    info={
        "header": "⌔︙تغييـر صـورة الملـف الشخصـي ڪل دقيقـة مـع لـون صـورة عشوائـي مع وضـع وقـت على الصـورة ❖",
        "description": "⌔︙إذا ڪنت تريد تغيير الوقـت المخصص لكل صـورة جديـدة، عندها يتوجـب عليك تعييـن ڤـار CHANGE_TIME في موقـع هيرڪـو والوقـت (بالثوانـي) بيـن ڪل تغييـر للصـورة الشخصيـة 💡",
        "note": "⌔︙لتشغيـل هـذا الأمـر، تحتـاج إلى ضبـط ڤـار DEFAULT_PIC في موقـع هيروڪـو،لإيقـاف هـذا، قـم بإرسـال الأمـر  ⩥ : .ايقاف تجديد الصوره الملونه",
        "usage": "{tr}تجديد الصوره الملونه",
    },
)
async def _(event):
    "⌔︙لتعييـن لـون صـورة عشوائـي مع وضـع وقـت لصـورة الملـف الشخصـي 💡"
    if Config.DEFAULT_PIC is None:
        return await edit_delete(
            event,
            "**⌔︙حـدث خـطأ، مـن أجـل هـذه الوظيفـة ، يلزمـك تعييـن ڤـار DEFAULT_PIC في ڤـارات موقـع  هيروڪـو 💡**",
            parse_mode=_format.parse_pre,
        )
    downloader = SmartDL(Config.DEFAULT_PIC, autopic_path, progress_bar=True)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvarstatus("تجديد الصوره الملونه") is not None and gvarstatus("تجديد الصوره الملونه") == "true":
        return await edit_delete(event, f"**⌔︙تجديد الصوره الملونه مفعّلـة بالفعـل !**")
    addgvar("تجديد الصوره الملونه", True)
    await edit_delete(event, f"**⌔︙تـمّ بـدأ تجديد الصوره الملونه بواسطـة المستخـدم ✓**")
    await bloom_pfploop()

@catub.cat_cmd(
    pattern="اسم وقتي$",
    command=("اسم وقتي", plugin_category),
    info={
        "header": "⌔︙تغييـر إسمـك مـع الوقـت 🜲",
        "description": "⌔︙يحـدّث إسم ملفـك الشخصـي مع الوقـت، قم بتعييـن ڤـار AUTONAME  في موقـع هيرڪـو بإسـم ملفـك الشخصـي 💡",
        "note": "⌔︙لإيقـاف هـذا، قـم بإرسـال الأمـر  ⩥ :  '.ايقاف اسم وقتي'",
        "usage": "{tr}اسم وقتي",
    },
)
async def _(event):
    "⌔︙لتعييـن إسـمك مع الوقـت 🜲"
    if gvarstatus("اسم وقتي") is not None and gvarstatus("اسم وقتي") == "true":
        return await edit_delete(event, f"**⌔︙الإسـم الوقتـي قيـد التشغيـل بالفعـل !**")
    addgvar("اسم وقتي", True)
    await edit_delete(event, "**⌔︙تـمّ بـدأ الإسـم الوقتـي بواسطـة المستخـدم ✓**")
    await autoname_loop()


@catub.cat_cmd(
    pattern="بايو تلقائي$",
    command=("بايو تلقائي", plugin_category),
    info={
        "header": "⌔︙تغييـر وصف مـع التاريخ 🜾",
        "description": "⌔︙يحـدّث إسم البايـو مع التاريخ، قم بتعييـن ڤـار DEFAULT_BIO  في موقـع هيرڪـو بإسـم ملفـك الشخصـي 💡",
        "note": "⌔︙لإيقـاف هـذا، قـم بإرسـال الأمـر  ⩥ : .ايقاف بايو تلقائي",
        "usage": "{tr}بايو تلقائي",
    },
)
async def _(event):
    "⌔︙يحـدّث البايـو مع التاريخ 💡"
    if gvarstatus("بايو تلقائي") is not None and gvarstatus("بايو تلقائي") == "true":
        return await edit_delete(event, f"**⌔︙البايـو التلقائي قيـد التشغيـل بالفعـل !**")
    addgvar("بايو تلقائي", True)
    await edit_delete(event, "**⌔︙تـمّ بـدأ البايـو التلقائي بواسطـة المستخـدم ✓**")
    await autobio_loop()


@catub.cat_cmd(
    pattern="ايقاف ([\s\S]*)",
    command=("ايقاف", plugin_category),
    info={
        "header": "⌔︙لإيقـاف أمـر التغييـر التلقائـي للبروفايـل ✦",
        "description": "إذا ڪنت تريـد إيقـاف أمـر التغييـر التلقائـي للبروفايـل، فإستخـدم هـذا الأمـر 💡",
        "options": {
            "autopic": "⌔︙لإيقـاف الصـورة التلقائيـة ✦",
            "digitalpfp": "⌔︙لإيقـاف أمـر التغييـر التلقائـي للبروفايـل ✦",
            "تجديد الصوره الملونه": "لايقاف تجديد الصوره الملونه",
            "اسم وقتي": "لايقاف الاسم الوقتي",
            "بايو تلقائي": "لايقاف البايو التلقائي",
            "ثور": "لايقاف صور ثور",
            "باتمان": "لايقاف صور باتمان",
            "spam": "لايقاف السبام",
        },
        "usage": "{tr}ايقاف <option>",
        "examples": ["{tr}ايقاف اسم وقتي"],
    },
)
async def _(event):  # sourcery no-metrics
    "⌔︙لإيقـاف أمـر التغييـر التلقائـي للبروفايـل"
    input_str = event.pattern_match.group(1)
    if input_str == "ثور" and gvarstatus("autopfp_strings") is not None:
        pfp_string = gvarstatus("autopfp_strings")[:-8]
        if pfp_string != "ثور":
            return await edit_delete(event, f"**⌔︙لم يتـم بـدأ صور ثور !**")
        await event.client(
            functions.photos.DeletePhotosRequest(
                await event.client.get_profile_photos("me", limit=1)
            )
        )
        delgvar("autopfp_strings")
        return await edit_delete(event, "**⌔︙تم إيقـاف صورة ثـور الآن ✓**")
    if input_str == "باتمان" and gvarstatus("autopfp_strings") is not None:
        pfp_string = gvarstatus("autopfp_strings")[:-8]
        if pfp_string != "باتمان":
            return await edit_delete(event, f"**⌔︙لم يتـم بـدأ صـور باتمـان !**")
        await event.client(
            functions.photos.DeletePhotosRequest(
                await event.client.get_profile_photos("me", limit=1)
            )
        )
        delgvar("autopfp_strings")
        return await edit_delete(event, "**⌔︙تم إيقـاف صورة باتمـان الآن ✓**")
    if input_str == "صوره وقتيه":
        if gvarstatus("صوره وقتيه") is not None and gvarstatus("صوره وقتيه") == "true":
            delgvar("صوره وقتيه")
            if os.path.exists(autopic_path):
                file = await event.client.upload_file(autopic_path)
                try:
                    await event.client(functions.photos.UploadProfilePhotoRequest(file))
                    os.remove(autopic_path)
                except BaseException:
                    return
            return await edit_delete(event, "**⌔︙تم إيقـاف الصـورة التلقائيـة الآن ✓**")
        return await edit_delete(event, "**⌔︙لم يتـم تفعيـل الصـورة التلقائيـة ✕**")
    if input_str == "تجديد الصوره":
        if gvarstatus("تجديد الصوره") is not None and gvarstatus("تجديد الصوره") == "true":
            delgvar("تجديد الصوره")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "**⌔︙تم إيقـاف  تجديد الصوره الآن ✓**")
        return await edit_delete(event, "**⌔︙لم يتـم تفعيـل تجديد الصوره ✕**")
    if input_str == "تجديد الصوره الملونه":
        if gvarstatus("تجديد الصوره الملونه") is not None and gvarstatus("تجديد الصوره الملونه") == "true":
            delgvar("تجديد الصوره الملونه")
            if os.path.exists(autopic_path):
                file = await event.client.upload_file(autopic_path)
                try:
                    await event.client(functions.photos.UploadProfilePhotoRequest(file))
                    os.remove(autopic_path)
                except BaseException:
                    return
            return await edit_delete(event, "**⌔︙تم إيقـاف بلـوم الآن ✓**")
        return await edit_delete(event, "**⌔︙لم يتـم تفعيـل بلـوم ✕**")
    if input_str == "اسم وقتي":
        if gvarstatus("اسم وقتي") is not None and gvarstatus("اسم وقتي") == "true":
            delgvar("اسم وقتي")
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER)
            )
            return await edit_delete(event, "**⌔︙تم إيقـاف الإسـم الوقتـي الآن ✓**")
        return await edit_delete(event, "**⌔︙لم يتـم تفعيـل الإسـم الوقتـي ✕**")
    if input_str == "بايو تلقائي":
        if gvarstatus("بايو تلقائي") is not None and gvarstatus("بايو تلقائي") == "true":
            delgvar("بايو تلقائي")
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "**⌔︙تم إيقـاف البايـو التلقائـي الآن ✓**")
        return await edit_delete(event, "**⌔︙لم يتـم تفعيـل البايـو التلقائـي ✕**")
    if input_str == "spam":
        if gvarstatus("spamwork") is not None and gvarstatus("spamwork") == "true":
            delgvar("spamwork")
            return await edit_delete(event, "**⌔︙تم إيقـاف تڪـرار الأمـر الآن ✓**")
        return await edit_delete(event, "**⌔︙لم تقـم بتفعيـل التكـرار !**")
    END_CMDS = [
        "صوره وقتيه",
        "تجديد الصوره",
        "تجديد الصوره الملونه",
        "اسم وقتي",
        "بايو تلقائي",
        "ثور",
        "باتمان",
        "spam",
    ]
    if input_str not in END_CMDS:
        await edit_delete(
            event,
            f"⌔︙ {input_str} أمـر الإنهـاء غيـر صالـح، اذڪـر بوضـوح ما يجـب أن أنهـي !",
            parse_mode=_format.parse_pre,
        )


catub.loop.create_task(autopfp_start())
catub.loop.create_task(autopicloop())
catub.loop.create_task(digitalpicloop())
catub.loop.create_task(bloom_pfploop())
catub.loop.create_task(autoname_loop())
catub.loop.create_task(autobio_loop())
