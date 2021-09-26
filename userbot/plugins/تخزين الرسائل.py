import asyncio

# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

from userbot import catub
from userbot.core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete
from ..helpers.tools import media_type
from ..helpers.utils import _format
from ..sql_helper import no_log_pms_sql
from ..sql_helper.globals import addgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)

plugin_category = "utils"


class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


LOG_CHATS_ = LOG_CHATS()


@catub.cat_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def monito_p_m_s(event):  # sourcery no-metrics
    if Config.PM_LOGGER_GROUP_ID == -100:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    sender = await event.get_sender()
    if not sender.bot:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id) and chat.id != 777000:
            if LOG_CHATS_.RECENT_USER != chat.id:
                LOG_CHATS_.RECENT_USER = chat.id
                if LOG_CHATS_.NEWPM:
                    if LOG_CHATS_.COUNT > 1:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                "**⌔︙ **رسـالة جـديدة", f"{LOG_CHATS_.COUNT} "
                            )
                        )
                    else:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                "**⌔︙ **رسـالة جـديدة", f"{LOG_CHATS_.COUNT} "
                            )
                        )
                    LOG_CHATS_.COUNT = 0
                LOG_CHATS_.NEWPM = await event.client.send_message(
                    Config.PM_LOGGER_GROUP_ID,
                    f"**⌔︙ المسـتخدم ** {_format.mentionuser(sender.first_name , sender.id)}\n **⌔︙  ارسـل رسـالة جديدة **\n**⌔︙ الايدي :** `{chat.id}`",
                )
            try:
                if event.message:
                    await event.client.forward_messages(
                        Config.PM_LOGGER_GROUP_ID, event.message, silent=True
                    )
                LOG_CHATS_.COUNT += 1
            except Exception as e:
                LOGS.warn(str(e))
@catub.cat_cmd(
    pattern="^(تشغيل|ايقاف) تخزين الخاص$",
    command=("(تشغيل|ايقاف) تخزين الخاص", plugin_category),
    info={
        "header": "لتشغيل او ايقاف تخزين رسائل الخاص في جروب التخزين.",
        "description": "اضبط PM_LOGGER_GROUP_ID في الڤارات لتعمل مع هذا",
        "usage": [
            "{tr}تشغيل تخزين الخاص",
            "{tr}ايقاف تخزين الخاص",
        ],
    },
)
async def set_pmlog(event):
    "لتشغـيل او ايقـاف تخـزين رسائل الـخاص"
    input_str = event.pattern_match.group(1)
    if input_str == "ايقاف":
        h_type = False
    elif input_str == "تشغيل":
        h_type = True
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        PMLOG = False
    else:
        PMLOG = True
    if PMLOG:
        if h_type:
            await event.edit("**⌔︙  تـخزين رسـائل الخـاص بالفـعل مُمكـنة ✅**")
        else:
            addgvar("PMLOG", h_type)
            await event.edit("**⌔︙  تـم تعـطيل تخـزين رسائل الـخاص بنـجاح ✅**")
    elif h_type:
        addgvar("PMLOG", h_type)
        await event.edit("**⌔︙  تـم تفعيل تخـزين رسائل الـخاص بنـجاح ✅**")
    else:
        await event.edit("**⌔︙  تـخزين رسـائل الخـاص بالفـعل معـطلة ✅**")


@catub.cat_cmd(
    pattern="^(تشغيل|ايقاف) تخزين الجروبات$",
    command=("(تشغيل|ايقاف) تخزين الجروبات", plugin_category),
    info={
        "header": "لتشغيل او ايقاف تخزين رسايل الجروبات في جروب التخزين.",
        "description": "اضبط PM_LOGGER_GROUP_ID في الڤارات لتعمل",
        "usage": [
            "{tr}تشغيل تخزين الجروبات",
            "{tr}ايقاف تخزين الجروبات",
        ],
    },
)
async def set_grplog(event):
    "لتشغـيل او ايقـاف تخـزين رسائل الجروبات"
    input_str = event.pattern_match.group(1)
    if input_str == "ايقاف":
        h_type = False
    elif input_str == "تشغيل":
        h_type = True
    if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") == "false":
        GRPLOG = False
    else:
        GRPLOG = True
    if GRPLOG:
        if h_type:
            await event.edit("**⌔︙  تـخزين رسـائل الجروبات بالفـعل مُمكـنة ✅**")
        else:
            addgvar("GRPLOG", h_type)
            await event.edit("**⌔︙  تـم تعـطيل تخـزين رسائل الجروبات بنـجاح ✅**")
    elif h_type:
        addgvar("GRPLOG", h_type)
        await event.edit("**⌔︙  تـم تفعيل تخـزين رسائل الجروبات بنـجاح ✅**")
    else:
        await event.edit("**⌔︙  تـخزين رسـائل الجروبات بالفـعل معـطلة ✅**")
