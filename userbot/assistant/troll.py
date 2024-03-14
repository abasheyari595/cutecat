import json
import os
import re

from telethon.events import CallbackQuery

from userbot import catub


@catub.tgbot.on(CallbackQuery(data=re.compile(b"troll_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    if os.path.exists("./userbot/troll.txt"):
        jsondata = json.load(open("./userbot/troll.txt"))
        try:
            message = jsondata[f"{timestamp}"]
            userid = message["userid"]
            ids = [userid]
            if event.query.user_id in ids:
                reply_pop_up_alert = (
                    "لا يسمح لك برؤية هذه الرسالة، حظاً موفقاً في المرة القادمة!"
                )
            else:
                encrypted_tcxt = message["text"]
                reply_pop_up_alert = encrypted_tcxt
        except KeyError:
            reply_pop_up_alert = "هذه الرسالة لم تعد موجودة في خادم كات"
    else:
        reply_pop_up_alert = "هذه الرسالة لم تعد موجودة "
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
