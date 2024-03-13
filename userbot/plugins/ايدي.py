# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import html
import os

from requests import get
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_input_location
from userbot import catub
from userbot.core.logger import logging

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers import get_user_from_event, reply_id

plugin_category = "utils"
LOGS = logging.getLogger(__name__)


async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        if isinstance(user, int) or user.startswith("@"):
            user_obj = await event.client.get_entity(user)
            return user_obj
        try:
            user_object = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_object


async def fetch_info(replied_user, event):
    """Get details from the User object."""
    FullUser = (await event.client(GetFullUserRequest(replied_user.id))).full_user
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(user_id=replied_user.id, offset=42, max_id=0, limit=80)    )
    replied_user_profile_photos_count = "لايـوجـد بروفـايـل"
    dc_id = "Can't get dc id"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
        dc_id = replied_user.photo.dc_id
    except AttributeError:
        pass
    user_id = replied_user.id
    first_name = replied_user.first_name
    full_name = FullUser.private_forward_name
    common_chat = FullUser.common_chats_count
    username = replied_user.username
    user_bio = FullUser.about
    is_bot = replied_user.bot
    restricted = replied_user.restricted
    verified = replied_user.verified
    photo = await event.client.download_profile_photo(     user_id,     Config.TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg",    download_big=True  )
    first_name = (      first_name.replace("\u2060", "")
        if first_name
        else ("هذا المستخدم ليس له اسم")
    )
    last_name = last_name.replace("\u2060", "") if last_name else (" ")
    username = "@{}".format(username) if username else ("هذا الشخص لايوجد لديه معرف")
    user_bio = "هذا الشخص لايوجد لديه نــبــذة" if not user_bio else user_bio
    caption = "<b>• ⚜️ | مــعــلــومــات الــمــســتــخــدم :</b>\n"
    caption += f"<b>• ⚜️ | الاســم  :  </b> {first_name} {last_name}\n"
    caption += f"<b>• ⚜️ | الــمــ؏ــࢪفہ  : </b> {username}\n"
    caption += f"<b>• ⚜️ | الايــديہ  :  </b> <code>{user_id}</code>\n"
    caption += f"<b>• ⚜️ | ؏ــدد صــوࢪڪہ  : </b> {replied_user_profile_photos_count}\n"
    caption += f"<b>• ⚜️ | الــنــبــذة  : </b> \n<code>{user_bio}</code>\n\n"
    caption += f"<b>• ⚜️ | الــمــجــمــو؏ــاتہ الـمـشـتـࢪكـة  : </b> {common_chat}\n"
    caption += f"<b>• ⚜️ | رابــط مــبـاشـࢪ لــہ الـحـسـابہ  :  </b> \n"
    caption += f'• ⚜️ | <a href="tg://user?id={user_id}">{first_name}</a> \n'
    return photo, caption



@catub.cat_cmd(
    pattern="^ايدي(?:\s|$)([\s\S]*)",
    command=("ايدي", plugin_category),
    info={
        "header": "الحصول على معلومات للمستخدم.",
        "description": "تفاصيل المستخدم كاملة.",
        "usage": "{tr}ايدي <إسم المستخـدم/معرّف المستخـدم/بالرد>",
    },
)
async def who(event):
    "الحصول على معلومات للمستخدم"
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    replied_user, reason = await get_user_from_event(event)
    if not replied_user:
        return
    cat = await edit_or_reply(event, "`• ⚜️ | جـاري جـلب معلومات المسـتخدم  🆔....`")
    replied_user = await event.client(GetFullUserRequest(replied_user.id))
    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        return await edit_or_reply(cat, "`• ⚜️ | تعذر جلب معلومات هذا المستخدم.`")
    message_id_to_reply = await reply_id(event)
    try:
        await event.client.send_file(
            event.chat_id,
            photo,
            caption=caption,
            link_preview=False,
            force_document=False,
            reply_to=message_id_to_reply,
            parse_mode="html",
        )
        if not photo.startswith("http"):
            os.remove(photo)
        await cat.delete()
    except TypeError:
        await cat.edit(caption, parse_mode="html")


@catub.cat_cmd(
    pattern="^رابط الحساب(?:\s|$)([\s\S]*)",
    command=("رابط الحساب", plugin_category),
    info={
        "header": "للحصول علي رابط لخاص المستخدم.",
        "usage": "{tr}رابط الحساب <إسم المستخـدم/معرّف المستخـدم/بالرد>",
    },
)
async def permalink(mention):
    """للحصول علي رابط لخاص المستخدم مع نص معدل."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"• ⚜️ | [{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"• ⚜️ | [{tag}](tg://user?id={user.id})")
