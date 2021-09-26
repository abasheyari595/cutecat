# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

#--------------------------------------------------------------------------------------------------------------------------------

import asyncio, time, io, math, os, logging, asyncio, shutil, re, subprocess, json
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from base64 import b64decode
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User
from telethon.tl import functions, types
from telethon.tl.functions.messages import GetHistoryRequest, CheckChatInviteRequest, GetFullChatRequest
from telethon.errors import (ChannelInvalidError, ChannelPrivateError, ChannelPublicGroupNaError, InviteHashEmptyError, InviteHashExpiredError, InviteHashInvalidError)
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest
from telethon.errors import FloodWaitError
from time import sleep
from html import unescape
from urllib.parse import quote_plus
from urllib.error import HTTPError
from telethon import events
from requests import get
from html import unescape
from re import findall
from asyncio import sleep
from telethon.errors.rpcerrorlist import YouBlockedUserError
import random
from userbot import catub
from ..core.managers import edit_delete, edit_or_reply

plugin_category = "utils"

async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("`قناة او مجموعه غير صالحه ❌`")
            return None
        except ChannelPrivateError:
            await event.reply("`هذه قناة خاصة / مجموعة أو أنا محظور من هناك`")
            return None
        except ChannelPublicGroupNaError:
            await event.reply("`القناة أو المجموعه غير موجودة`")
            return None
        except (TypeError, ValueError) as err:
            await event.reply("`قناة او مجموعه غير صالحه ❌`")
            return None
    return chat_info



def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = ' '.join(names)
    return full_name
    
@catub.cat_cmd(
    pattern="^دعوة ([\s\S]*)",
    command=("دعوة", plugin_category),
    info={
        "header": "أضف المستخدم المعطى / المستخدمين إلى المجموعة التي استخدمت فيها الأمر.",
        "description": "يضيف الشخص المذكور فقط أو بوت ليس كل الأعضاء",
        "usage": "{tr}دعوة <معرف المستخدم(s)/ايدي المستخدم(s)>",
        "examples": "{tr}دعوة @combot @MissRose_bot",
    },
)
async def _(event):
    "دعوة المستخدم الي الشات."
    to_add_users = event.pattern_match.group(1)
    if not event.is_channel and event.is_group:
        # https://lonamiwebs.github.io/Telethon/methods/messages/add_chat_user.html
        for user_id in to_add_users.split(" "):
            try:
                await event.client(
                    functions.messages.AddChatUserRequest(
                        chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                    )
                )
            except Exception as e:
                return await edit_delete(event, f"`{str(e)}`", 5)
    else:
        # https://lonamiwebs.github.io/Telethon/methods/channels/invite_to_channel.html
        for user_id in to_add_users.split(" "):
            try:
                await event.client(
                    functions.channels.InviteToChannelRequest(
                        channel=event.chat_id, users=[user_id]
                    )
                )
            except Exception as e:
                return await edit_delete(event, f"`{e}`", 5)

    await edit_or_reply(event, f"`{to_add_users} تم دعوته بنجاح ✅`")

@catub.cat_cmd(
    pattern="^سحب ([\s\S]*)",
    command=("سحب", plugin_category),
    info={
        "header": "أضف المستخدمين إلى المجموعة التي استخدمت فيها الأمر .سحب الكل » معرف الجروب الي عاوز تسحب اعضاءه «.",
        "description": "اضافة جميع الاعضاء ممكن يسبب سبام او خطا مؤقت في البوت",
        "usage": "{tr}سحب <معرف الجروب>",
        "examples": "{tr}سحب @FE_1EF",
    },
)
async def get_users(event):   
    sender = await event.get_sender() ; me = await event.client.get_me()
    if not sender.id == me.id:
        hell = await event.reply("`جاري سحب الاعضاء للجروب 📬...`")
    else:
    	hell = await event.edit("`جاري سحب الاعضاء للجروب 📬...`")
    kraken = await get_chatinfo(event) ; chat = await event.get_chat()
    if event.is_private:
              return await hell.edit("`عذرا، لايمكن إضافة المستخدمين هنا ❗️`")    
    s = 0 ; f = 0 ; error = 'None'   
  
    await hell.edit("**حالة الترمنال 🚸**\n\n`تجميع الاعضاء 🚁.......`")
    async for user in event.client.iter_participants(kraken.full_chat.id):
                try:
                    if error.startswith("Too"):
                        return await hell.edit(f"**انتهي الترمنال مع وجود بعض الاخطاء 🚫**\n(`ربما حصلت علي خطأ محدود من التيلثون حاول في وقت آخر`)\n**خطأ ❌** : \n`{error}`\n\n• تم سحب `{s}` من الناس ✅\n• فشل سحب ❌ `{f}` من الناس")
                    await event.client(functions.channels.InviteToChannelRequest(channel=chat,users=[user.id]))
                    s = s + 1                                                    
                    await hell.edit(f"**الترمنال مشغل...**\n\n• تم سحب `{s}` من الناس ✅\n• فشل سحب `{f}` من الناس ❌\n\n**× اخر خطأ:** `{error}`")                
                except Exception as e:
                    error = str(e) ; f = f + 1             
    return await hell.edit(f"**انتهي الترمنال** \n\n• تم بنجاح سحب `{s}` من الناس ✅ \n• فشل سحب `{f}` من الناس ❌")
    