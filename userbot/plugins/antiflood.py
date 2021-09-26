import asyncio

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from ..sql_helper import antiflood_sql as sql
from ..utils import is_admin
from . import edit_or_reply, catub

plugin_category = "admin"
CHAT_FLOOD = sql.__load_flood_settings()

ANTI_FLOOD_WARN_MODE = ChatBannedRights(
    until_date=None, view_messages=None, send_messages=True
)


@catub.cat_cmd(incoming=True, groups_only=True)
async def _(event):
    if not CHAT_FLOOD:
        return
    catadmin = await is_admin(event.client, event.chat_id, event.client.uid)
    if not catadmin:
        return
    if str(event.chat_id) not in CHAT_FLOOD:
        return
    should_ban = sql.update_flood(event.chat_id, event.message.sender_id)
    if not should_ban:
        return
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id, event.message.sender_id, ANTI_FLOOD_WARN_MODE
            )
        )
    except Exception:
        no_admin_privilege_message = await event.client.send_message(
            entity=event.chat_id,
            message=f"**⌔∮ تنبيه التكرار للادمنية ⚠️**\n\n**▾∮ الى** @admin **المجموعة!**\n**▾∮ قام↫** [المستخدم](tg://user?id={event.message.sender_id})\n**▾∮بتكرار رسائله في المجموعة**\n",
            reply_to=event.message.id,
        )
        await asyncio.sleep(4)
        await no_admin_privilege_message.edit(
            "**⌔∮هذا هو الشخص الذي قام بالتكرار \n توقف يا رجل لكي لا تًطرد 📵**"
        )
    else:
        await event.client.send_message(
            entity=event.chat_id,
            message=f"**⌔∮ عملية التقيد التلقائي للتكرار ⚠️**\n\n**▾ قام ↫**[المستخدم ](tg://user?id={event.message.sender_id})\n**▾∮تم تقييده تلقائيًا بسبب عبوره حد السماح بالتكرار في هذه المجموعة**",
            reply_to=event.message.id,
        )


@catub.cat_cmd(
    pattern="^ضع تكرار(?:\s|$)([\s\S]*)",
    command=("ضع تكرار", plugin_category),
    info={
        "عمل الملف": "لإعداد مضاد للتكرار في مجموعة",
        "وصف الملف": "يحذر المستخدم إذا قام بإرسال رسائل اكثر من العدد الموضوع من قبلك في المجموعة\n اذا كانت لديك صلاحيات اشراف فـأنه سيقـوم بكتم المستخـدم في تلك المجموعة ( مسح رسائله).",
        "ملاحظة": "لايقاف تحذير التكرار ضع قيمة عالية مثل ( {tr}ضع تكرار 9999999 )",
        "طريقة الاستخدام": "{tr} ضع تكرار <عدد صغير> (لوضع التكرار\n{tr} ضع تكرار <عدد كبير> (لالغاء تحذير التكرار)",
        "مثال عن الامر": [
            "{tr}ضع تكرار 7",
            "{tr}ضع تكرار 9999999999",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "لوضع عدد تكرار الرسائل في المجموعة"
    input_str = event.pattern_match.group(1)
    event = await edit_or_reply(event, "**▾∮ يتم وضع عدد التكرار الجديد ... ♻️**")
    await asyncio.sleep(2)
    try:
        sql.set_flood(event.chat_id, input_str)
        sql.__load_flood_settings()
        await event.edit(f"**▾∮ عدد التكرار في المجموعة الان** ↫`┆{input_str}┆` 📊")
    except Exception as e:
        await event.edit(str(e))
