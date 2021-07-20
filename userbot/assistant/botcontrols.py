import asyncio
from datetime import datetime

from telethon.errors import BadRequestError, FloodWaitError, ForbiddenError

from userbot import catub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import reply_id, time_formatter
from ..helpers.utils import _format
from ..sql_helper.bot_blacklists import check_is_black_list, get_all_bl_users
from ..sql_helper.bot_starters import del_starter_from_db, get_all_starters
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID
from .botmanagers import (
    ban_user_from_bot,
    get_user_and_reason,
    progress_str,
    unban_user_from_bot,
)

LOGS = logging.getLogger(__name__)

plugin_category = "bot"
botusername = Config.TG_BOT_USERNAME
cmhd = Config.COMMAND_HAND_LER


@catub.bot_cmd(
    pattern=f"^/help$",
    from_users=Config.OWNER_ID,
)
async def bot_help(event):
    await event.reply(
        f"""اوامر البوت هي :
**ملاحظة : **هذه الاوامر تعمل فقط في الـبوت {botusername}

• **الامر : **/معلومات <بالرد على رسالة المستخدم>
• **المعلومات : ** من خلال هذا الامر يمكنك معرف من الشخص الذي ارسل تاملصق او المتحركه للبوت  ،
• **ملاحظة : **تعمل لجميع المستخدمين حتى الذين فعلاو خصوصية التحويل

• **الامر : **/بلوك <السبب> او   /حظر <المعرف/ايدي المستخدم> <السبب>
• **المعلومات : ** قم بالرد على الرسالة مع السبب ليتم حظره وتبليغك لاحقا بإنه محظور
• **ملاحظة : ** السبب مطلوب بدون السبب الامر لا يشتغل

• **الامر : **/انبلوك <السبب> او   /الغاء حظر <المعرف/الايدي>
• **المعلومات : **قم بالرد على المستخدم مع السبب او ارسل فقط الامر مع الايدي او المعرف
• **ملاحظة : ** للتأكد من قائمة المحظورين ارسل  `{cmhd}المحظورين`.

• **الامر : **/اذاعة
• **المعلومات : ** لعمل اذاعة لجميع المستخدمين بالرد على الرسالة ولرؤية مستخدمين البوت ارسل  `{cmhd}المستخدمين`.
• **ملاحظة : ** اذا الشخص قام بايقاف البوت او حظره الرسائل لم تصل اليه بسبب ارتباط قاعده البيانات
"""
    )


@catub.bot_cmd(
    pattern=f"^/اذاعة$",
    from_users=Config.OWNER_ID,
)
async def bot_broadcast(event):
    replied = await event.get_reply_message()
    if not replied:
        return await event.reply("قم بالرد على الرسالة للأذاعه !")
    start_ = datetime.now()
    br_cast = await replied.reply("يتم الأذاعه للجميع ...")
    blocked_users = []
    count = 0
    bot_users_count = len(get_all_starters())
    if bot_users_count == 0:
        return await event.reply("لا يوجد اي شخص يستخدم بوتك")
    for user in get_all_starters():
        try:
            await event.client.send_message(
                int(user.user_id), "🔊 تم استلام اذاعه جديدة."
            )
            await event.client.send_message(int(user.user_id), replied)
            await asyncio.sleep(0.8)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except (BadRequestError, ForbiddenError):
            del_starter_from_db(int(user.user_id))
        except Exception:
            LOGS.error(str(e))
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID, f"**خطأ في الأذاعة **\n`{str(e)}`"
                )
        else:
            count += 1
            if count % 5 == 0:
                try:
                    prog_ = (
                        "🔊 الأذاعه العامه ...\n\n"
                        + progress_str(
                            total=bot_users_count,
                            current=count + len(blocked_users),
                        )
                        + f"\n\n• ✔️ **بنـجاح* :  `{count}`\n"
                        + f"• ✖️ **خطأ** :  `{len(blocked_users)}`"
                    )
                    await br_cast.edit(prog_)
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
    end_ = datetime.now()
    b_info = f"🔊 تـم بنجاح الأذاعه الى ➜  <b>{count} من المستخدمين.</b>"
    if len(blocked_users) != 0:
        b_info += f"\n🚫  <b>{len(blocked_users)} من المستخدمين</b> قام بحظر بوتك اذا تم حذف الرسالة."
    b_info += (
        f"\n⏳  <code> العملية اخذت: {time_formatter((end_ - start_).seconds)}</code>."
    )
    await br_cast.edit(b_info, parse_mode="html")


@catub.cat_cmd(
    pattern=f"المستخدمين$",
    command=("المستخدمين", plugin_category),
    info={
        "header": "To get users list who started bot.",
        "description": "To get compelete list of users who started your bot",
        "usage": "{tr}bot_users",
    },
)
async def ban_starters(event):
    "للحصول على مستخدمين البوت."
    ulist = get_all_starters()
    if len(ulist) == 0:
        return await edit_delete(event, "** ليم يستخدم اي احد بوتك**")
    msg = "**قائمه مستخدمين البوت :\n\n**"
    for user in ulist:
        msg += f"• 👤 {_format.mentionuser(user.first_name , user.user_id)}\n**الايدي:** `{user.user_id}`\n**المعرفات:** @{user.username}\n**التاريخ: **__{user.date}__\n\n"
    await edit_or_reply(event, msg)


@catub.bot_cmd(
    pattern=f"^/بلوك\s+(.*)",
    from_users=Config.OWNER_ID,
)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, "لا يمكنني العثور على المستخدم", reply_to=reply_to
        )
    if not reason:
        return await event.client.send_message(
            event.chat_id, "لحظر شخص اكتب السبب اولا", reply_to=reply_to
        )
    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**خطأ:**\n`{str(e)}`")
    if user_id == Config.OWNER_ID:
        return await event.reply("لا أستطيع حظر مالك البوت")
    check = check_is_black_list(user.id)
    if check:
        return await event.client.send_message(
            event.chat_id,
            f"#بالفعل_محظور\
            \nهذا المستخدم موجود في قائمه المحظورين\
            \n**سبب الحظر:** `{check.reason}`\
            \n**التاريخ:** `{check.date}`.",
        )
    msg = await ban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@catub.bot_cmd(
    pattern=f"^/انبلوك(?: |$)(.*)",
    from_users=Config.OWNER_ID,
)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, "`I can't find user to unban`", reply_to=reply_to
        )
    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**Error:**\n`{str(e)}`")
    check = check_is_black_list(user.id)
    if not check:
        return await event.client.send_message(
            event.chat_id,
            f"#User_Not_Banned\
            \n👤 {_format.mentionuser(user.first_name , user.id)} doesn't exist in my Banned Users list.",
        )
    msg = await unban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@catub.cat_cmd(
    pattern=f"المحظورين$",
    command=("المحظورين", plugin_category),
    info={
        "header": "To get users list who are banned in bot.",
        "description": "To get list of users who are banned in bot.",
        "usage": "{tr}bblist",
    },
)
async def ban_starters(event):
    "To get list of users who are banned in bot."
    ulist = get_all_bl_users()
    if len(ulist) == 0:
        return await edit_delete(event, "`No one is banned in your bot yet.`")
    msg = "**The list of users who are banned in your bot are :\n\n**"
    for user in ulist:
        msg += f"• 👤 {_format.mentionuser(user.first_name , user.chat_id)}\n**ID:** `{user.chat_id}`\n**UserName:** @{user.username}\n**Date: **__{user.date}__\n**Reason:** __{user.reason}__\n\n"
    await edit_or_reply(event, msg)


@catub.cat_cmd(
    pattern=f"التكرار (on|off)$",
    command=("التكرار", plugin_category),
    info={
        "header": "To enable or disable bot antiflood.",
        "description": "if it was turned on then after 10 messages or 10 edits of same messages in less time then your bot auto loacks them.",
        "usage": [
            "{tr}bot_antif on",
            "{tr}bot_antif off",
        ],
    },
)
async def ban_antiflood(event):
    "To enable or disable bot antiflood."
    input_str = event.pattern_match.group(1)
    if input_str == "on":
        if gvarstatus("bot_antif") is not None:
            return await edit_delete(event, "`Bot Antiflood was already enabled.`")
        addgvar("bot_antif", True)
        await edit_delete(event, "`Bot Antiflood Enabled.`")
    elif input_str == "off":
        if gvarstatus("bot_antif") is None:
            return await edit_delete(event, "`Bot Antiflood was already disabled.`")
        delgvar("bot_antif")
        await edit_delete(event, "`Bot Antiflood Disabled.`")
