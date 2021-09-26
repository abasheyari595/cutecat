import asyncio
from random import choice, randint

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import get_user_from_event
from . import ALIVE_NAME

plugin_category = "fun"


@catub.cat_cmd(
    pattern="^scam(?:\s|$)([\s\S]*)",
    command=("scam", plugin_category),
    info={
        "header": "عمل نشاط وهمي في المجموعه لفتره زمنيه محدده",
        "description": "إذا لم يتم ذكر الوقت، فقد يختار وقت عشوائي 5 أو 6 دقائق للذكر استخدام الوقت في ثوان",
        "usage": [
            "{tr}scam <action> <الوقت(بالثواني)>",
            "{tr}scam <action>",
            "{tr}scam",
        ],
        "examples": "{tr}scam photo 300",
        "actions": [
            "typing",
            "contact",
            "game",
            "location",
            "voice",
            "round",
            "video",
            "photo",
            "document",
        ],
    },
)
async def _(event):
    options = [
        "typing",
        "contact",
        "game",
        "location",
        "voice",
        "round",
        "video",
        "photo",
        "document",
    ]
    input_str = event.pattern_match.group(1)
    args = input_str.split()
    if len(args) == 0:
        scam_action = choice(options)
        scam_time = randint(300, 360)
    elif len(args) == 1:
        try:
            scam_action = str(args[0]).lower()
            scam_time = randint(300, 360)
        except ValueError:
            scam_action = choice(options)
            scam_time = int(args[0])
    elif len(args) == 2:
        scam_action = str(args[0]).lower()
        scam_time = int(args[1])
    else:
        await edit_delete(event, "`غيـﮯر صـآلح ❌`")
        return
    try:
        if scam_time > 0:
            await event.delete()
            async with event.client.action(event.chat_id, scam_action):
                await asyncio.sleep(scam_time)
    except BaseException:
        return


@catub.cat_cmd(
    pattern="^ادمن(?:\s|$)([\s\S]*)",
    command=("ادمن", plugin_category),
    info={
        "header": "لرفع الشخص كمشرف بدون حقوق مسئول",
        "note": "تحتاج الحقوق المناسبة لهذا",
        "usage": [
            "{tr}ادمن <ايدي/المعرف/بالرد>",
            "{tr}ادمن <ايدي/المعرف/بالرد> <اسم مناسب>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "لرفع الشخص كمشرف بدون حقوق مسئول"
    new_rights = ChatAdminRights(post_messages=True)
    catevent = await edit_or_reply(event, "`جآر ترقيـﮯة آلشـخص...`")
    user, rank = await get_user_from_event(event, catevent)
    if not rank:
        rank = "Admin"
    if not user:
        return
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    except Exception as e:
        return await edit_delete(catevent, f"__{str(e)}__", time=10)
    await catevent.edit("`تم ترقيـﮯته بنجاح ✅`")


@catub.cat_cmd(
    pattern="^مشرف وهمي$",
    command=("مشرف وهمي", plugin_category),
    info={
        "header": "رفع مشرف وهمي",
        "description": "الرسوم المتحركة التي تظهر تمكين جميع الأذونات له هو المسؤول (ترقية وهمية)",
        "usage": "{tr}مشرف وهمي",
    },
    groups_only=True,
)
async def _(event):
    "رفع مشرف وهمي."
    animation_interval = 1
    animation_ttl = range(20)
    event = await edit_or_reply(event, "`جاري ترقية الشخص.......`")
    animation_chars = [
        "**`يتم ترقية الشخص...`**",
        "**`تمكين جميع الصلاحيات له‏‏...`**",
        "**(1) ارسال الرسائل: ☑️**",
        "**(1) ارسال الرسائل: ✅**",
        "**(2) ارسال الوسائط: ☑️**",
        "**(2) ارسال الوسائط: ✅**",
        "**(3) ارسال الملصقات و الصور المتحركه: ☑️**",
        "**(3) ارسال الملصقات و الصور المتحركه: ✅**",
        "**(4) ارسال الاستفتاءات: ☑️**",
        "**(4) ارسال الاستفتاءات: ✅**",
        "**(5) تضمين الروابط: ☑️**",
        "**(5) تضمين الروابط: ✅**",
        "**(6) اضافة مستخدمين: ☑️**",
        "**(6) اضافة مستخدمين: ✅**",
        "**(7) تثبيت الرسائل: ☑️**",
        "**(7) تثبيت الرسائل: ✅**",
        "**(8) تغيير معلومات المجموعه: ☑️**",
        "**(8) تغيير معلومات المجموعه: ✅**",
        "**تم منح جميع الاذونات بنجاح ✅**",
        f"**تم ترقيـﮯته بنجاح ✅ بواسطة: {ALIVE_NAME}**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 20])
