# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @h3ppp

import asyncio
import os
import random
from urllib.parse import quote_plus

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.google_tools import chromeDriver
from . import catub, deEmojify

plugin_category = "utils"

carbon_language = "auto"


def download_carbon(driver, url):
    driver.get(url)
    download_path = "./"
    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": download_path},
    }
    driver.execute("send_command", params)

    driver.find_element("xpath", "//button[contains(text(),'Export')]").click()


@catub.cat_cmd(
    pattern="^كربون(?:\s|$)([\s\S]*)",
    command=("كربون", plugin_category),
    info={
        "header": "مولدات الكربون لنص معين (نمط ثابت)",
        "usage": [
            "{tr}كربون <text>",
            "{tr}كربون <reply to text>",
        ],
    },
)
async def carbon_api(event):
    """A Wrapper for carbon.now.sh"""
    cat = await edit_or_reply(event, "`جاري المعالجه 🧪...`")
    carbon_url = "https://carbon.now.sh/?l={lang}&code={code}"

    query = event.pattern_match.group(1)
    replied_msg = await event.get_reply_message()
    if not query and replied_msg:
        query = replied_msg.message
    if not query:
        return await edit_delete(cat, "لم يتم إعطاء أي نص")

    code = quote_plus(deEmojify(query))
    cat = await edit_or_reply(event, "`جاري عمل الكربون...\n25%`")
    url = carbon_url.format(code=code, lang=carbon_language)
    driver, driver_message = chromeDriver.start_driver()
    if driver is None:
        return await edit_delete(event, driver_message)
    driver.get(url)
    await edit_or_reply(cat, "`انتظر من فضلك...\n50%`")
    download_carbon(driver, url)

    await edit_or_reply(cat, "`جاري..\n75%`")

    await asyncio.sleep(2)
    await edit_or_reply(cat, "`تم عمل الكربون بنجاح ✅...\n100%`")
    file = "./carbon.png"
    await edit_or_reply(cat, "`جاري الرفع 📎..`")
    await event.client.send_file(
        event.chat_id,
        file,
        caption="هاهو الكربون الخاص بك ✔️",
        force_document=True,
        reply_to=event.message.reply_to_msg_id,
    )
    os.remove("./carbon.png")
    driver.quit()
    await cat.delete()
