# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import asyncio

from . import catub, edit_or_reply

plugin_category = "fun"


@catub.cat_cmd(
    pattern="^تحميلات$",
    command=("تحميلات", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "انيم": "{tr}تحميلات",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.3
    animation_ttl = range(20)
    event = await edit_or_reply(event, "▯")
    animation_chars = ["▮", "▯", "▬", "▭", "‎"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])


@catub.cat_cmd(
    pattern="^اشكال مربع$",
    command=("اشكال مربع", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}اشكال مربع",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.3
    animation_ttl = range(20)
    event = await edit_or_reply(event, "◨")
    animation_chars = ["◧", "◨", "◧", "◨", "‎"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])


@catub.cat_cmd(
    pattern="^up$",
    command=("up", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}up",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.3
    animation_ttl = range(20)
    event = await edit_or_reply(event, "╻")
    animation_chars = ["╹", "╻", "╹", "╻", "‎"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])


@catub.cat_cmd(
    pattern="^دائره$",
    command=("دائره", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}دائره",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.3
    animation_ttl = range(20)
    event = await edit_or_reply(event, "دائره...")
    animation_chars = ["⚫", "⬤", "●", "∘", "‎"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])


@catub.cat_cmd(
    pattern="^قلب$",
    command=("قلب", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}قلب",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.5
    animation_ttl = range(20)
    event = await edit_or_reply(event, "❤️")
    animation_chars = ["🖤", "❤️", "🖤", "❤️", "‎"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])


@catub.cat_cmd(
    pattern="^مزاج$",
    command=("مزاج", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}مزاج",
    },
)
async def _(event):
    "animation command"
    animation_interval = 1
    animation_ttl = range(20)
    event = await edit_or_reply(event, "مزاج")
    animation_chars = [
        "😁",
        "😧",
        "😡",
        "😢",
        "😁",
        "😧",
        "😡",
        "😢",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 10])


@catub.cat_cmd(
    pattern="^قرد$",
    command=("قرد", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}قرد",
    },
)
async def _(event):
    "animation command"
    animation_interval = 2
    animation_ttl = range(12)
    event = await edit_or_reply(event, "قروده....")
    animation_chars = [
        "🐵",
        "🙉",
        "🙈",
        "🙊",
        "🐵",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 6])



@catub.cat_cmd(
    pattern="^يد$",
    command=("يد", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}يد",
    },
)
async def _(event):
    "animation command"
    animation_interval = 1
    animation_ttl = range(13)
    event = await edit_or_reply(event, "🖐️")
    animation_chars = [
        "👈",
        "👉",
        "☝️",
        "👆",
        "🖕",
        "👇",
        "✌️",
        "🤞",
        "🖖",
        "🤘",
        "🤙",
        "🖐️",
        "👌",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 13])


@catub.cat_cmd(
    pattern="^العد التنازلي$",
    command=("العد التنازلي", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}العد التنازلي",
    },
)
async def _(event):
    "animation command"
    animation_interval = 1
    animation_ttl = range(12)
    event = await edit_or_reply(event, "العد التنازلي....")
    animation_chars = [
        "🔟",
        "9️⃣",
        "8️⃣",
        "7️⃣",
        "6️⃣",
        "5️⃣",
        "4️⃣",
        "3️⃣",
        "2️⃣",
        "1️⃣",
        "0️⃣",
        "🆘",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 12])


@catub.cat_cmd(
    pattern="^الوان قلوب$",
    command=("الوان قلوب", plugin_category),
    info={
        "الامر": "**امر تسليه قم بالتجربه بنفسك**",
        "الاستخدام": "{tr}الوان قلوب",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.3
    animation_ttl = range(54)
    event = await edit_or_reply(event, "🖤")
    animation_chars = [
        "❤️",
        "🧡",
        "💛",
        "💚",
        "💙",
        "💜",
        "🖤",
        "💘",
        "💝",
        "❤️",
        "🧡",
        "💛",
        "💚",
        "💙",
        "💜",
        "🖤",
        "💘",
        "💝",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 18])
