# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

from telethon import functions

from userbot import catub

from ..Config import Config
from ..core import CMD_INFO, GRP_INFO, PLG_INFO
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

cmdprefix = Config.COMMAND_HAND_LER

plugin_category = "tools"

hemojis = {
    "admin": "👮‍♂️",
    "bot": "🤖",
    "fun": "🎨",
    "misc": "🧩",
    "tools": "🧰",
    "utils": "🗂",
    "extra": "➕",
}


def get_key(val):
    for key, value in PLG_INFO.items():
        for cmd in value:
            if val == cmd:
                return key
    return None


def getkey(val):
    for key, value in GRP_INFO.items():
        for plugin in value:
            if val == plugin:
                return key
    return None


async def cmdinfo(input_str, event, plugin=False):
    if input_str[0] == cmdprefix:
        input_str = input_str[1:]
    try:
        about = CMD_INFO[input_str]
    except KeyError:
        if plugin:
            await edit_delete(
                event,
                f"**⌔︙ لا يـوجد مكـون إضـافـي أو أمـر مثـل **`{input_str}`** فـي كات بالعربي .**",
            )
            return None
        await edit_delete(
            event, f"**⌔︙ لا يـوجـد أمـر مثـل **`{input_str}`**في كات بالعربي .**"
        )
        return None
    except Exception as e:
        await edit_delete(event, f"**⌔︙ هنـاك خطـأ**\n`{str(e)}`")
        return None
    outstr = f"**⌔︙ الأمر :** `{cmdprefix}{input_str}`\n"
    plugin = get_key(input_str)
    if plugin is not None:
        outstr += f"**⌔︙ عـدد الاضافات :** `{plugin}`\n"
        category = getkey(plugin)
        if category is not None:
            outstr += f"**⌔︙ الفـئـة :** `{category}`\n\n"
    outstr += f"**⌔︙ الـمقدمـة :**\n{about[0]}"
    return outstr


async def plugininfo(input_str, event, flag):
    try:
        cmds = PLG_INFO[input_str]
    except KeyError:
        outstr = await cmdinfo(input_str, event, plugin=True)
        return outstr
    except Exception as e:
        await edit_delete(event, f"**⌔︙ هنـاك خطـأ**\n`{str(e)}`")
        return None
    if len(cmds) == 1 and (flag is None or (flag and flag != "الاضافه")):
        outstr = await cmdinfo(cmds[0], event, plugin=False)
        return outstr
    outstr = f"**⌔︙ عـدد الاضافات : **`{input_str}`\n"
    outstr += f"**⌔︙ الأوامـر المتوفـرة :** `{len(cmds)}`\n"
    category = getkey(input_str)
    if category is not None:
        outstr += f"**⌔︙ الفـئة :** `{category}`\n\n"
    for cmd in cmds:
        outstr += f"⌔︙  **الأمـر :** `{cmdprefix}{cmd}`\n"
        try:
            outstr += f"⌔︙  **يقـوم بـ :** `{CMD_INFO[cmd][1]}`\n\n"
        except IndexError:
            outstr += f"⌔︙  **يقـوم بـ :** `لا شـيئ مكـتـوب`\n\n"
    outstr += f"**⌔︙ الاستـعـمال : ** {cmdprefix}مساعده + اسم الامـر\
        \n**⌔︙ ملاحـضـه عـزيـزي : **إذا كـان اسـم الأمـر هـو نـفسه اسـم البرنامج المساعد ، فاستـخدم هـذا الاسـم {cmdprefix}مساعده الامر <اسم الامـر او الاضافه>`."
    return outstr


async def grpinfo():
    outstr = "**⌔︙ الاضافات في كات بالعربي  :**\n\n"
    outstr += f"**⌔︙ الاستعمال : ** `{cmdprefix}مساعده <اسم الاضافه او الامر>`\n\n"
    category = ["admin", "bot", "fun", "misc", "tools", "utils", "extra"]
    for cat in category:
        plugins = GRP_INFO[cat]
        outstr += f"**{hemojis[cat]} {cat.title()} **({len(plugins)})\n"
        for plugin in plugins:
            outstr += f"`{plugin}`  "
        outstr += "\n\n"
    return outstr


async def cmdlist():
    outstr = "**⌔︙ القائمة الإجمالية للأوامر في كات بالعربي :**\n\n"
    category = ["admin", "bot", "fun", "misc", "tools", "utils", "extra"]
    for cat in category:
        plugins = GRP_INFO[cat]
        outstr += f"**{hemojis[cat]} {cat.title()} ** - {len(plugins)}\n\n"
        for plugin in plugins:
            cmds = PLG_INFO[plugin]
            outstr += f"• **{plugin.title()} يمتلك {len(cmds)} الاوامر**\n"
            for cmd in cmds:
                outstr += f"  - `{cmdprefix}{cmd}`\n"
            outstr += "\n"
    outstr += f"**⌔︙ الاستعمال : ** `{cmdprefix}مساعده الامر <اسم الامر>`"
    return outstr


@catub.cat_cmd(
    pattern="^مساعده ?(الامر|الاضافه|الاضافات)? ?([\s\S]*)?",
    command=("مساعده", plugin_category),
    info={
        "header": "للحصول على دليل لاستخدام البوت.",
        "description": "للحصول علي تعليمات حول امر او اضافه",
        "note": "لو الامر والاضافه نفس الاسم سوف تحصل علي تعليمات حول الاضافه لذلك باستخدام هذه العلم تحصل على دليل الاوامر",
        "العلم": {
            "الامر": "لجلب معلومات عن الامر.",
            "الاضافه": "لجلب معلومات عن الاضافه.",
            "جميع الاضافات": "للحصول علي جميع الاضافات في نص.",
        },
        "usage": [
            "مساعده (الاضافه/اسم الامر)",
            "مساعده الامر (اسم الامر)",
        ],
        "examples": ["مساعده مساعده", "مساعده الامر مساعده"],
    },
)
async def _(event):
    "للحصول على دليل لاستخدام البوت."
    flag = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    if flag and flag == "الامر" and input_str:
        outstr = await cmdinfo(input_str, event)
        if outstr is None:
            return
    elif input_str:
        outstr = await plugininfo(input_str, event, flag)
        if outstr is None:
            return
    else:
        if flag == "الاضافات":
            outstr = await grpinfo()
        else:
            results = await event.client.inline_query(Config.TG_BOT_USERNAME, "مساعده")
            await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
            await event.delete()
            return
    await edit_or_reply(event, outstr)


@catub.cat_cmd(
    pattern="^جميع الاوامر(?:\s|$)([\s\S]*)",
    command=("جميع الاوامر", plugin_category),
    info={
        "header": "لإظهار قائمة الاوامر.",
        "description": "إذا لم يتم تقديم أي إدخال ، فسيتم عرض قائمة بجميع الأوامر.",
        "usage": [
            "جميع الاوامر لاظهار كل الاوامر",
            "جميع الاوامر + اسم الامر لاضافه معينه",
        ],
    },
)
async def _(event):
    "لإظهار قائمة الاوامر."
    input_str = event.pattern_match.group(1)
    if not input_str:
        outstr = await cmdlist()
    else:
        try:
            cmds = PLG_INFO[input_str]
        except KeyError:
            return await edit_delete(event, "**⌔︙ اسم البرنامج المساعد غير صالح أعد التحقق منه**")
        except Exception as e:
            return await edit_delete(event, f"**⌔︙ هناك خطا**\n`{str(e)}`")
        outstr = f"• **{input_str.title()} يمتلك {len(cmds)} اوامر"
        for cmd in cmds:
            outstr += f"  - `{cmdprefix}{cmd}`\n"
        outstr += f"**⌔︙ الاستعمال : ** `{cmdprefix}< مساعده < الامر > < اسم الامر.`"
    await edit_or_reply(
        event, outstr, aslink=True, linktext="**⌔︙ جميع الاوامر في كات بالعربي 👈** :"
    )

@catub.cat_cmd(
    pattern="^بحث عن امر ([\s\S]*)",
    command=("بحث عن امر", plugin_category),
    info={
        "header": "للبحث عن الاوامر.",
        "examples": "بحث عن امر الاغاني",
    },
)
async def _(event):
    "للبحث عن الاوامر."
    cmd = event.pattern_match.group(1)
    found = [i for i in sorted(list(CMD_INFO)) if cmd in i]
    if found:
        out_str = "".join(f"`{i}`    " for i in found)
        out = f"**وجدت {len(found)} command(s) for: **`{cmd}`\n\n{out_str}"
        out += f"\n\n__لمزيد من المعلومات افحص {cmdprefix}< مساعده < الامر > < اسم الامر."
    else:
        out = f"لا يمكنني العثور على أي أمر من هذا القبيل `{cmd}` في كات بالعربي "
    await edit_or_reply(event, out)