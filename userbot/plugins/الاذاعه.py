# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @H3PPP

from userbot import bot
from userbot import CMD_HELP

GCAST_BLACKLIST = [
    -1001459701099,
    -1001198363638,
    ]
#

@bot.on(admin_cmd(pattern="^اذاعه للجروبات(?: |$)(.*)"))
async def gcast(event):
    venom = event.pattern_match.group(1)
    if venom:
        msg = venom
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        await eor(event, "**-يجب الرد على رساله او وسائط او كتابه النص مع الامر**")
        return
    sokker = await edit_or_reply(event, "`🔬 يتم الاذاعة في الجروبات انتظر لحظه...`")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                if chat not in GCAST_BLACKLIST:
                    await event.client.send_message(chat, msg)
                    done += 1
            except BaseException:
                er += 1
    await sokker.edit(
        f"**- تم بنجاح الأذاعة الى ** `{done}` **✅ من الدردشات ، خطأ في ارسال الى ** `{er}` **❌ من الدردشات**"
    )
    
@bot.on(admin_cmd(pattern="^اذاعه للخاص(?: |$)(.*)"))
async def gucast(event):
    venom = event.pattern_match.group(1)
    if venom:
        msg = venom
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        await eor(event, "**-يجب الرد على رسالة او وسائط او كتابه النص مع الامر**")
        return
    sokker = await edit_or_reply(event, "`🔬 يتم الاذاعة في الخاص انتظر لحظه...`")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await event.client.send_message(chat, msg)
            except BaseException:
                er += 1
    await sokker.edit(
        f"**- تم بنجاح الأذاعة الى ** `{done}` **✅ من الدردشات ، خطأ في ارسال الى ** `{er}` **❌ من الدردشات**"
    )
    
    
CMD_HELP.update(
    {
      "الاذاعه": "**الامر: **`اذاعه للجروبات`<نص/بالرد ؏ ميديا> \
        \n  •  **الوظيفة : **لعمل اذاعه في المجموعات لرسالة معينه او تستطيع بالرد على صورة او ملصق او الخ\
        \n\n **الامر:** `اذاعه للخاص <نص/بالرد ؏ ميديا>` \
        \n •  **الوظيفة  :** لعمل اذاعه لرسالة او صورة بالرد ؏ الشي التريد توسليه اذاعه بالامر "
    }
)
