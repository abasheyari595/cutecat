from asyncio import TimeoutError
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import catub

plugin_category = "extra"

@catub.cat_cmd(
    pattern="^sniff$",
    command=("sniff", plugin_category),
    info={
        "header": "Decrypt configs",
        "usage": "{tr}sniff",
    },
)
async def gen(e):
	if e.fwd_from:
		return 
	chat = "@kntlmanis_bot"
	user = await bot.get_me()
	if not user.username:
		uname = user.first_name
	uname = user.username
	reply = await e.get_reply_message()
	if not (reply and reply.media):
		await edit_or_reply(e, "Reply to a File’")
		return
	catevent = await edit_or_reply(e, "`Executing...`")
	ERROR_ = "Unblok bot @kntlmanis_bot To use this Command"
	chat = await e.client.get_entity(chat)
	async with e.client.conversation(chat.username, timeout=15) as conv:
		try: 
			response = conv.wait_event(events.NewMessage(incoming=True, from_users=chat.id))
			await reply.forward_to(chat.username)
			response = await response
		except YouBlockedUserError:
			await catevent.edit(f"`{ERROR_}`")
			return
		except asyncio.TimeoutError:
			return await catevent.edit("`Bot didn't respond in time`")
		except Exception as ex:
			return await catevent.edit(f"Error: `{ex}`")
		msg = response.message.message
		if "Don't Forget To Join Us" in msg:
			msg = msg.replace("Don't Forget To Join Us","").replace("😎 GROUP: @SNIFF_DSO","").replace("💻 SOURCE : @hctools","")
			msg = f"`Dec by: `@{uname}`\n\n{msg}`"
			await catevent.respond(msg, link_preview=False)
			await catevent.delete()
			await catevent.edit("response.message.message")
