# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import os

from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl import functions
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest
from telethon.tl.types import Channel, Chat, InputPhoto, User

from userbot import catub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply

LOGS = logging.getLogger(__name__)
plugin_category = "utils"


# ====================== CONSTANT ===============================
INVALID_MEDIA = "**⌔︙إمتداد هذه الصورة غير صالح  ❌**"
PP_CHANGED = "**⌔︙تم تغير صورة حسابك بنجاح  ✅**"
PP_TOO_SMOL = "**⌔︙هذه الصورة صغيرة جدًا قم بإختيار صورة أخرى  ⚠️**"
PP_ERROR = "**⌔︙حدث خطأ أثناء معالجة الصورة  ⚠️**"
BIO_SUCCESS = "**⌔︙تم تغيير بايو حسابك بنجاح  ✅**"
NAME_OK = "**⌔︙تم تغيير اسم حسابك بنجاح  ✅**"
USERNAME_SUCCESS = "**⌔︙تم تغيير معرّف حسابك بنجاح  ✅**"
USERNAME_TAKEN = "**⌔︙هذا المعرّف مستخدم  ❌**"
# ===============================================================


@catub.cat_cmd(
    pattern="^وضع بايو (.*)",
    command=("وضع بايو", plugin_category),
    info={
        "header": "⌔︙لتعيين بايو لهذا الحساب  🔖",
        "usage": "{tr}وضع بايو <البايو الخاص بك>",
    },
)
async def _(event):
    "⌔︙لتعيين بايو لهذا الحساب  🔖"
    bio = event.pattern_match.group(1)
    try:
        await event.client(functions.account.UpdateProfileRequest(about=bio))
        await edit_delete(event, "**⌔︙تم تغيير البايو بنجاح  ✅**")
    except Exception as e:
        await edit_or_reply(event, f"**⌔︙خطأ  ⚠️ :**\n`{str(e)}`")


@catub.cat_cmd(
    pattern="^وضع اسم (.*)",
    command=("وضع اسم", plugin_category),
    info={
        "header": "⌔︙لتعيين/تغيير اسم لهذا الحساب  🔖.",
        "usage": ["{tr}وضع اسم الاسم الأول ؛ الكنية", "{tr}وضع اسم الاسم الأول"],
    },
)
async def _(event):
    "⌔︙لتعيين/تغيير اسم لهذا الحساب  🔖"
    names = event.pattern_match.group(1)
    first_name = names
    last_name = ""
    if ";" in names:
        first_name, last_name = names.split("|", 1)
    try:
        await event.client(
            functions.account.UpdateProfileRequest(
                first_name=first_name, last_name=last_name
            )
        )
        await edit_delete(event, "**⌔︙تم تغيير الاسم بنجاح  ✅**")
    except Exception as e:
        await edit_or_reply(event, f"**⌔︙خطأ  ⚠️ :**\n`{str(e)}`")


@catub.cat_cmd(
    pattern="^وضع صوره$",
    command=("وضع صوره", plugin_category),
    info={
        "header": "⌔︙لوضع صوره ل هذا الحساب  📂.",
        "usage": "{tr}وضع صوره <الرد على الصورة أو gif>",
    },
)
async def _(event):
    "⌔︙لوضع صوره ل هذا الحساب  📂"
    reply_message = await event.get_reply_message()
    catevent = await edit_or_reply(
        event, "**...**"
    )
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    photo = None
    try:
        photo = await event.client.download_media(
            reply_message, Config.TMP_DOWNLOAD_DIRECTORY
        )
    except Exception as e:
        await catevent.edit(str(e))
    else:
        if photo:
            await catevent.edit("**⌔︙ تم وضع الصوره بنجاح ✅**")
            if photo.endswith((".mp4", ".MP4")):
                # https://t.me/tgbetachat/324694
                size = os.stat(photo).st_size
                if size > 2097152:
                    await catevent.edit("**⌔︙ يجب ان يكون الحجم اقل من 2 ميغا ✅**")
                    os.remove(photo)
                    return
                catpic = None
                catvideo = await event.client.upload_file(photo)
            else:
                catpic = await event.client.upload_file(photo)
                catvideo = None
            try:
                await event.client(
                    functions.photos.UploadProfilePhotoRequest(
                        file=catpic, video=catvideo, video_start_ts=0.01
                    )
                )
            except Exception as e:
                await catevent.edit(f"**⌔︙خطأ  ⚠️ :**\n`{str(e)}`")
            else:
                await edit_or_reply(
                    catevent, "**⌔︙ تم تغيير الصورة بنجاح ✅**"
                )
    try:
        os.remove(photo)
    except Exception as e:
        LOGS.info(str(e))


@catub.cat_cmd(
    pattern="^وضع معرف (.*)",
    command=("وضع معرف", plugin_category),
    info={
        "header": "⌔︙ لتعيين / تحديث اسم المستخدم لهذا الحساب 👥.",
        "usage": "{tr}وضع معرف <اسم مستخدم جديد>",
    },
)
async def update_username(username):
    """قم بتعيين اسم مستخدم جديد في تليجرام."""
    newusername = username.pattern_match.group(1)
    try:
        await username.client(UpdateUsernameRequest(newusername))
        await edit_delete(event, USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await edit_or_reply(event, USERNAME_TAKEN)
    except Exception as e:
        await edit_or_reply(event, f"**⌔︙خطأ  ⚠️ :**\n`{str(e)}`")