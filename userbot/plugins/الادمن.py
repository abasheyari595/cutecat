# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

from asyncio import sleep

from telethon import functions
from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    InputChatPhotoEmpty,
    MessageMediaPhoto,
)

from userbot import catub

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID

# =================== STRINGS ============
PP_TOO_SMOL = "**⌔︙الصورة صغيرة جدًا  📸** ."
PP_ERROR = "**⌔︙فشل أثناء معالجة الصورة  📵** ."
NO_ADMIN = "**⌔︙أنا لست مشرف هنا ** ."
NO_PERM = "**⌔︙ليس لدي أذونات كافية  🚮** ."
CHAT_PP_CHANGED = "**⌔︙تغيّرت صورة الدردشة  🌅** ."
INVALID_MEDIA = "**⌔︙ملحق غير صالح  📳** ."

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

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

LOGS = logging.getLogger(__name__)
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

plugin_category = "admin"
# ================================================

@catub.cat_cmd(
    pattern="^(وضع|حذف) الصوره$",
    command=("(وضع|حذف) الصوره", plugin_category),
    info={
        "⌔︙ الأسـتخدام": "لتغيير صورة المجموعة او حذفها",
        "⌔︙ الشـرح": "رد علي الصوره لوضعها كصورة للمجموعه",
        "flags": {
            "وضع": "لوضع صورة للجروب",
            "حذف": "لحذف صورة الجروب",
        },
        "⌔︙ الأمـر": [
            "{tr}وضع الصوره <بالرد علي الصوره>",
            "{tr}حذف الصوره",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def set_group_photo(event):  # sourcery no-metrics
    "⌔︙لتغيير المجموعة  ♌️"
    flag = (event.pattern_match.group(1)).strip()
    if flag == "وضع":
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await edit_delete(event, INVALID_MEDIA)
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await edit_delete(event, CHAT_PP_CHANGED)
            except PhotoCropSizeSmallError:
                return await edit_delete(event, PP_TOO_SMOL)
            except ImageProcessFailedError:
                return await edit_delete(event, PP_ERROR)
            except Exception as e:
                return await edit_delete(event, f"**⌔︙خطأ  ❌ : **`{str(e)}`")
            process = "updated"
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edit_delete(event, f"**♕︙ خطأ : **`{str(e)}`")
        process = "deleted"
        await edit_delete(event, "**⌔︙تـم حذف الـصورة بنـجاح  ✔️**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "⌔︙ صوره_المجموعة\n"
            f"⌔︙ صورة المجموعه {process} بنجاح "
            f"⌔︙ المحادثة  📜 : {event.chat.title}(`{event.chat_id}`)",
        )

@catub.cat_cmd(
    pattern="^رفع مشرف(?: |$)(.*)",
    command=("رفع مشرف", plugin_category),
    info={
        "الامر": "لرفع الشخص مشرف مع صلاحيات",
        "الشرح": "لرفع الشخص مشرف بالمجموعه قم بالرد على الشخص\
            \nNote : You need proper rights for this",
        "الاستخدام": [
            "{tr}رفع مشرف <ايدي/معرف/بالرد عليه>",
            "{tr}رفع مشرف <ايدي/معرف/بالرد عليه> ",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def promote(event):
    "لرفع مشرف بالمجموعه"
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "Admin"
    if not user:
        return
    catevent = await edit_or_reply(event, "**⌔︙يـتم الرفـع  ↗️ **")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    await catevent.edit("**⌔︙تم رفعه مشرف بالمجموعه بنجاح  📤**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"⌔︙ترقية  🆙\
            \n⌔︙المستخدم  🚹 : [{user.first_name}](tg://user?id={user.id})\
            \n⌔︙المحادثة  📜 : {event.chat.title} (`{event.chat_id}`)",
        )

@catub.cat_cmd(
    pattern="^تنزيل مشرف(?: |$)(.*)",
    command=("تنزيل مشرف", plugin_category),
    info={
        "الامر": "لتنزيل الشخص كن الاشراف",
        "الشرح": "يقوم هذا الامر بحذف جميع صلاحيات المشرف\
            \nملاحظه :**لازم تكون انت الشخص الي رفعه او تكون مالك المجموعه حتى تنزله**",
        "الاستخدام": [
            "{tr}تنزيل مشرف <الايدي/المعرف/بالرد عليه>",
            "{tr}تنزيل مشرف <الايدي/المعرف/بالرد عليه>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def demote(event):
    "لتنزيل من رتبة الادمن"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "**⌔︙يـتم التنزيل من الاشراف  ↙️**")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    rank = "admin"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    await catevent.edit("**⌔︙تـم تنزيله من قائمه الادمنيه بنجاح  ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"⌔︙ تنزيل_مشرف\
            \n⌔︙المستخدم  🚹 : [{user.first_name}](tg://user?id={user.id})\
            \n⌔︙المحادثة  📜 : {event.chat.title}(`{event.chat_id}`)",
        )

@catub.cat_cmd(
    pattern="^طرد(?: |$)(.*)",
    command=("طرد", plugin_category),
    info={
        "header": "⌔︙ لطرد شخص من المجموعة ",
        "description": "طرد الشخص من المجموعه يمكنه الانضمام مرة اخري.\
        \nNote : You need proper rights for this.",
        "usage": [
            "{tr}طرد <الايدي/المعرف/بالرد عليه>",
            "{tr}طرد <الايدي/المعرف/بالرد عليه> <السبب>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def endmute(event):
    "⌔︙إستخدم هذا لطرد مستخدم من المحادثة  🚷"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "**⌔︙جاري طرد هذا الشخص من المجموعة  ❎**")
    try:
        await event.client.kick_participant(event.chat_id, user.id)
    except Exception as e:
        return await catevent.edit(NO_PERM + f"\n{str(e)}")
    if reason:
        await catevent.edit(
            f"**⌔︙المستخدم  🚹 : [{user.first_name}](tg://user?id={user.id}) \n تم طـرده بنجاح  ✅ ** n\⌔︙ السـبب: {reason}"
        )
    else:
        await catevent.edit(f"**⌔︙المستخدم  🚹 : [{user.first_name}](tg://user?id={user.id}) \n تم طـرده بنجاح  ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "⌔︙ المطرودين\n"
            f"⌔︙ المستخدمين: [{user.first_name}](tg://user?id={user.id})\n"
            f"⌔︙المحادثة  📜 : {event.chat.title}(`{event.chat_id}`)\n",
        )


@catub.cat_cmd(
    pattern="^تثبيت( بالاشعار|$)",
    command=("تثبيت", plugin_category),
    info={
        "header": "لتثبيت الرسائل في المجموعه",
        "description": "قم بالرد علي الرسالة لتثبيتها\
        \nNote : You need proper rights for this if you want to use in group.",
        "options": {"بالاشعار": "لاشعار جميع اعضاء المجموعه."},
        "usage": [
            "{tr}تثبيت <بالرد علي الرساله>",
            "{tr}تثبيت بالاشعار <بالرد علي الرساله>",
        ],
    },
)
async def pin(event):
    "⌔︙ تثبيت  📌"
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await edit_delete(event, "**⌔︙يرجى الرد على الرسالة التي تريد تثبيتها 📨 **", 5)
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{str(e)}`", 5)
    await edit_delete(event, "**⌔︙تم تثبيت الرسالة بنجاح في هذه الدردشة  📌**", 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"⌔︙ تثبيت  📌\
                \n⌔︙ تم تثبيت الرسالة بنجاح في الدردشة  📌\
                \n⌔︙المستخدم  🚹 : {event.chat.title}(`{event.chat_id}`)\
                \n⌔︙المحادثة  📜 : {is_silent}",
        )


@catub.cat_cmd(
    pattern="^الغاء التثبيت( للكل|$)",
    command=("الغاء التثبيت", plugin_category),
    info={
        "header": "لالغاء تثبيت الرسائل المثبته",
        "description": "قم بالرد علي الرساله لالغاء تثبيتها \
        \nNote : تحتاج إلى الصلاحيات المناسبة لهذا إذا كنت ترغب في استخدامها في المجموعة.",
        "options": {"للكل": "لالغاء تثبيت جميع الرسائل المثبته"},
        "usage": [
            "{tr}الغاء التثبيت <بالرد>",
            "{tr}الغاء التثبيت للكل",
        ],
    },
)
async def pin(event):
    "⌔︙لإلغاء تثبيت رسائل من المجموعة  ⚠️"
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "all":
        return await edit_delete(
            event,
            "⌔︙ يرجى الرد على الرسالة التي تريد تثبيتها استخدم `.الغاء التثبيت للكل`  لالغاء تثبيت جميع الرسائل  📍",
            5,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "للكل":
            await event.client.unpin_message(event.chat_id)
        else:
            return await edit_delete(
                event, "⌔︙ يرجى الرد على الرسالة التي تريد تثبيتها استخدم `.الغاء التثبيت للكل`  لالغاء تثبيت جميع الرسائل  📍", 5
            )
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{str(e)}`", 5)
    await edit_delete(event, "**⌔︙تم الغاء التثبيت بنجاح  ✅**", 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"**⌔︙ الـغاء التثبيت  ❗️ \
                \n** ⌔︙ تم بنجاح الغاء التثبيـت في الدردشة  ✅ \
                \n⌔︙الدردشـه  🔖 : {event.chat.title}(`{event.chat_id}`)",
        )


@catub.cat_cmd(
    pattern="^الاحداث( ر)?(?: |$)(\d*)?",
    command=("الاحداث", plugin_category),
    info={
        "header": "للحصول على الرسائل المحذوفة الأخيرة في المجموعة",
        "description": "للتحقق من الرسائل المحذوفة الأخيرة في المجموعة، سيعرض بشكل افتراضي 5. يمكنك الحصول على 1 إلى 15 رسالة.",
        "flags": {
            "ر": "استخدم هذا مع الامر لتحميل الوسائط للدردشة الاخري سوف تظهر فقط كوسائط."
        },
        "usage": [
            "{tr}الاحداث <العدد>",
            "{tr}الاحداث ر <العدد>",
        ],
        "examples": [
            "{tr}الاحداث 7",
            "{tr}الاحداث ر 7 (هذا سوف يرد 7 رسائل محذوفه لهذه الرسالة",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _iundlt(event):  # sourcery no-metrics
    "⌔︙لأخذ نظرة عن آخر الرسائل المحذوفة في المجموعة  💠"
    catevent = await edit_or_reply(event, "**⌔︙يتم البحث عن اخر الاحداث انتظر  🔍**")
    flag = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        if lim > 15:
            lim = int(15)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(5)
    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )
    deleted_msg = f"**⌔︙ اخر {lim} رسائل محذوفة في هذه المجموعة  🗑 :**"
    if not flag:
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n⌔︙ {msg.old.message} \n **تم ارسالها بـواسطة  🛃** {_format.mentionuser(ruser.first_name ,ruser.id)}"
            else:
                deleted_msg += f"\n⌔︙ {_media_type} \n **تم ارسالها بـواسطة  🛃** {_format.mentionuser(ruser.first_name ,ruser.id)}"
        await edit_or_reply(catevent, deleted_msg)
    else:
        main_msg = await edit_or_reply(catevent, deleted_msg)
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                await main_msg.reply(
                    f"⌔︙ {msg.old.message}\n**تم ارسالها بـواسطة  🛃** {_format.mentionuser(ruser.first_name ,ruser.id)}"
                )
            else:
                await main_msg.reply(
                    f"⌔︙ {msg.old.message}\n**تم ارسالها بـواسطة  🛃** {_format.mentionuser(ruser.first_name ,ruser.id)}",
                    file=msg.old.media,
                )
                
@catub.cat_cmd(
    pattern="^حظر(?:\s|$)([\s\S]*)",
    command=("حظر", plugin_category),
    info={
        "⌔︙ الاستخدام": "يقـوم بـحظر شخـص في الـكروب الءي اسـتخدمت فيـه الامر.",
        "⌔︙ الشرح": "لحـظر شخـص من الكـروب ومـنعه من الأنـضمام مجـددا\
            \n⌔︙ تـحتاج الصلاحـيات لـهذا الأمـر.",
        "⌔︙ الامر": [
            "{tr}حظر <الايدي/المعرف/بالرد عليه>",
            "{tr}حظر <الايدي/المعرف/بالرد عليه> <السبب>",
        ],
    },
    groups_only=True,
    require_admin=True,
) 
async def _ban_person(event):
    "⌔︙ لحـظر شخص في كـروب مـعين"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == event.client.uid:
        return await edit_delete(event, "⌔︙ عـذرا لا تسـتطيع حـظر شـخص")
    catevent = await edit_or_reply(event, "⌔︙ تـم حـظره بـنجاح")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await catevent.edit(
            "⌔︙ ليـس لـدي جـميع الصـلاحيـات لكـن سيـبقى محـظور"
        )
    if reason:
        await catevent.edit(
            f"⌔︙ المسـتخدم {_format.mentionuser(user.first_name ,user.id)} \n ⌔︙ تـم حـظره بنـجاح !!\n**⌔︙السبب : **`{reason}`"
        )
    else:
        await catevent.edit(
            f"⌔︙ المسـتخدم {_format.mentionuser(user.first_name ,user.id)} \n ⌔︙ تـم حـظره بنـجاح ✅"
        )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙ الحـظر\
                \nالمسـتخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالـدردشـة: {event.chat.title}\
                \nايدي الكروب(`{event.chat_id}`)\
                \nالسبـب : {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙ الحـظر\
                \nالمسـتخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالـدردشـة: {event.chat.title}\
                \n ايـدي الكـروب: (`{event.chat_id}`)",
            )

@catub.cat_cmd(
    pattern="^الغاء حظر(?:\s|$)([\s\S]*)",
    command=("الغاء حظر", plugin_category),
    info={
        "⌔︙ الأسـتخدام": "يقـوم بـالغاء حـظر الشـخص في الـكروب الذي اسـتخدمت فيـه الامر.",
        "⌔︙ الشرح": "لألـغاء حـظر شخـص من الكـروب والسـماح له من الأنـضمام مجـددا\
            \n⌔︙ تـحتاج الصلاحـيات لـهذا الأمـر.",
        "⌔︙ الأمـر": [
            "{tr}الغاء حظر <الايدي/المعرف/بالرد عليه>",
            "{tr}الغاء حظر <الايدي/المعرف/بالرد عليه> <السبب> ",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def nothanos(event):
    "⌔︙ لألـغاء الـحظر لـشخص في كـروب مـعين"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "⌔︙ جـار الـغاء الـحظر أنتـظر")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await catevent.edit(
            f"⌔︙ الـمستخدم {_format.mentionuser(user.first_name ,user.id)}\n ⌔︙ تـم الـغاء حـظره بنـجاح "
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "⌔︙ الـغاء الـحظر \n"
                f"الـمستخدم: [{user.first_name}](tg://user?id={user.id})\n"
                f"الـدردشـة: {event.chat.title}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await catevent.edit("⌔︙ يـبدو أن هذه الـعمليـة تم إلغاؤهـا")
    except Exception as e:
        await catevent.edit(f"**خـطأ :**\n`{e}`")


@catub.cat_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))

@catub.cat_cmd(
    pattern="^كتم(?: |$)(.*)",
    command=("كتم", plugin_category),
    info={
        "⌔︙ الأسـتخدام": "لكتـم الشـخص في الـمجموعة التي تـرسل الأمر بهـا",
        "⌔︙ الشـرح": "إذا لم يكن المشرف بعد قم بتغيير صلاحياته في المجموعة,\
            إذا كان المسؤول أو إذا حاولت في الدردشة الشخصية، فسيتم حذف رسائله\
            \n⌔︙ تـحتاج الصلاحـيات لـهذا الأمـر.",
        "⌔︙ الأمـر": [
            "{tr}كتم <الايدي/المعرف/بالرد عليه>",
            "{tr}كتم <الايدي/المعرف/بالرد عليه> <السبب> ",
        ],
    },  # sourcery no-metrics
)
async def startmute(event):
    "لكتـم الشـخص في الـمجموعة التي تـرسل الأمر بهـا"
    if event.is_private:
        await event.edit("**⌔︙ قـد تـكون هـنالك بـعض المـشاكل والأخطـاء**")
        await sleep(2)
        await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "**⌔︙ هـذا الـشخص بالـفعـل مكـتوم**"
            )
        if event.chat_id == event.client.uid:
            return await edit_delete(event, "**⌔︙ لا يـمكنك حـظر نـفسك**")
        try:
            mute(event.chat_id, event.chat_id)
        except Exception as e:
            await event.edit(f"**خـطأ **\n`{str(e)}`")
        else:
            await event.edit("**⌔︙ تـم كـتم الـمستـخدم بـنجاح ✅**")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔︙ الـكتم **\n"
                f"**المسـتخدم :** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return await edit_or_reply(
                event, "**⌔︙ تـحتاج الصلاحـيات لـهذا الأمـر**"
            )
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == event.client.uid:
            return await edit_or_reply(event, "**⌔︙ لا يـمكنك حـظر نـفسك**")
        if is_muted(user.id, event.chat_id):
            return await edit_or_reply(
                event, "**⌔︙ هـذا الـشخص بالـفعـل مكـتوم**"
            )
        result = await event.client(
            functions.channels.GetParticipantRequest(event.chat_id, user.id)
        )
        try:
            if result.participant.banned_rights.send_messages:
                return await edit_or_reply(
                    event,
                    "**⌔︙ هـذا الـشخص بالـفعـل مكـتوم**",
                )
        except AttributeError:
            pass
        except Exception as e:
            return await edit_or_reply(event, f"**خـطأ : **`{str(e)}`", 10)
        try:
            await event.client(EditBannedRequest(event.chat_id, user.id, MUTE_RIGHTS))
        except UserAdminInvalidError:
            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
                if chat.admin_rights.delete_messages is not True:
                    return await edit_or_reply(
                        event,
                        "**⌔︙ تـحتاج صـلاحـيات الـحذف لـهذا الأمـر**",
                    )
            elif "creator" not in vars(chat):
                return await edit_or_reply(
                    event, "**⌔︙ تـحتاج الصلاحـيات لـهذا الأمـر **"
                )
            mute(user.id, event.chat_id)
        except Exception as e:
            return await edit_or_reply(event, f"**Error : **`{str(e)}`", 10)
        if reason:
            await edit_or_reply(
                event,
                f"**⌔︙ الـمستخدم** {_format.mentionuser(user.first_name ,user.id)}\n **⌔︙ تـم كتمه بنـجاح**\n **⌔︙ الدردشـة** {event.chat.title}\n"
                f"**⌔︙ السـبب:** {reason}",
            )
        else:
            await edit_or_reply(
                event,
                f"**⌔︙ الـمستخدم :** {_format.mentionuser(user.first_name ,user.id)}\n **⌔︙ تـم كتمه بنـجاح ✅**\n **⌔︙ الدردشـة** {event.chat.title}"
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔︙ الـكتم**\n"
                f"**الـمستخدم :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**الـدردشـة :** {event.chat.title}\n"
                f"**ايدي الكروب:** (`{event.chat_id}`)",
            )

@catub.cat_cmd(
    pattern="^الغاء كتم(?: |$)(.*)",
    command=("الغاء كتم", plugin_category),
    info={
        "⌔︙ الأسـتخدام": "لألـغاء كتـم الشـخص ",
        "⌔︙ الشـرح": "لألـغاء كتـم الشـخص في الـمجموعة التي تـرسل الأمر بهـا.\
        \n⌔︙ تـحتاج الصلاحـيات لـهذا الأمـر.",
        "⌔︙ الأمـر": [
            "{tr}الغاء كتم <الايدي/المعرف/بالرد عليه>",
            "{tr}الغاء كتم <الايدي/المعرف/بالرد عليه> <السبب> ",
        ],
    },
)
async def endmute(event):
    "لألـغاء كتـم الشـخص في الـمجموعة التي تـرسل الأمر بهـا"
    if event.is_private:
        await event.edit("**⌔︙ قـد تـحدث بعـض الأخـطاء**")
        await sleep(1)
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if not is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "**⌔︙ هـذا الـمستخدم لـيس مكـتوم**"
            )
        try:
            unmute(event.chat_id, event.chat_id)
        except Exception as e:
            await event.edit(f"**خـطأ **\n`{str(e)}`")
        else:
            await event.edit(
                "**⌔︙ تـم الـغاء كـتم الـمستـخدم بـنجاح**"
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔︙ الـغاء الكـتم**\n"
                f"**الـمستخدم :** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        user, _ = await get_user_from_event(event)
        if not user:
            return
        try:
            if is_muted(user.id, event.chat_id):
                unmute(user.id, event.chat_id)
            else:
                result = await event.client(
                    functions.channels.GetParticipantRequest(event.chat_id, user.id)
                )
                if result.participant.banned_rights.send_messages:
                    await event.client(
                        EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS)
                    )
        except AttributeError:
            return await edit_or_reply(
                event,
                "**⌔︙ هـذا الـمستخدم يسـتطيع الـتحدث بِـحريـة هـنا**",
            )
        except Exception as e:
            return await edit_or_reply(event, f"**خـطأ : **`{str(e)}`")
        await edit_or_reply(
            event,
            f"**⌔︙ الـمستخدم** {_format.mentionuser(user.first_name ,user.id)}\n ⌔︙ تـم الـغاء كتـمه\n **⌔︙ الدردشة** {event.chat.title}",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔︙ الـغاء الكـتم**\n"
                f"**المـستخدم :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**الـدردشـة :** {event.chat.title}(`{event.chat_id}`)",
            )
@catub.cat_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()            
