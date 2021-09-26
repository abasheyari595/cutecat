from asyncio import sleep

from googletrans import LANGUAGES, Translator

# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID, deEmojify

plugin_category = "utils"


async def getTranslate(text, **kwargs):
    translator = Translator()
    result = None
    for _ in range(10):
        try:
            result = translator.translate(text, **kwargs)
        except Exception:
            translator = Translator()
            await sleep(0.1)
    return result


@catub.cat_cmd(
    pattern="^ترجمه ([\s\S]*)",
    command=("ترجمه", plugin_category),
    info={
        "header": "لترجمة النص إلى اللغة المطلوبة.",
        "note": "لاكواد اللغه راجع [هذا اللينك](https://bit.ly/2SRQ6WU)",
        "usage": [
            "{tr}ترجمه <كود اللغه> ; <النص>",
            "{tr}ترجمه <كود اللغه>",
        ],
        "examples": "{tr}ترجمه  + ar ; cat is one of the popular bot",
    },
)
async def _(event):
    "لترجمة النص."
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "en"
    elif ";" in input_str:
        lan, text = input_str.split(";")
    else:
        return await edit_delete(
            event, "**⌔︙ للترجمه يجـب الـرد على الرساله واكتب .ترجمه ar**", time=5
        )
    text = deEmojify(text.strip())
    lan = lan.strip()
    Translator()
    try:
        translated = await getTranslate(text, dest=lan)
        after_tr_text = translated.text
        output_str = f"**⌔︙ تمت الترجمه مـن  :** {LANGUAGES[translated.src].title()}\n **⌔︙ الـى ** {LANGUAGES[lan].title()} \
                \n\n{after_tr_text}"
        await edit_or_reply(event, output_str)
    except Exception as exc:
        await edit_delete(event, f"**خـطأ:**\n`{str(exc)}`", time=5)


@catub.cat_cmd(
    pattern="^ترجم(?: |$)([\s\S]*)",
    command=("ترجم", plugin_category),
    info={
        "header": "لترجمة النص إلى اللغة المطلوبة.",
        "note": "لهذا قم بعمل ضبط ترجم وكود اللغه.",
        "usage": [
            "{tr}ترجم",
            "{tr}ترجم <النص>",
        ],
    },
)
async def translateme(trans):
    "لترجمة النص إلى اللغة المطلوب."
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await edit_or_reply(
            trans, "`إعطاء نص أو الرد على رسالة للترجمة!`"
        )
    TRT_LANG = gvarstatus("TRT_LANG") or "en"
    try:
        reply_text = await getTranslate(deEmojify(message), dest=TRT_LANG)
    except ValueError:
        return await edit_delete(trans, "`Invalid destination language.`", time=5)
    source_lan = LANGUAGES[f"{reply_text.src.lower()}"]
    transl_lan = LANGUAGES[f"{reply_text.dest.lower()}"]
    reply_text = f"**من {source_lan.title()}({reply_text.src.lower()}) إلي {transl_lan.title()}({reply_text.dest.lower()}) :**\n`{reply_text.text}`"

    await edit_or_reply(trans, reply_text)
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"`Translated some {source_lan.title()} stuff to {transl_lan.title()} just now.`",
        )


@catub.cat_cmd(
    pattern="^ضبط (شات البوت|ترجم) ([\s\S]*)",
    command=("ضبط", plugin_category),
    info={
        "header": "لضبط اللغه للمترجم وشات البوت.",
        "description": "اضغط هنا [لاكواد اللغه](https://bit.ly/2SRQ6WU)",
        "options": {
            "ترجم": "لغة المترجم الاصليه",
            "شات بوت": "اللغه الاصليه لشات البوت(شات البوت)",
        },
        "usage": "{tr}ضبط option <language codes>",
        "examples": [
            "{tr}ضبط ترجم ar",
            "{tr}ضبط شات البوت ar",
        ],
    },
)
async def lang(value):
    "لضبط اللغه للمترجم وشات البوت."
    arg = value.pattern_match.group(2).lower()
    input_str = value.pattern_match.group(1)
    if arg not in LANGUAGES:
        return await edit_or_reply(
            value,
            f"`كود اللغه غير صالح ❗️`\n`اكواد اللغه المتاحه للمترجم`:\n\n`{LANGUAGES}`",
        )
    LANG = LANGUAGES[arg]
    if input_str == "ترجم":
        addgvar("TRT_LANG", arg)
        await edit_or_reply(
            value, f"`⌔︙ تغيرت لغة المترجم إلى {LANG.title()}.`"
        )
    else:
        addgvar("AI_LANG", arg)
        await edit_or_reply(
            value, f"`⌔︙ تم تغيير لغة شات البوت إلى {LANG.title()}.`"
        )
    LANG = LANGUAGES[arg]

    if BOTLOG:
        if input_str == "ترجم":
            await value.client.send_message(
                BOTLOG_CHATID, f"`⌔︙ تغيرت لغة المترجم إلى {LANG.title()}.`"
            )
        if input_str == "شات البوت":
            await value.client.send_message(
                BOTLOG_CHATID, f"`⌔︙ تم تغيير لغة شات البوت إلى {LANG.title()}.`"
            )