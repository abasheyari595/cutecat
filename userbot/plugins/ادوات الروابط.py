# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import requests
from validators.url import url

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "utils"


@catub.cat_cmd(
    pattern="^دنس(?:\s|$)([\s\S]*)",
    command=("دنس", plugin_category),
    info={
        "header": "للحصول على دومين (دنس) من الرابط المحدد.",
        "usage": "{tr}دنس <الرابط/بالرد>",
        "examples": "{tr}دنس google.com",
    },
)
async def _(event):
    "للحصول على دومين (دنس) من الرابط المحدد."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "⌔︙  يجـب عليم الرد على الرابط او وضع الرابط مع الام", 5
        )
    check = url(input_str)
    if not check:
        catstr = "http://" + input_str
        check = url(catstr)
    if not check:
        return await edit_delete(event, "⌔︙  هذا الرابط غير مدعوم", 5)
    sample_url = f"https://da.gd/dns/{input_str}"
    response_api = requests.get(sample_url).text
    if response_api:
        await edit_or_reply(event, f"الـ دي أن اس لـ {input_str} هي \n\n{response_api}")
    else:
        await edit_or_reply(
            event, f"⌔︙ - لم استطع ايجاد `{input_str}` في الانترنت"
        )

 
@catub.cat_cmd(
    pattern="^اختصار(?:\s|$)([\s\S]*)",
    command=("اختصار", plugin_category),
    info={
        "header": "اختصار رابط معين.",
        "usage": "{tr}اختصار <الرابط/بالرد>",
        "examples": "{tr}اختصار https://github.com/",
    },
)
async def _(event):
    "اختصار رابط معين"
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "⌔︙  يجـب عليم الرد على الرابط او وضع الرابط مع الامر", 5
        )
    check = url(input_str)
    if not check:
        catstr = f"http://" + input_str
        check = url(catstr)
    if not check:
        return await edit_delete(event, "⌔︙  هذا الرابط غير مدعوم", 5)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    sample_url = f"https://da.gd/s?url={input_str}"
    response_api = requests.get(sample_url).text
    if response_api:
        await edit_or_reply(
            event, f"⌔︙ تـم صنـع رابـط مصغر: {response_api}", link_preview=False
        )
    else:
        await edit_or_reply(event, "⌔︙  هـنالك شي خطـا حاول لاحقـا")
  
@catub.cat_cmd(
    pattern="^اخفاء(?:\s|$)([\s\S]*)",
    command=("اخفاء", plugin_category),
    info={
        "header": "لاخفاء الرابط مع مساحات بيضاء باستخدام هايبر لينك.",
        "usage": "{tr}اخفاء <الرابط/بالرد>",
        "examples": "{tr}اخفاء https://github.com/",
    },
)
async def _(event):
    "لاخفاء الرابط مع مساحات بيضاء باستخدام هايبر لينك."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "⌔︙  يجـب عليم الرد على الرابط او وضع الرابط مع الامر", 5
        )
    check = url(input_str)
    if not check:
        catstr = "http://" + input_str
        check = url(catstr)
    if not check:
        return await edit_delete(event, "⌔︙  هذا الرابط غير مدعوم", 5)
    await edit_or_reply(event, "[ㅤㅤㅤㅤㅤㅤㅤ](" + input_str + ")")
