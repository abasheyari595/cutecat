#======================================================================================================================================

import asyncio, os
from datetime import datetime

from ..core.managers import edit_or_reply
from . import catub, hmention, reply_id
"""
try:
    from . import PING_PIC, PING_TEXT
except:
    pass
"""
PING_PIC = os.environ.get("PING_PIC")  or ("https://telegra.ph/file/403ad5dd2e7707e53c0e8.jpg")
PING_TEXT = os.environ.get("CUSTOM_PING_TEXT", None) or "ɪ ꜱʟᴀʏ ᴅʀᴀɢᴏɴꜱ ᴀᴛ ɴɪɢʜᴛ ᴡʜɪʟᴇ ʏᴏᴜ ꜱʟᴇᴇᴘ 🖤🥀"

plugin_category = "tools"

@catub.cat_cmd(
    pattern="^ping( -a|$)",
    command=("ping", plugin_category),
    info={
        "header": "check how long it takes to ping your userbot",
        "flags": {"-a": "average ping"},
        "usage": ["{tr}ping", "{tr}ping -a"],
    },
)
async def _(event):
    "To check ping"
    flag = event.pattern_match.group(1)
    start = datetime.now()
    if flag == " -a":
        catevent = await edit_or_reply(event, "`!....`")
        await asyncio.sleep(0.3)
        await catevent.edit("`..!..`")
        await asyncio.sleep(0.3)
        await catevent.edit("`....!`")
        end = datetime.now()
        tms = (end - start).microseconds / 1000
        ms = round((tms - 0.6) / 3, 3)
        await catevent.edit(f"**☞ ╰•★★  ℘ơŋɠ ★★•╯**\n➥ {ms} ms")
    else:
        catevent = await edit_or_reply(event, "<b><i>☞ •★★  ℘ơŋɠ ★★•</b></i>", "html")
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        await catevent.edit(
            f"╰•★★ ℘ơŋɠ ★★•╯\n\n    ⚘ {ms}\n    ⚘ Oɯɳҽɾ : {hmention}",
            parse_mode="html",
        )       

#pping -> edited ping with pic

@catub.cat_cmd(
    pattern="^pping$",
    command=("pping", plugin_category),
    info={
        "header": "check how long it takes to ping your userbot.",
        "option": "To show media in this cmd you need to set PING_PIC with media link, get this by replying the media by .tgm",
        "usage": ["{tr}pping", ],
    },
)
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(event)
    start = datetime.now()
    cat = await edit_or_reply(event, "<b><i>  ❤️⃝⃝⃝⃝⃝⃝⃝⃝⃝⃝⃝⃝⃝⃝⃟✨ ᑭｉｎｇｉｎｇ... 🍀⃝⃝⃟🍂 </b></i>", "html")
    end = datetime.now()
    await cat.delete()
    ms = (end - start).microseconds / 1000
    if PING_PIC:
        caption = f"<b><i>{PING_TEXT}<i><b>\n\n<code>╭         ─┉─ • ─┉─         ╮\n┃ 🍀⃝⃝⃟🍂 ℘ơŋɠ ☞ {ms}\n┃ ❤️⃝⃝⃝⃝⃝⃝⃝⃝⃝⃝⃝⃝⃝⃝⃟✨ Oɯɳҽɾ ☞ <b>{hmention}</b>\n╰        ─┉─¡! • !¡─┉─       ╯"
        await event.client.send_file(
            event.chat_id,
            PING_PIC,
            caption=caption,
            parse_mode="html",
            reply_to=reply_to_id,
            link_preview=False,
            allow_cache=True,
        )
    else:
        await event.edit_or_reply(event, "<code>Add PING_PIC first nubh.<code>", "html")

#====================================================================================================================================== 
