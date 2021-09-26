#credit @YVW_6 do not steal
from telethon.errors.rpcerrorlist import YouBlockedUserError
import asyncio
from userbot import bot
from userbot.utils import admin_cmd

@bot.on(admin_cmd(pattern="^bin ?(.*)"))
async def sed(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("__Please input bin who want to check!..__")
    await event.edit(f"```𝙲𝙷𝙴𝙲𝙺𝙸𝙽𝙶 𝙱𝙸𝙽 𝚆𝙰𝙸𝚃...```")
    async with bot.conversation("@kurumichkbot") as conv:
        try:
            jemboed = await conv.send_message(f"/bin {query}")
            await asyncio.sleep(10)
            asu = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await event.reply("Unblock @kurumichkbot or chat first")
        if asu.text.startswith("Wait for result..."):
            return await event.edit(f"Bin {query} Invalid!")
        else:
            await event.edit(asu.message)
            await event.client.delete_messages(conv.chat_id, [jemboed.id, asu.id])
            
@bot.on(admin_cmd(pattern="^check ?(.*)"))
async def sed(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("__Please input cc who want to check!..__")
    await event.edit(f"```𝙲𝙷𝙴𝙲𝙺𝙸𝙽𝙶 𝙲𝙲 𝚆𝙰𝙸𝚃...```")
    async with bot.conversation("@AuthCheckerBot") as conv:
        try:
            jemboed = await conv.send_message(f"/ss {query}")
            await asyncio.sleep(10)
            asu = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)			
        except YouBlockedUserError:
            return await event.reply("Unblock @AuthCheckerBot or chat first")
        if asu.text.startswith("Wait for result..."):
            return await event.edit(f"cc {query} Invalid!")
        else:
            await event.edit(asu.message)
            await event.client.delete_messages(conv.chat_id, [jemboed.id, asu.id])
            
@bot.on(admin_cmd(pattern="^gen ?(.*)"))
async def sed(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("__Please input bin who want to generate!..__")
    await event.edit(f"`𝙶𝙴𝙽𝙴𝚁𝙰𝚃𝙴 𝙲𝙲 𝚆𝙰𝙸𝚃...`")
    async with bot.conversation("@AuthCheckerBot") as conv:
        try:
            jemboed = await conv.send_message(f"/gen {query}")
            await asyncio.sleep(10)
            asu = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)			
        except YouBlockedUserError:
            return await event.reply("Unblock @AuthCheckerBot or chat first")
        if asu.text.startswith("Wait for result..."):
            return await event.edit(f"bin {query} Invalid!")
        else:
            await event.edit(asu.message)
            await event.client.delete_messages(conv.chat_id, [jemboed.id, asu.id])
            
@bot.on(admin_cmd(pattern="^chc ?(.*)"))
async def sed(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("__Please input cc who want to check!..__")
    await event.edit(f"`𝙲𝙷𝙴𝙲𝙺𝙸𝙽𝙶 𝙲𝙲 𝚆𝙰𝙸𝚃...`")
    async with bot.conversation("@MarioChkBot") as conv:
        try:
            jemboed = await conv.send_message(f"!chc {query}")
            await asyncio.sleep(10)
            asu = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)			
        except YouBlockedUserError:
            return await event.reply("Unblock @MarioChkBot or chat first")
        if asu.text.startswith("Wait for result..."):
            return await event.edit(f"cc {query} Invalid!")
        else:
            await event.edit(asu.message)
            await event.client.delete_messages(conv.chat_id, [jemboed.id, asu.id])
     
@bot.on(admin_cmd(pattern="^chk ?(.*)"))
async def sed(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("__Please input cc who want to check!..__")
    await event.edit(f"```𝙲𝙷𝙴𝙲𝙺𝙸𝙽𝙶 𝙲𝙲 𝚆𝙰𝙸𝚃...```")
    async with bot.conversation("@AuthCheckerBot") as conv:
        try:
            jemboed = await conv.send_message(f"/chk {query}")
            await asyncio.sleep(10)
            asu = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)			
        except YouBlockedUserError:
            return await event.reply("Unblock @AuthCheckerBot or chat first")
        if asu.text.startswith("Wait for result..."):
            return await event.edit(f"cc {query} Invalid!")
        else:
            await event.edit(asu.message)
            await event.client.delete_messages(conv.chat_id, [jemboed.id, asu.id])            
                          
@bot.on(admin_cmd(pattern="^nmap ?(.*)"))
async def sed(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("__Please enter the domain that you want to check!..__")
    await event.edit(f"```Getting info {query}..```")
    async with bot.conversation("@scriptkiddies_bot") as conv:
        try:
            jemboed = await conv.send_message(f"/nmap {query}")
            asu = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await event.reply("Unblock @scriptkiddies_bot or chat first")
        else:
            await event.edit(asu.message)
            await event.client.delete_messages(conv.chat_id, [jemboed.id, asu.id])


@bot.on(admin_cmd(pattern="^subd ?(.*)"))
async def sed(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("__Please enter the domain that you want to generate!..__")
    await event.edit(f"```Generated subdomain {query}..```")
    async with bot.conversation("@scriptkiddies_bot") as conv:
        try:
            jemboed = await conv.send_message(f"/subdomain {query}")
            asu = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await event.reply("Unblock @scriptkiddies_bot or chat first")
        else:
            await event.edit(asu.message)
            await event.client.delete_messages(conv.chat_id, [jemboed.id, asu.id])


@bot.on(admin_cmd(pattern="^cekhttp ?(.*)"))
async def sed(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("__Please enter the domain that you want to check!..__")
    await event.edit(f"```Checking Respond {query}..```")
    async with bot.conversation("@scriptkiddies_bot") as conv:
        try:
            jemboed = await conv.send_message(f"/httpheader {query}")
            asu = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await event.reply("Unblock @scriptkiddies_bot or chat first")
        else:
            await event.edit(asu.message)
            await event.client.delete_messages(conv.chat_id, [jemboed.id, asu.id])

CMD_HELP.update({
    "checker":
    "**HELP FOR CHECKER**\
\n╭━━━━━━━━━━━━━━━━━━━╮\
\n\n  `.bin <bin number>`\
\n   Usage: to check bin information.\
\n\n  `.check <cc|m|y|cvv>`\
\n   Usage: to check respond cc.\
\n\n  `.gen <bin>`\
\n   Usage: to generate cc with bin.\
\n\n  `.chc <cc|m|y|cvv>`\
\n   Usage: to check Stripe Charge 1$.\
\n\n  `.chk <cc|m|y|cvv>`\
\n   Usage: to check live cc.\
\n\n  `.nmap <domain hosts>`\
\n   Usage: to get info bug/host.\
\n\n  `.subd <domain hosts>`\
\n   Usage: to get subdomain bug/host.\
\n\n  `.cekhttp <domain hosts>`\
\n   Usage: to check respons bug/host.\
\n╰━━━━━━━━━━━━━━━━━━━╯"
})
