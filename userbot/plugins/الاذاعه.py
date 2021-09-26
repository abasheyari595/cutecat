# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import os

from telethon import events
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights
from userbot import catub

from ..core.managers import edit_or_reply

from . import *
plugin_category = "utils"

@catub.cat_cmd(
    pattern="^وجه ?(.*)$",
    command=("وجه", plugin_category),
)
async def gcast(event):
    "توجيه الرساله لكل المجموعات."
    if not event.out and not is_fullsudo(event.sender_id):
        return await edit_or_reply(event, "هـذا الامـر مقـيد للسـودو")
    xx = event.pattern_match.group(1)
    if not xx:
        return edit_or_reply(event, "** ⌔︙ يجـب وضـع نـص مع الامـر للتوجيـه**")
    tt = event.text
    msg = tt[6:]
    event = await edit_or_reply(event, "** ⌔︙ يتـم الـتوجيـة للـمجموعـات انتـظر قليلا**")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await event.edit(f"تـم بنـجـاح فـي {done} من الـدردشـات , خطـأ فـي {er} من الـدردشـات")


@catub.cat_cmd(
    pattern="^حول ?(.*)$",
    command=("حول", plugin_category),
)
async def gucast(event):
    "تحويل الرساله لكل الي في الخاص."
    if not event.out and not is_fullsudo(event.sender_id):
        return await edit_or_reply(event, "هـذا الامـر مقـيد للسـودو")
    xx = event.pattern_match.group(1)
    if not xx:
        return edit_or_reply(event, "** ⌔︙ يجـب وضـع نـص مع الامـر للتوجيـه**")
    tt = event.text
    msg = tt[7:]
    kk = await edit_or_reply(event, "** ⌔︙ يتـم الـتوجيـة للخـاص انتـظر قليلا**")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await event.edit(f"تـم بنـجـاح فـي {done} من الـدردشـات , خطـأ فـي {er} من الـدردشـات")
