# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import os
from datetime import datetime
from pathlib import Path

from ..Config import Config
from ..utils import load_module, remove_plugin
from . import (
    CMD_HELP,
    CMD_LIST,
    SUDO_LIST,
    catub,
    edit_delete,
    edit_or_reply,
    hmention,
    reply_id,
)

plugin_category = "tools"

DELETE_TIMEOUT = 5
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


@catub.cat_cmd(
    pattern="^تنصيب$",
    command=("تنصيب", plugin_category),
    info={
        "header": "لتثبيت اضافه خارجيه.",
        "description": "قم بالرد علي اي اضافه خارجيه(مدعومه) لتنصيبها في البوت.",
        "usage": "{tr}تنصيب",
    },
)
async def install(event):
    "لتثبيت اضافه خارجي."
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                "userbot/plugins/",
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await edit_delete(
                    event,
                    f"تم تنصيب الاضافه  بنجاح ✅ `{os.path.basename(downloaded_file_name)}`",
                    10,
                )
            else:
                os.remove(downloaded_file_name)
                await edit_delete(
                    event, "خطأ ❗️ تم تثبيت هذا الاضافه بالفعل / مثبت مسبقا.", 10
                )
        except Exception as e:
            await edit_delete(event, f"**خطأ ❌️:**\n`{e}`", 10)
            os.remove(downloaded_file_name)

@catub.cat_cmd(
    pattern="^ارسل ([\s\S]*)",
    command=("ارسل", plugin_category),
    info={
        "header": "لارسال الاضافه في الشات",
        "usage": "{tr}ابعت <اسم الاضافه>",
        "examples": "{tr}ابعت الاغاني",
    },
)
async def send(event):
    "لارسال الاضافه في الشات"
    reply_to_id = await reply_id(event)
    thumb = thumb_image_path if os.path.exists(thumb_image_path) else None
    input_str = event.pattern_match.group(1)
    the_plugin_file = f"./userbot/plugins/{input_str}.py"
    if os.path.exists(the_plugin_file):
        start = datetime.now()
        caat = await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            thumb=thumb,
        )
        end = datetime.now()
        ms = (end - start).seconds
        await event.delete()
        await caat.edit(
            f"<b><i>🔗 اسم الاضافه :- {input_str} .</i></b>\n<b><i>🧪 تم التحميل في {ms} ثواني .</i></b>\n<b><i>",
            parse_mode="html",
        )
    else:
        await edit_or_reply(event, "🚨: لم يتم ايجاد الملف")

@catub.cat_cmd(
    pattern="^الغاء تنصيب ([\s\S]*)",
    command=("الغاء تنصيب", plugin_category),
    info={
        "header": "لالغاء تنصيب الاضافه مؤقتا.",
        "description": "لايقاف وظيفة الاضافه وازالتها من البوت.",
        "note": "لالغاء تفعيل الإضافة للابد من البوت قم بظبط ڤار NO_LOAD في هيروكو مع اسم الاضافه, قم بعمل مساحه بين الاسماء اذا كان هناك اكثر من اضافه تود ازالتها.",
        "usage": "{tr}الغاء تنصيب <اسم الاضافه>",
        "examples": "{tr}الغاء تنصيب الاغاني",
    },
)
async def unload(event):
    "لالغاء تنصيب الاضافه مؤقتا."
    shortname = event.pattern_match.group(1)
    path = Path(f"userbot/plugins/{shortname}.py")
    if not os.path.exists(path):
        return await edit_delete(
            event, f"لايوجد اضافه في هذا المسار {path} لالغاء تثبيتها"
        )
    os.remove(path)
    if shortname in CMD_LIST:
        CMD_LIST.pop(shortname)
    if shortname in SUDO_LIST:
        SUDO_LIST.pop(shortname)
    if shortname in CMD_HELP:
        CMD_HELP.pop(shortname)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"{shortname} تم الغاء التنصيب بنجاح ✅")
    except Exception as e:
        await edit_or_reply(event, f"تم الغاء التنصيب بنجاح ✅ {shortname}\n{e}")
