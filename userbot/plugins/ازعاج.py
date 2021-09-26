# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.echo_sql import (
    addecho,
    get_all_echos,
    get_echos,
    is_echo,
    remove_all_echos,
    remove_echo,
    remove_echos,
)
from . import get_user_from_event

plugin_category = "fun"


@catub.cat_cmd(
    pattern="^ازعاج$",
    command=("ازعاج", plugin_category),
    info={
        "header": "لتكرار الرسائل المرسلة من قبل الشخص.",
        "description": "قم بالرد على المستخدم باستخدام هذا الامر, ثم سيتم تكرار جميع رسائل النص والملصقات إليه مرة أخرى.",
        "usage": "{tr}ازعاج <بالرد>",
    },
)
async def echo(event):
    "لتكرار الرسائل المرسلة من قبل الشخص"
    if event.reply_to_msg_id is None:
        return await edit_or_reply(
            event, "**⌔︙ يرجى الرد على الشخص الذي تـريد ازعاجه ❕**"
        )
    catevent = await edit_or_reply(event, "**⌔︙ يتم تفعيل هذا الامر انتظر قليلا ❕**")
    user, rank = await get_user_from_event(event, catevent, nogroup=True)
    if not user:
        return
    reply_msg = await event.get_reply_message()
    chat_id = event.chat_id
    user_id = reply_msg.sender_id
    if event.is_private:
        chat_name = user.first_name
        chat_type = "Personal"
    else:
        chat_name = event.chat.title
        chat_type = "Group"
    user_name = user.first_name
    user_username = user.username
    if is_echo(chat_id, user_id):
        return await edit_or_reply(event, "**⌔︙ تـم تفـعيل وضـع الازعاج على الشخص بنجاح ✅ **")
    try:
        addecho(chat_id, user_id, chat_name, user_name, user_username, chat_type)
    except Exception as e:
        await edit_delete(catevent, f"⌔︙ Error:\n`{str(e)}`")
    else:
        await edit_or_reply(catevent, "**⌔︙ تـم تفعـيل امـر الازعاج علـى هذا الشـخص**\n **⌔︙ سـيتم تقليـد جميع رسائلـه هـنا**")


@catub.cat_cmd(
    pattern="^مسح الازعاج",
    command=("مسح الازعاج", plugin_category),
    info={
        "header": "لإيقاف تكرار رسائل الشخص المعينه.",
        "description": "الرد علي الشخص بهذا الأمر للتوقف عن تكرار رسائله مرة أخرى.",
        "usage": "{tr}مسح الازعاج <بالرد>",
    },
)
async def echo(event):
    "لإيقاف تكرار رسائل الشخص المعينه"
    if event.reply_to_msg_id is None:
        return await edit_or_reply(
            event, "⌔︙ يرجى الرد على الشخص الذي تـريد مسح ازعاجه ❕"
        )
    reply_msg = await event.get_reply_message()
    user_id = reply_msg.sender_id
    chat_id = event.chat_id
    if is_echo(chat_id, user_id):
        try:
            remove_echo(chat_id, user_id)
        except Exception as e:
            await edit_delete(catevent, f"**⌔︙ هناك خطا ‼️ :**\n`{str(e)}`")
        else:
            await edit_or_reply(event, "⌔︙ تـم مسح وضـع الازعاج على الشخص بنجاح ✅ ")
    else:
        await edit_or_reply(event, "⌔︙ لم يتم تفعـيل امـر الازعاج علـى هذا الشـخص ‼️")


@catub.cat_cmd(
    pattern="^الغاء الازعاج( للكل)?",
    command=("الغاء الازعاج", plugin_category),
    info={
        "header": "لالغاء الازعاج في هذه المجموعه.",
        "description": "لإيقاف تقليد رسائل المستخدمين من المستخدمين الممكنين في المجموعه المعينة أو جميع المجموعات.",
        "flags": {"للكل": "لالغاء التقليد لجميع المجموعات"},
        "usage": [
            "{tr}الغاء الازعاج",
            "{tr}الغاء الازعاج للكل",
        ],
    },
)
async def echo(event):
    "لالغاء الازعاج في هذه المجموعه او الكل."
    input_str = event.pattern_match.group(1)
    if input_str:
        lecho = get_all_echos()
        if len(lecho) == 0:
            return await edit_delete(
                event, "**⌔︙ لم يتم تفعيل الازعاج بالاصل لاي شخص ⚠️**"
            )
        try:
            remove_all_echos()
        except Exception as e:
            await edit_delete(event, f"**⌔︙ هناك خطا ‼️ :**\n`{str(e)}`", 10)
        else:
            await edit_or_reply(
                event, "**⌔︙ تـم ايقاف وضـع الازعاج على الجميع بنجاح ✅ .**"
            )
    else:
        lecho = get_echos(event.chat_id)
        if len(lecho) == 0:
            return await edit_delete(
                event, "**⌔︙ لم يتم تفعيل الازعاج بالاصل لاي شخص ⚠️**"
            )
        try:
            remove_echos(event.chat_id)
        except Exception as e:
            await edit_delete(event, f"**⌔︙ هناك خطا ‼️ :**\n`{str(e)}`", 10)
        else:
            await edit_or_reply(
                event, "**⌔︙ تـم ايقاف وضـع الازعاج على الجميع بنجاح ✅**"
            )


@catub.cat_cmd(
    pattern="^المزعجهم( الكل)?$",
    command=("المزجعهم", plugin_category),
    info={
        "header": "يعرض قائمة المستخدمين الذين قمت بتمكين وضع الازعاج عليهم",
        "flags": {
            "الكل": "لإدراج المستخدمين الذين تم تفعيل وضع الازعاج عليهم في جميع الجروبات",
        },
        "usage": [
            "{tr}المزعجهم",
            "{tr}المزعجهم الكل",
        ],
    },
)
async def echo(event):  # sourcery no-metrics
    "يعرض قائمة المستخدمين الذين قمت بتمكين وضع الازعاج عليهم."
    input_str = event.pattern_match.group(1)
    private_chats = ""
    output_str = "**⌔︙ قائمه الاشخاص الذين تم ازعاجهم :**\n\n"
    if input_str:
        lsts = get_all_echos()
        group_chats = ""
        if len(lsts) > 0:
            for echos in lsts:
                if echos.chat_type == "Personal":
                    if echos.user_username:
                        private_chats += f"☞ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                    else:
                        private_chats += (
                            f"☞ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                        )
                else:
                    if echos.user_username:
                        group_chats += f"☞ [{echos.user_name}](https://t.me/{echos.user_username}) في مجموعة {echos.chat_name} الايدي `{echos.chat_id}`\n"
                    else:
                        group_chats += f"☞ [{echos.user_name}](tg://user?id={echos.user_id}) في مجموعة {echos.chat_name} الايدي `{echos.chat_id}`\n"

        else:
            return await edit_or_reply(event, "**⌔︙ لم يتم تفعيل ازعاج  اي شخص  ⚠️**")
        if private_chats != "":
            output_str += "**⌔︙ الـدردشـات الـخاصة **\n" + private_chats + "\n\n"
        if group_chats != "":
            output_str += "**⌔︙ دردشـات الـمجموعات **\n" + group_chats
    else:
        lsts = get_echos(event.chat_id)
        if len(lsts) <= 0:
            return await edit_or_reply(
                event, "**لم يتم تفعيل الازعاج بالاصل في هذه الدردشه ⚠️**"
            )

        for echos in lsts:
            if echos.user_username:
                private_chats += (
                    f"☞ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                )
            else:
                private_chats += (
                    f"☞ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                )
        output_str = f"**⌔︙ الاشخاص الذي تم تقليدهم في هذه الدردشه :**\n" + private_chats

    await edit_or_reply(event, output_str)


@catub.cat_cmd(incoming=True, edited=False)
async def samereply(event):
    if is_echo(event.chat_id, event.sender_id) and (
        event.message.text or event.message.sticker
    ):
        await event.reply(event.message)
