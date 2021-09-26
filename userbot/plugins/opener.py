#### Aslam

import asyncio
import os
import time

opn = []

@bot.on(admin_cmd(pattern="^open"))
@bot.on(sudo_cmd(pattern="^open", allow_sudo=True))
async def _(event):
    xx = await edit_or_reply(event, "...")
    if not event.reply_to_msg_id:
        return await edit_or_reply(xx, "Reply to a readable file coded by @Aslam_the_pro_coder", time=10)
    a = await event.get_reply_message()
    if not a.media:
        return await edit_or_reply(xx, "Reply to a readable file coded by @Aslam_the_pro_coder", time=10)
    b = await a.download_media()
    with open(b, "r") as c:
        d = c.read()
    n = 4096
    for bkl in range(0, len(d), n):
        opn.append(d[bkl : bkl + n])
    for bc in opn:
        await event.client.send_message(
            event.chat_id,
            f"{bc}\n\n**Coded by:** @Aslam_the_pro_coder",
            reply_to=event.reply_to_msg_id,
        )
    await event.delete()
    opn.clear()
    os.remove(b)
    await xx.delete()

CMD_HELP.update(
    {
        "Plugin": "Open\nCommand : .open\nFunction : /n<reply to a file>\nUse - Read contents of file and send as a telegram message.\n coded by @Aslam_the_pro_coder"
    }
)
