# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "extra"

name = "صوره"


@catub.cat_cmd(
    pattern="^صوره(?:\s|$)([\s\S]*)",
    command=("صوره", plugin_category),
    info={
        "header": "للحصول علي صورة الشخص او الجروب.",
        "description": "قم بالرد علي الشخص للحصول علي صورة البروفايل \ مع رقم صورهه الي محتاجها او استخدم امر (`.صوره جميعها`) لارسال جميع صوره. اذا لم تقم بالرد علي اي شخص\
        سوف يرسل لك البوت صورة المجموعه.",
        "usage": [
            "{tr}صوره <رقم الصوره>",
            "{tr}صوره جميعها",
            "{tr}صوره",
        ],
    },
)
async def potocmd(event):
    "للحصول علي صورة الشخص او الجروب"
    uid = "".join(event.raw_text.split(maxsplit=1)[1:])
    user = await event.get_reply_message()
    chat = event.input_chat
    if user:
        photos = await event.client.get_profile_photos(user.sender)
        u = True
    else:
        photos = await event.client.get_profile_photos(chat)
        u = False
    if uid.strip() == "":
        uid = 1
        if int(uid) > (len(photos)):
            return await edit_delete(
                event, "**⌔︙ لم يتم العثور على صورة لهذا  الشخص 🏞**"
            )
        send_photos = await event.client.download_media(photos[uid - 1])
        await event.client.send_file(event.chat_id, send_photos)
    elif uid.strip() == "جميعها":
        if len(photos) > 0:
            await event.client.send_file(event.chat_id, photos)
        else:
            try:
                if u:
                    photo = await event.client.download_profile_photo(user.sender)
                else:
                    photo = await event.client.download_profile_photo(event.input_chat)
                await event.client.send_file(event.chat_id, photo)
            except Exception:
                return await edit_delete(event, "**⌔︙ هذا المستخدم ليس لديه صور لتظهر لك  🙅🏼  **")
    else:
        try:
            uid = int(uid)
            if uid <= 0:
                await edit_or_reply(
                    event, "**⌔︙ الرقم غير صحيح - اختر رقم صوره موجود فعليا ⁉️**"
                )
                return
        except BaseException:
            await edit_or_reply(event, "**⌔︙ هناك خطا  ⁉️**")
            return
        if int(uid) > (len(photos)):
            return await edit_delere(
                event, "**⌔︙ لم يتم العثور على صورة لهذا  الشخص 🏞**"
            )

        send_photos = await event.client.download_media(photos[uid - 1])
        await event.client.send_file(event.chat_id, send_photos)
    await event.delete()
