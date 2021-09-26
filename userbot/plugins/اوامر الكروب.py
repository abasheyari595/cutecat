# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

from asyncio import sleep

from telethon.errors import (
    ChatAdminRequiredError,
    FloodWaitError,
    MessageNotModifiedError,
    UserAdminInvalidError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsKicked,
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)

from userbot import catub

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import readable_time
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)
plugin_category = "admin"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


async def ban_user(chat_id, i, rights):
    try:
        await iqthon(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)


@catub.cat_cmd(
    pattern="^اطردني$",
    command=("اطردني", plugin_category),
    info={
        "header": "للمغادره من المجموعه.",
        "usage": [
            "{tr}اطردني",
        ],
    },
    groups_only=True,
)
async def kickme(leave):
    "للمغادره من المجموعه."
    await leave.edit("**⌔︙ جـاري مـغادرة المجـموعة مـع السـلامة  🚶‍♂️**")
    await leave.client.kick_participant(leave.chat_id, "me")

@catub.cat_cmd(
    pattern="^تفليش بالطرد$",
    command=("تفليش بالطرد", plugin_category),
    info={
        "header": "لطرد جميع اعضاء الجروب.",
        "description": "لطرد كل اعضاء الجروب باستثناء الادمن.",
        "usage": [
            "{tr}تفليش بالطرد",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "لطرد جميع اعضاء الجروب."
    result = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, event.client.uid)
    )
    if not result.participant.admin_rights.ban_users:
        return await edit_or_reply(
            event, "⌔︙ - يبدو انه ليس لديك صلاحيات الحذف في هذه الدردشة "
        )
    catevent = await edit_or_reply(event, "`يتم الطرد انتظر قليلا `")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client.kick_participant(event.chat_id, user.id)
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await catevent.edit(
        f"⌔︙  تم بنجاح طرد من {total} الاعضاء ✅ "
    )


@catub.cat_cmd(
    pattern="^تفليش بالحظر$",
    command=("تفليش بالحظر", plugin_category),
    info={
        "header": "لحظر جميع اعضاء الجروب.",
        "description": "لحظر جميع اعضاء الجروب باستثناء الادمن.",
        "usage": [
            "{tr}تفليش بالحظر",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "لحظر جميع أعضاء الجروب."
    result = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, event.client.uid)
    )
    if not result:
        return await edit_or_reply(
            event, "⌔︙ - يبدو انه ليس لديك صلاحيات الحذف في هذه الدردشة ❕"
        )
    catevent = await edit_or_reply(event, "`جار الحظر انتظر قليلا  `")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
                success += 1
                await sleep(0.5) # for avoid any flood waits !!-> do not remove it 
        except Exception as e:
            LOGS.info(str(e))
    await catevent.edit(
        f"⌔︙  تم بنجاح حظر من {total} الاعضاء ✅ "
    )

@catub.cat_cmd(
    pattern="^مسح المحظورين$",
    command=("مسح المحظورين", plugin_category),
    info={
        "header": "إلغاء حظر جميع الحسابات المحظورة في المجموعة.",
        "usage": [
            "{tr}مسح المحظورين",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "To unban all banned users from group."
    catevent = await edit_or_reply(
        event, "**⌔︙  إلغاء حظر جميع الحسابات المحظورة في هذه المجموعة 🆘**"
    )
    succ = 0
    total = 0
    flag = False
    chat = await event.get_chat()
    async for i in event.client.iter_participants(
        event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
    ):
        total += 1
        rights = ChatBannedRights(until_date=0, view_messages=False)
        try:
            await event.client(
                functions.channels.EditBannedRequest(event.chat_id, i, rights)
            )
        except FloodWaitError as e:
            LOGS.warn(f"**⌔︙ هناك ضغط كبير بالاستخدام يرجى الانتضار .. ‼️ بسبب  : {e.seconds} **")
            await catevent.edit(
                f"**⌔︙ {readable_time(e.seconds)} مطلـوب المـعاودة مـرة اخـرى للـمسح 🔁 **"
            )
            await sleep(e.seconds + 5)
        except Exception as ex:
            await catevent.edit(str(ex))
        else:
            succ += 1
            if flag:
                await sleep(2)
            else:
                await sleep(1)
            try:
                if succ % 10 == 0:
                    await catevent.edit(
                        f"**⌔︙ جـاري مسـح المحـظورين ⭕️  : \n {succ} الحسـابات الـتي غيـر محظـورة لحـد الان.**"
                    )
            except MessageNotModifiedError:
                pass
    await catevent.edit(f"**⌔︙ تـم مسـح المحـظورين مـن أصـل 🆘 :**{succ}/{total} \n اسـم المجـموعـة 📄 : {chat.title}")



@catub.cat_cmd(
    pattern="^المحذوفين ?([\s\S]*)",
    command=("المحذوفين", plugin_category),
    info={
        "header": "للتحقق من الحسابات المحذوفة وازالتها",
        "description": "عمليات البحث عن الحسابات المحذوفة في مجموعة. استخدم `.تنظيف المحذوفين` لإزالة الحسابات المحذوفة من المجموعة..",
        "usage": ["{tr}المحذوفين", "{tr}تنظيف المحذوفين"],
    },
    groups_only=True,
)
async def rm_deletedacc(show):
    "للتحقق من الحسابات المحذوفة وازالتها"
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**⌔︙لا توجـد حـسابات محذوفـة في هـذه المجموعـة !**"
    if con != "تنظيف":
        event = await edit_or_reply(
            show, "**⌔︙جـاري البحـث عـن الحسابـات المحذوفـة ⌯**"
        )
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"**⌔︙لقد وجـدت  {del_u}  من  حسابـات محذوفـة في هـذه المجموعـة لحذفهـم إستخـدم الأمـر  ⩥ :  `.المحذوفين تنظيف`"
        await event.edit(del_status)
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_delete(show, "⌔︙أنـا لسـت مشـرفـاً هنـا !", 5)
        return
    event = await edit_or_reply(
        show, "**⌔︙جـاري حـذف الحسـابات المحذوفـة ⌯**"
    )
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client.kick_participant(show.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_delete(event, "**⌔︙  ليس لدي صلاحيات الحظر هنا**", 5)
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"**⌔︙تـم حـذف  {del_u}  الحسـابات المحذوفـة ✓**"
    if del_a > 0:
        del_status = f"**⌔︙تـم حـذف {del_u} الحسـابات المحذوفـة، ولڪـن لـم يتـم حذف الحسـابات المحذوفـة للمشرفيـن !**"
    await edit_delete(event, del_status, 5)
    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            f"**⌔︙تنظيف :**\
            \n⌔︙ {del_status}\
            \n*⌔︙المحادثـة ⌂** {show.chat.title}(`{show.chat_id}`)",
        )


@catub.cat_cmd(
    pattern="^احصائيات الاعضاء ?([\s\S]*)",
    command=("احصائيات الاعضاء", plugin_category),
    info={
        "header": "للحصول على ملخص موجز للأعضاء في المجموعة",
        "description": "للحصول على ملخص موجز للأعضاء في المجموعة. بحاجة إلى إضافة بعض الميزات في المستقبل.",
        "usage": [
            "{tr}احصائيات الاعضاء",
        ],
    },
    groups_only=True,
)
async def _(event):  # sourcery no-metrics
    "للحصول على ملخص موجز للأعضاء في المجموعة"
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not chat.admin_rights and not chat.creator:
            await edit_or_reply(event, "**⌔︙ انت لست مشرف هنا**")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    et = await edit_or_reply(event, "**⌔︙ جـاري البحـث عـن قوائـم المشارڪيـن ⌯**")
    async for i in event.client.iter_participants(event.chat_id):
        p += 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            y += 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**⌔︙أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastMonth):
            m += 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**⌔︙أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastWeek):
            w += 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**⌔︙أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusOffline):
            o += 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("**⌔︙أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusOnline):
            q += 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("**⌔︙أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusRecently):
            r += 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**⌔︙أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
        if i.bot:
            b += 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("**⌔︙ احتاج الى صلاحيات المشرفين للقيام بهذا الامر **")
                    e.append(str(e))
                    break
                else:
                    c += 1
        elif i.deleted:
            d += 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**⌔︙أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
        elif i.status is None:
            n += 1
    if input_str:
        required_string = """**⌔︙ الـمطرودين {} / {} الأعـضاء
⌔︙ الحـسابـات المـحذوفة: {}
⌔︙ حـالة المستـخدم الفـارغه: {}
⌔︙ اخر ظهور منذ شـهر: {}
⌔︙ اخر ظـهور منـذ اسبوع: {}
⌔︙ غير متصل: {}
⌔︙ المستخدمين النشطون: {}
⌔︙ اخر ظهور قبل قليل: {}
⌔︙ البوتات: {}
⌔︙ مـلاحظة: {}**"""
        await et.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await sleep(5)
    await et.edit(
        """**⌔︙ : {} مـجموع المـستخدمين
⌔︙ الحـسابـات المـحذوفة: {}
⌔︙ حـالة المستـخدم الفـارغه: {}
⌔︙ اخر ظهور منذ شـهر: {}
⌔︙ اخر ظـهور منـذ اسبوع: {}
⌔︙ غير متصل: {}
⌔︙ المستخدمين النشطون: {}
⌔︙ اخر ظهور قبل قليل: {}
⌔︙ البوتات: {}
⌔︙ مـلاحظة: {}**""".format(
            p, d, y, m, w, o, q, r, b, n
        )
    )
