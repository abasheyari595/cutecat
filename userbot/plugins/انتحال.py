# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import html

from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest

from ..Config import Config
from . import (
    ALIVE_NAME,
    AUTONAME,
    BOTLOG,
    BOTLOG_CHATID,
    DEFAULT_BIO,
    catub,
    edit_delete,
    get_user_from_event,
)

plugin_category = "utils"
DEFAULTUSER = str(AUTONAME) if AUTONAME else str(ALIVE_NAME)
DEFAULTUSERBIO = (
    str(DEFAULT_BIO)
    if DEFAULT_BIO
    else "الحمد الله على كل شئ  ⌔︙"
)


@catub.cat_cmd(
    pattern="^انتحال(?: |$)(.*)",
    command=("انتحال", plugin_category),
    info={
        "header": "⌔︙لإنتحـال حسـاب المستخـدم المذڪور أو الذي تم الردّ عليـه  🃏",
        "usage": "{tr}انتحال اسم المستخدم/معرف المستخدم/ الرد",
    },
)
async def _(event):
    "⌔︙ لإنتحـال حسـاب المستخـدم المذڪور أو الذي تم الردّ عليـه  🃏"
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return
    user_id = replied_user.id
    profile_pic = await event.client.download_profile_photo(user_id, Config.TEMP_DIR)
    first_name = html.escape(replied_user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.last_name
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
    replied_user = await event.client(GetFullUserRequest(replied_user.id))
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await event.client(functions.account.UpdateProfileRequest(first_name=first_name))
    await event.client(functions.account.UpdateProfileRequest(last_name=last_name))
    await event.client(functions.account.UpdateProfileRequest(about=user_bio))
    pfile = await event.client.upload_file(profile_pic)
    await event.client(functions.photos.UploadProfilePhotoRequest(pfile))
    await edit_delete(event, "**⌔︙ تـم إنتحـال الحسـاب بنجـاح  ✓**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"**⌔︙الإنتحـال 🃏 :** \n **✓ تـم إنتحـال الحسـاب بنجـاح :**  [{first_name}](tg://user?id={user_id })",
        )


@catub.cat_cmd(
    pattern="^الغاء الانتحال$",
    command=("الغاء الانتحال", plugin_category),
    info={
        "header": "⌔︙ لإعـادة إسمـك الأصلـي، البايـو وصـورة الملف الشخصي  ♲",
        "note": "⌔︙ للتشغيل السليم لهذا الأمر، تحتاج إلى تعيين الإسم التلقائي والبايو الإفتراضي مع اسم ملفك الشخصي والسيرة الذاتية على التوالي ❗️.",
        "usage": "{tr}الغاء الانتحال",
    },
)
async def _(event):
    "لإعادة تعيين التفاصيل الأصلية الخاصة بك"
    name = f"{DEFAULTUSER}"
    blank = ""
    bio = f"{DEFAULTUSERBIO}"
    await event.client(
        functions.photos.DeletePhotosRequest(
            await event.client.get_profile_photos("me", limit=1)
        )
    )
    await event.client(functions.account.UpdateProfileRequest(about=bio))
    await event.client(functions.account.UpdateProfileRequest(first_name=name))
    await event.client(functions.account.UpdateProfileRequest(last_name=blank))
    await edit_delete(event, "**⌔︙تمّـت إعـادة حسـابك بنجـاح ✓**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, f"⌔︙ **الأعـادة ♲ :**\n**⌔︙ تـم إعـادة ضبـط حسـابك إلـى وضعـه الطبيـعي بـنجاح ✓**"
        )
