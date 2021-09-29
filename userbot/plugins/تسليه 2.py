# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import asyncio
from collections import deque

from . import catub, edit_or_reply

plugin_category = "fun"


@catub.cat_cmd(
    pattern="^افكر$",
    command=("افكر", plugin_category),
    info={
        "الامر": "امر تسليه جربه بنفسك",
        "الاستخدام": "{tr}افكر",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "^افكر")
    deq = deque(list("🤔🧐🤔🧐🤔🧐"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="^ضحك$",
    command=("ضحك", plugin_category),
    info={
        "الامر": "امر تسليه جربه بنفسك",
        "الاستخدام": "{tr}ضحك",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "^ضحك")
    deq = deque(list("😹🤣😂😹🤣😂"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="^ضايج$",
    command=("ضايج", plugin_category),
    info={
        "الامر": "امر تسليه جربه بنفسك",
        "الاستخدام": "{tr}ضايج",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "^ضايج")
    deq = deque(list("😕😞🙁☹️😕😞🙁"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="^وقت$",
    command=("وقت", plugin_category),
    info={
        "الامر": "امر تسليه جربه بنفسك",
        "الاستخدام": "{tr}وقت",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "وقت^")
    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="^بوسه$",
    command=("بوسه", plugin_category),
    info={
        "الامر": "امر تسليه جربه بنفسك",
        "الاستخدام": "{tr}بوسه",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "^بوسه")
    deq = deque(list("😗😙😚😚😘"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="^قلوب$",
    command=("قلوب", plugin_category),
    info={
        "الامر": "امر تسليه جربه بنفسك",
        "الاستخدام": "{tr}قلوب",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "^قلوب")
    deq = deque(list("❤️🧡💛💚💙💜🖤"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="^جيم$",
    command=("جيم", plugin_category),
    info={
        "الامر": "امر تسليه جربه بنفسك",
        "الاستخدام": "{tr}جيم",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "^جيم")
    deq = deque(list("🏃‍🏋‍🤸‍🏃‍🏋‍🤸‍🏃‍🏋‍🤸‍"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="^الارض$",
    command=("الارض", plugin_category),
    info={
        "الامر": "امر تسليه جربه بنفسك",
        "الاستخدام": "{tr}الارض",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "^الارض")
    deq = deque(list("🌏🌍🌎🌎🌍🌏🌍🌎"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="^قمر$",
    command=("قمر", plugin_category),
    info={
        "الامر": "امر تسليه جربه بنفسك",
        "الاستخدام": "{tr}قمر",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "^قمر")
    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="^اقمار$",
    command=("اقمار", plugin_category),
    info={
        "الامر": "امر تسليه جربه بنفسك",
        "الاستخدام": "{tr}اقمار",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "^اقمار")
    animation_interval = 0.2
    animation_ttl = range(101)
    await event.edit("اقمار..")
    animation_chars = [
        "🌗🌗🌗🌗🌗\n🌓🌓🌓🌓🌓\n🌗🌗🌗🌗🌗\n🌓🌓🌓🌓🌓\n🌗🌗🌗🌗🌗",
        "🌘🌘🌘🌘🌘\n🌔🌔🌔🌔🌔\n🌘🌘🌘🌘🌘\n🌔🌔🌔🌔🌔\n🌘🌘🌘🌘🌘",
        "🌑🌑🌑🌑🌑\n🌕🌕🌕🌕🌕\n🌑🌑🌑🌑🌑\n🌕🌕🌕🌕🌕\n🌑🌑🌑🌑🌑",
        "🌒🌒🌒🌒🌒\n🌖🌖🌖🌖🌖\n🌒🌒🌒🌒🌒\n🌖🌖🌖🌖🌖\n🌒🌒🌒🌒🌒",
        "🌓🌓🌓🌓🌓\n🌗🌗🌗🌗🌗\n🌓🌓🌓🌓🌓\n🌗🌗🌗🌗🌗\n🌓🌓🌓🌓🌓",
        "🌔🌔🌔🌔🌔\n🌘🌘🌘🌘🌘\n🌔🌔🌔🌔🌔\n🌘🌘🌘🌘🌘\n🌔🌔🌔🌔🌔",
        "🌕🌕🌕🌕🌕\n🌑🌑🌑🌑🌑\n🌕🌕🌕🌕🌕\n🌑🌑🌑🌑🌑\n🌕🌕🌕🌕🌕",
        "🌖🌖🌖🌖🌖\n🌒🌒🌒🌒🌒\n🌖🌖🌖🌖🌖\n🌒🌒🌒🌒🌒\n🌖🌖🌖🌖🌖",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 8])


@catub.cat_cmd(
    pattern="^قمور$",
    command=("قمور", plugin_category),
    info={
        "الامر": "امر تسليه جربه بنفسك",
        "الاستخدام": "{tr}قمور",
    },
)
async def _(event):
    "أمر الرسوم المتحركة"
    event = await edit_or_reply(event, "^قمور")
    animation_interval = 0.2
    animation_ttl = range(96)
    await event.edit("قمور..")
    animation_chars = [
        "🌗",
        "🌘",
        "🌑",
        "🌒",
        "🌓",
        "🌔",
        "🌕",
        "🌖",
        "🌗",
        "🌘",
        "🌑",
        "🌒",
        "🌓",
        "🌔",
        "🌕",
        "🌖",
        "🌗",
        "🌘",
        "🌑",
        "🌒",
        "🌓",
        "🌔",
        "🌕",
        "🌖",
        "🌗",
        "🌘",
        "🌑",
        "🌒",
        "🌓",
        "🌔",
        "🌕",
        "🌖",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 32])
