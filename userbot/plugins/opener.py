#by @YVW_6

import asyncio
import os
import time

opn = []

@bot.on(admin_cmd(pattern="open"))
@bot.on(sudo_cmd(pattern="open", allow_sudo=True))
async def _(event):
    xx = await edit_or_reply(event, "`Loading ...`")
    if not event.reply_to_msg_id:
        return await edit_or_reply(xx, "Reply to a readable file", time=10)
    a = await event.get_reply_message()
    if not a.media:
        return await edit_or_reply(xx, "Reply to a readable file", time=10)
    b = await a.download_media()
    with open(b, "r") as c:
        d = c.read()
    n = 4096
    for bkl in range(0, len(d), n):
        opn.append(d[bkl : bkl + n])
    for bc in opn:
        await event.client.send_message(
            event.chat_id,
            f"`{bc}`",
            reply_to=event.reply_to_msg_id,
        )
    await event.delete()
    opn.clear()
    os.remove(b)
    await xx.delete()

CMD_HELP.update(
    {
        "opener": "__**PLUGIN NAME :** Opener__\
    \n\n📌** CMD ➥** `.open`\
    \n**USAGE   ➥  **Read contents of file and send as a telegram message\
    \n\nCoded By @YVW_6\
     "
    }
)
