# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

from telethon.tl import functions

from .. import catub
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..utils.tools import create_supergroup

plugin_category = "tools"


@catub.cat_cmd(
    pattern="^انشاء (مجموعه خارقه|مجموعه عاديه|قناه) ([\s\S]*)",
    command=("انشاء", plugin_category),
    info={
        "header": "⌔︙لإنشاء مجموعة خاصة/قناة مع تليثون ڤينوم  ☸️",
        "description": "⌔︙إستخدام الامر لإنشاء مجموعة خارقة، مجموعة عادية أو قناة  ⚜️",
        "flags": {
            "مجموعه خارقه": "⌔︙لإنشاء مجموعة خارقة خاصة",
            "مجموعه عاديه": "⌔︙لإنشاء مجموعة أساسية خاصة.",
            "قناه": "⌔︙لإنشاء قناة خاصة ",
        },
        "usage": "{tr}انشاء (مجموعه خارقه|مجموعه عاديه|قناه) <اسم المجموعه او القناه>",
        "examples": "{tr}انشاء مجموعه خارقه + اسم الكروب",
    },
)
async def _(event):
    "⌔︙لإنشاء مجموعة خاصة/قناة مع مستخدم البوت  ☸️"
    type_of_group = event.pattern_match.group(1)
    group_name = event.pattern_match.group(2)
    if type_of_group == "قناه":
        descript = "⌔︙ هذه قناة إختبار أُنشئت بإستعمال تيلثون كات"
    else:
        descript = "⌔︙ هذه المجموعه إختبار أُنشئت بإستعمال تيلثون كات"
    if type_of_group == "مجموعه خارقه":
        try:
            result = await event.client(
                functions.messages.CreateChatRequest(
                    users=[Config.TG_BOT_USERNAME],
                   
                    title=group_name,
                )
            )
            created_chat_id = result.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await edit_or_reply(
                event, f"⌔︙ اسم المجموعه `{group_name}` ** تم الإنشاء بنجاح  ✅  دخول ** {result.link}"
            )
        except Exception as e:
            await edit_delete(event, f"**⌔︙ حدث خطأ ما  🆘:**\n{str(e)}")
    elif type_of_group == "قناه":
        try:
            r = await event.client(
                functions.channels.CreateChannelRequest(
                    title=group_name,
                    about=descript,
                    megagroup=False,
                )
            )
            created_chat_id = r.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await edit_or_reply(
                event,
                f"⌔︙ اسم القناه `{group_name}` ** تم الإنشاء بنجاح  ✅  دخول ** {result.link}",
            )
        except Exception as e:
            await edit_delete(event, f"**⌔︙ حدث خطأ ما  🆘 :**\n{str(e)}")
    elif type_of_group == "مجموعه خارقه":
        answer = await create_supergroup(
            group_name, event.client, Config.TG_BOT_USERNAME, descript
        )
        if answer[0] != "error":
            await edit_or_reply(
                event,
                f"⌔︙ ميجا جروب `{group_name}` ** تم الإنشاء بنجاح  ✅  دخول ** {answer[0].link}",
            )
        else:
            await edit_delete(event, f"**⌔︙ حدث خطأ ما  🆘 :**\n{str(answer[1])}")
    else:
        await edit_delete(event, "**⌔︙الاوامر` **صنع مجموعه لمعرفة كيفية استخدامي.`")
