# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import re
from asyncio import sleep

from telethon.errors import rpcbaseerrors
from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterEmpty,
    InputMessagesFilterGeo,
    InputMessagesFilterGif,
    InputMessagesFilterMusic,
    InputMessagesFilterPhotos,
    InputMessagesFilterRoundVideo,
    InputMessagesFilterUrl,
    InputMessagesFilterVideo,
    InputMessagesFilterVoice,
)

from userbot import catub

from ..core.managers import edit_or_reply
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "utils"
purgelist = {}

@catub.cat_cmd(
    pattern="^مسح(\s*| \d+)$",
    command=("مسح", plugin_category),
    info={
        "header": "To delete replied message.",
        "description": "Deletes the message you replied to in x(count) seconds if count is not used then deletes immediately",
        "usage": ["{tr}del <time in seconds>", "{tr}del"],
        "examples": "{tr}del 2",
    },
)
async def delete_it(event):
    "To delete replied message."
    input_str = event.pattern_match.group(1).strip()
    msg_src = await event.get_reply_message()
    if msg_src:
        if input_str and input_str.isnumeric():
            await event.delete()
            await sleep(int(input_str))
            try:
                await msg_src.delete()
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID, "#الـمسـح \n ⎈ ⦙تـم حـذف الـرسالة بـنجاح"
                    )
            except rpcbaseerrors.BadRequestError:
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "⎈ ⦙لا يمـكنني الـحذف احـتاج صلاحيـات الادمـن",
                    )
        elif input_str:
            if not input_str.startswith("var"):
                await edit_or_reply(event, "⎈ ⦙عـذرا الـرسالة غيـر موجـودة")
        else:
            try:
                await msg_src.delete()
                await event.delete()
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID, "#الـمسـح \n ⎈ ⦙تـم حـذف الـرسالة بـنجاح"
                    )
            except rpcbaseerrors.BadRequestError:
                await edit_or_reply(event, "⎈ ⦙عـذرا الـرسالة لا استـطيع حـذفها")
    elif not input_str:
        await event.delete()


@catub.cat_cmd(
    pattern="^حذف رسائلي$",
    command=("حذف رسائلي", plugin_category),
    info={
        "header": "To purge your latest messages.",
        "description": "Deletes x(count) amount of your latest messages.",
        "usage": "{tr}purgeme <count>",
        "examples": "{tr}purgeme 2",
    },
)
async def purgeme(event):
    "To purge your latest messages."
    message = event.text
    count = int(message[12:])
    i = 1
    async for message in event.client.iter_messages(event.chat_id, from_user="me"):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await event.client.send_message(
        event.chat_id,
        f"**⎈ ⦙ تم حذف** " + str(count) + " رساله 🗑️",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "⎈ ⦙ #حـذف_الـرسائل 🗳 \n`تم حذف" + str(count) + " رساله بنجاح.` 🗑️",
        )
    await sleep(5)
    await smsg.delete()


# TODO: only sticker messages.
@catub.cat_cmd(
    pattern="^تنظيف(?:\s|$)([\s\S]*)",
    command=("تنظيف", plugin_category),
    info={
        "header": "To delete replied message.",
        "description": "Deletes the message you replied to in x(count) seconds if count is not used then deletes immediately",
        "usage": ["{tr}تنظيف <time in seconds>", "{tr}تنظيفl"],
        "examples": "{tr}تنظيف 2",
    },
)
async def iq(cloneiq):  
    chat = await cloneiq.get_input_chat()
    msgs = []
    count = 0
    input_str = cloneiq.pattern_match.group(1)
    iqype = re.findall(r"\w+", input_str)
    try:
        p_type = iqype[0].replace("-", "")
        input_str = input_str.replace(iqype[0], "").strip()
    except IndexError:
        p_type = None
    error = ""
    result = ""
    await cloneiq.delete()
    reply = await cloneiq.get_reply_message()
    if reply:
        if input_str and input_str.isnumeric():
            if p_type is not None:
                for ty in p_type:
                    if ty in Tnsmeet:
                        async for msg in cloneiq.client.iter_messages(cloneiq.chat_id, limit=int(input_str), offset_id=reply.id - 1, reverse=True, filter=Tnsmeet[ty]):
                            count += 1
                            msgs.append(msg)
                            if len(msgs) == 50:
                                await cloneiq.client.delete_messages(chat, msgs)
                                msgs = []
                        if msgs:
                            await cloneiq.client.delete_messages(chat, msgs)
                    elif ty == "s":
                        error += f"\n**⎈ ⦙   هنـاك خطـا فـي تركـيب الجمـلة 🔩 :**"
                    else:
                        error += f"\n\n⎈ ⦙   `{ty}`  **هنـاك خطـا فـي تركـيب الجمـلة 🔩 :**"
            else:
                count += 1
                async for msg in cloneiq.client.iter_messages(cloneiq.chat_id, limit=(int(input_str) - 1), offset_id=reply.id, reverse=True):
                    msgs.append(msg)
                    count += 1
                    if len(msgs) == 50:
                        await cloneiq.client.delete_messages(chat, msgs)
                        msgs = []
                if msgs:
                    await cloneiq.client.delete_messages(chat, msgs)
        elif input_str and p_type is not None:
            if p_type == "s":
                try:
                    cont, inputstr = input_str.split(" ")
                except ValueError:
                    cont = "error"
                    inputstr = input_str
                cont = cont.strip()
                inputstr = inputstr.strip()
                if cont.isnumeric():
                    async for msg in cloneiq.client.iter_messages(cloneiq.chat_id, limit=int(cont), offset_id=reply.id - 1, reverse=True, search=inputstr):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await cloneiq.client.delete_messages(chat, msgs)
                            msgs = []
                else:
                    async for msg in cloneiq.client.iter_messages(cloneiq.chat_id, offset_id=reply.id - 1, reverse=True, search=input_str):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await cloneiq.client.delete_messages(chat, msgs)
                            msgs = []
                if msgs:
                    await cloneiq.client.delete_messages(chat, msgs)
            else:
                error += f"\n⎈ ⦙   `{ty}`  **هنـاك خطـا فـي تركـيب الجمـلة 🔩 :** "
        elif input_str:
            error += f"\n⎈ ⦙   **هنـاك خطـا فـي تركـيب الجمـلة 🔩 :**"
        elif p_type is not None:
            for ty in p_type:
                if ty in Tnsmeet:
                    async for msg in cloneiq.client.iter_messages(cloneiq.chat_id, min_id=cloneiq.reply_to_msg_id - 1, filter=Tnsmeet[ty]):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await cloneiq.client.delete_messages(chat, msgs)
                            msgs = []
                    if msgs:
                        await cloneiq.client.delete_messages(chat, msgs)
                else:
                    error += f"\n⎈ ⦙   `{ty}`  **هنـاك خطـا فـي تركـيب الجمـلة 🔩 :**"
        else:
            async for msg in cloneiq.client.iter_messages(chat, min_id=cloneiq.reply_to_msg_id - 1 ):
                count += 1
                msgs.append(msg)
                if len(msgs) == 50:
                    await cloneiq.client.delete_messages(chat, msgs)
                    msgs = []
            if msgs:
                await cloneiq.client.delete_messages(chat, msgs)
    elif p_type is not None and input_str:
        if p_type != "s" and input_str.isnumeric():
            for ty in p_type:
                if ty in Tnsmeet:
                    async for msg in cloneiq.client.iter_messages(cloneiq.chat_id, limit=int(input_str), filter=Tnsmeet[ty]):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await cloneiq.client.delete_messages(chat, msgs)
                            msgs = []
                    if msgs:
                        await cloneiq.client.delete_messages(chat, msgs)
                elif ty == "s":
                    error += f"\n**⎈ ⦙   لا تستطـيع استـخدام امر التنظيف عبر البحث مع الاضافه 🔎**"
                else:
                    error += f"\n⎈ ⦙   `{ty}`  **هنـاك خطـا فـي تركـيب الجمـلة 🔩 :**"
        elif p_type == "s":
            try:
                cont, inputstr = input_str.split(" ")
            except ValueError:
                cont = "error"
                inputstr = input_str
            cont = cont.strip()
            inputstr = inputstr.strip()
            if cont.isnumeric():
                async for msg in cloneiq.client.iter_messages(cloneiq.chat_id, limit=int(cont), search=inputstr):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await cloneiq.client.delete_messages(chat, msgs)
                        msgs = []
            else:
                async for msg in cloneiq.client.iter_messages(cloneiq.chat_id, search=input_str):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await cloneiq.client.delete_messages(chat, msgs)
                        msgs = []
            if msgs:
                await cloneiq.client.delete_messages(chat, msgs)
        else:
            error += f"\n⎈ ⦙   `{ty}`  **هنـاك خطـا فـي تركـيب الجمـلة 🔩 :**"
    elif p_type is not None:
        for ty in p_type:
            if ty in Tnsmeet:
                async for msg in cloneiq.client.iter_messages(cloneiq.chat_id, filter=Tnsmeet[ty]
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await cloneiq.client.delete_messages(chat, msgs)
                        msgs = []
                if msgs:
                    await cloneiq.client.delete_messages(chat, msgs)
            elif ty == "s":
                error += f"\n**⎈ ⦙   لا تستطـيع استـخدام امر التنظيف عبر البحث مع الاضافه 🔎**"
            else:
                error += f"\n⎈ ⦙   `{ty}`  **هنـاك خطـا فـي تركـيب الجمـلة 🔩 :**"
    elif input_str.isnumeric():
        async for msg in cloneiq.client.iter_messages(chat, limit=int(input_str) + 1):
            count += 1
            msgs.append(msg)
            if len(msgs) == 50:
                await cloneiq.client.delete_messages(chat, msgs)
                msgs = []
        if msgs:
            await cloneiq.client.delete_messages(chat, msgs)
    else:
        error += "\n**⎈ ⦙   لم يتـم تحـديد الرسـالة أرسل  (.الاوامر ) و رؤية اوامر التنظيف  📌**"
    if msgs:
        await cloneiq.client.delete_messages(chat, msgs)
    if count > 0:
        result += "⎈ ⦙   تـم الأنتـهاء من التـنظيف السـريع  ✅  \n ⎈ ⦙   لقـد  تـم حـذف \n  ⎈ ⦙   عـدد  " + str(count) + " من الـرسائـل 🗑️"
    if error != "":
        result += f"\n\n**⎈ ⦙  عـذرا هنـاك خطـأ ❌:**{error}"
    if result == "":
        result += "**⎈ ⦙   لا تـوجد رسـائل لـتنظيفها ♻️**"
    hi = await cloneiq.client.send_message(cloneiq.chat_id, result)
    if BOTLOG:
        await cloneiq.client.send_message(BOTLOG_CHATID, f"**⎈ ⦙   #حـذف_الـرسائل 🗳️** \n{result}")
    await sleep(5)
    await hi.delete()
