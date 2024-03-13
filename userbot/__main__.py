import sys

import userbot
from userbot import BOTLOG_CHATID, HEROKU_APP, PM_LOGGER_GROUP_ID

from .Config import Config
from .core.logger import logging
from .core.session import catub
from .utils import (
    add_bot_to_logger_group,
    ipchange,
    load_plugins,
    setup_bot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("كات بالعربي")

print(userbot.__copyright__)
print("مرخصة بموجب شروط " + userbot.__license__)

cmdhr = Config.COMMAND_HAND_LER

try:
    LOGS.info("يتم بدء البوت المساعد")
    catub.loop.run_until_complete(setup_bot())
    LOGS.info("اكتملت عمليه تشغيل البوت المساعد ✅")
except Exception as e:
    LOGS.error(f"{e}")
    sys.exit()


class CatCheck:
    def __init__(self):
        self.sucess = True


Catcheck = CatCheck()


async def startup_process():
    check = await ipchange()
    if check is not None:
        Catcheck.sucess = False
        return
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    print("البوت المساعد الخاص بك يعمل بنجاح ✅.!!!")
    print(
        f"تهانيا اكتب الآن `alive` للتأكد من انه يعمل بشكل طبيعي 🔥\
        \nاذا كنت بحاجه للمساعده, تواصل معي https://t.me/x0ceo"
    )
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    Catcheck.sucess = True
    return


catub.loop.run_until_complete(startup_process())


if len(sys.argv) not in (1, 3, 4):
    catub.disconnect()
elif not Catcheck.sucess:
    if HEROKU_APP is not None:
        HEROKU_APP.restart()
else:
    try:
        catub.run_until_disconnected()
    except ConnectionError:
        pass
