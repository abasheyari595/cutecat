# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import asyncio

from userbot import catub

from ..core.managers import edit_or_reply
from ..helpers.utils import _format
from . import ALIVE_NAME

plugin_category = "fun"


@catub.cat_cmd(
    pattern="^تهكير$",
    command=("تهكير", plugin_category),
    info={
        "header": "امر الرسوم المتحركه مضحك.",
        "description": "الرد على المستخدم لإظهار رسوم متحركه تهكير",
        "note": "هذا للتسلية فقط. ليس تهكير حقيقي.",
        "usage": "{tr}تهكير",
    },
)
async def _(event):
    "امر الرسوم المتحركه مضحك."
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        idd = reply_message.sender_id
        if idd == 1959178200:
            await edit_or_reply(
                event, "**⌔︙ عـذرا أنـة مبـرمج السـورس لايـمكن تهكيـرة. ⚜️**"
            )
        else:
            event = await edit_or_reply(event, "**⌔︙ جـاري التـهكير ⚠️**")
            animation_chars = [
                "**⌔︙ جـاري الاتصـال بجهـاز الضحـية لأختـراقـة  📳**",
                "**⌔︙ أختـراق جهـاز الضحـية الهـددف محـدد جـاري أختـراقـة ㊙️**",
                "**⌔︙ تحـميل الاخـتراق  ㊙️ .. 0%**\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**⌔︙ تحـميل الاخـتراق  ㊙️ .. 4%**\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**⌔︙ تحـميل الاخـتراق  ㊙️ ..10%**\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**⌔︙ تحـميل الاخـتراق  ㊙️ .. 20%**\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**⌔︙ تحـميل الاخـتراق  ㊙️ .. 36%**\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**⌔︙ تحـميل الاخـتراق  ㊙️ .. 52%**\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**⌔︙ تحـميل الاخـتراق  ㊙️ .. 84%**\n█████████████████████▒▒▒▒ ",
                "**⌔︙ تحـميل الاخـتراق  ㊙️ .. 100%**\n████████████████████████",
                f"**⌔︙ تـم اخـتراق الضحـية 🆘 الفـديـة لالغاء الاخـتراق يرجي اعطاء 9999🍕 لـ السيـد `{ALIVE_NAME}` . بـدون تنـازل**",
            ]
            animation_interval = 3
            animation_ttl = range(11)
            for i in animation_ttl:
                await asyncio.sleep(animation_interval)
                await event.edit(animation_chars[i % 11])
    else:
        await edit_or_reply(
            event,
            "**⌔︙ لم يتم تعريف أي مستخدم قم برد على الضحية**",
            parse_mode=_format.parse_pre,
        )
