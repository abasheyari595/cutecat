# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

from telethon.errors import BadRequestError
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from userbot import catub

from ..core.managers import edit_or_reply
from ..helpers.utils import _format
from . import BOTLOG, BOTLOG_CHATID, extract_time, get_user_from_event

plugin_category = "admin"

# =================== CONSTANT ===================
NO_ADMIN = "**▾↫ عذرًا انا لست مشرفًا هنا! **"
NO_PERM = "**▾↫ عذرًا احتاج الى صلاحيات! **"


@catub.cat_cmd(
    pattern="^قيده(?:\s|$)([\s\S]*)",
    command=("قيده", plugin_category),
    info={
        "header": "لتقيـيـد المسـتخـدم من ارسـال الـرسـائل مـؤقـتا",
        "description": "لـكتـم مستخـدم مؤقـتا مـع وقـت انـت تحـدده.",
        "وحـدات الـوقت": {
            "s": "بالثـواني",
            "m": "بالـدقائق",
            "h": "بالـساعات",
            "d": "بالأيـام",
            "w": "بالأسـابيع",
        },
        "usage": [
            "{tr}قيده <ايدي/معرف/بالرد> <وقت>",
            "{tr}قيده <ايدي/معرف/بالرد> <وقت> <سبب>",
        ],
        "examples": ["{tr}قيده لتـقـييـد المسـتخـدم لـمدة يومـين"],
    },
    groups_only=True,
    require_admin=True,
)
async def tmuter(event):  # sourcery no-metrics
    "لتقييد شخص من المجموعة بشكل مؤقت"
    catevent = await edit_or_reply(event, "**▾∮ جاري** `┆تقييد┆` **المستخدم ✘ ...**")
    user, reason = await get_user_from_event(event, catevent)
    if not user:
        return
    if not reason:
        return await catevent.edit(
            "**▾∮ لم تقم بذكر الوقت الامر الصحيح ↶**\n__▾قيده <ايدي/اسم مستخدم/رد> <3h>__\n**▾∮واذا لم تعرف فارسل** `مساعدة قيده`"
        )
    reason = reason.split(" ", 1)
    hmm = len(reason)
    cattime = reason[0].strip()
    reason = "".join(reason[1:]) if hmm > 1 else None
    ctime = await extract_time(catevent, cattime)
    if not ctime:
        return
    if user.id == event.client.uid:
        return await catevent.edit(f"**▾∮ عذرًا لا يمكنني ┆تقييد┆ نفسي! ✘**")
    try:
        await catevent.client(
            EditBannedRequest(
                event.chat_id,
                user.id,
                ChatBannedRights(until_date=ctime, send_messages=True),
            )
        )
        # Announce that the function is done
        if reason:
            await catevent.edit(
                f"**▾∮ تم تقييد المستخدم مؤقتًا 🚷 ↫ **{_format.mentionuser(user.first_name ,user.id)} ✓\n**▾∮ الوقت 🕐 ↫**`┆{cattime}┆`\n**▾∮ السبب 📝↫** `{reason}`"
            )
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "**⌔∮ الان عملية**`┆تقييد┆`**مؤقت ☟**\n\n"
                    f"**▾∮ تم **`┆تقييد┆`**المستخدم 🚷 ↫ ** [{user.first_name}](tg://user?id={user.id}) ✓\n**▾∮ اسم المجموعة ✎ ↫** 『`{event.chat.title}`』\n**▾∮ ايدي المجموعة 🆔 ↫** 「`{event.chat_id}`」\n**▾∮ الوقت 🕐 ↫**`┆{cattime}┆`\n**▾∮ السبب 📝↫** `{reason}`",
                )
        else:
            await catevent.edit(
                f"**▾∮ تم تقييد المستخدم مؤقتًا 🚷 ↫ **{_format.mentionuser(user.first_name ,user.id)} ✓\n**▾∮ الوقت 🕐 ↫**`┆{cattime}┆`\n"
            )
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "**⌔∮ الان عملية**`┆تقييد┆`**مؤقت ☟**\n\n"
                    f"**▾∮ تم **`┆تقييد┆`**المستخدم 🚷 ↫ ** [{user.first_name}](tg://user?id={user.id}) ✓\n**▾∮ اسم المجموعة ✎ ↫** 『`{event.chat.title}`』\n**▾∮ ايدي المجموعة 🆔 ↫** 「`{event.chat_id}`」\n**▾∮ الوقت 🕐 ↫**`┆{cattime}┆`",
                )
        # Announce to logging group
    except UserIdInvalidError:
        return await catevent.edit("**▾∮ قد تحدث مشاكل او اخطاء غير متوقعة! **")
    except UserAdminInvalidError:
        return await catevent.edit("**▾∮ لا تستطيع** `┆تقييد┆` **المشرفين! ✘**")
    except Exception as e:
        return await catevent.edit(f"`{str(e)}`")


@catub.cat_cmd(
    pattern="^حظره(?:\s|$)([\s\S]*)",
    command=("حظره", plugin_category),
    info={
        "header": "لحـظر المسـتخـدم من مجمـوعة معيـنة مـؤقـتا",
        "description": "لحـظر مستخـدم مؤقـتا مـع وقـت انـت تحـدده.",
        "وحـدات الـوقت": {
            "s": "بالثـواني",
            "m": "بالـدقائق",
            "h": "بالـساعات",
            "d": "بالأيـام",
            "w": "بالأسـابيع",
        },
        "usage": [
            "{tr}حظره <ايدي/معرف/بالرد> <وقت>",
            "{tr}حظره <ايدي/معرف/بالرد> <وقت> <سبب>",
        ],
        "examples": ["{tr}حظره لحـظر المسـتخـدم لـمدة يومـين"],
    },
    groups_only=True,
    require_admin=True,
)
async def tban(event):  # sourcery no-metrics
    "To ban a person for specific time"
    catevent = await edit_or_reply(event, "`banning....`")
    user, reason = await get_user_from_event(event, catevent)
    if not user:
        return
    if not reason:
        return await catevent.edit(
            "**▾∮ لم تقم بذكر الوقت الامر الصحيح ↶**\n__▾حضره <ايدي/اسم مستخدم/رد> <3h>__\n**▾∮واذا لم تعرف فارسل** `مساعدة حضره`"
        )
    reason = reason.split(" ", 1)
    hmm = len(reason)
    cattime = reason[0].strip()
    reason = "".join(reason[1:]) if hmm > 1 else None
    ctime = await extract_time(catevent, cattime)
    if not ctime:
        return
    if user.id == event.client.uid:
        return await catevent.edit(f"**▾∮ عذرًا لا يمكنني ┆حظر┆ نفسي! ✘**")
    await catevent.edit("**▾∮ جاري  ┆حظر┆ المستخدم ✘ ...**")
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id,
                user.id,
                ChatBannedRights(until_date=ctime, view_messages=True),
            )
        )
    except UserAdminInvalidError:
        return await catevent.edit("**▾∮ لا تستطيع** `┆حظر┆` **المشرفين! ✘**")
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    # Helps ban group join spammers more easily
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await catevent.edit(
            "`I dont have message nuking rights! But still he was banned!`"
        )
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await catevent.edit(
            f"**▾∮ تم ┆حظر┆ المستخدم مؤقتًا ⛔️ ↫ **{_format.mentionuser(user.first_name ,user.id)} ✓\n**▾∮ الوقت 🕐 ↫**`┆{cattime}┆`\n**▾∮ السبب 📝↫**  `{reason}`"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔∮ الان عملية** `┆حظر┆` **مؤقت ⚠️ ☟**\n\n"
                f"**▾∮ تم ** `┆حظر┆` **المستخدم ⛔️ ↫ ** [{user.first_name}](tg://user?id={user.id}) ✓\n**▾∮ اسم المجموعة ✎ ↫** 『`{event.chat.title}`』\n**▾∮ ايدي المجموعة 🆔 ↫** 「`{event.chat_id}`」\n**▾∮ الوقت 🕐 ↫**`┆{cattime}┆`\n**▾∮ السبب 📝↫** `{reason}`",
            )
    else:
        await catevent.edit(
            f"**▾∮ تم ┆حظر┆ المستخدم مؤقتًا ⛔️ ↫ **{_format.mentionuser(user.first_name ,user.id)} ✓\n**▾∮ الوقت 🕐 ↫**`┆{cattime}┆`\n"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔∮ الان عملية** `┆حظر┆` **مؤقت ⚠️ ☟**\n\n"
                f"**▾∮ تم ** `┆حظر┆` **المستخدم ⛔️ ↫ ** [{user.first_name}](tg://user?id={user.id}) ✓\n**▾∮ اسم المجموعة ✎ ↫** 『`{event.chat.title}`』\n**▾∮ ايدي المجموعة 🆔 ↫** 「`{event.chat_id}`」\n**▾∮ الوقت 🕐 ↫**`┆{cattime}┆`",
            )
