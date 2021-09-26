# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import html
import os

from requests import get
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_input_location

from userbot import catub

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers import get_user_from_event, reply_id
from . import spamwatch

plugin_category = "fun"

C = (
    "\n......................................../´¯/) "
    "\n......................................,/¯../ "
    "\n...................................../..../ "
    "\n..................................../´.¯/"
    "\n..................................../´¯/"
    "\n..................................,/¯../ "
    "\n................................../..../ "
    "\n................................./´¯./"
    "\n................................/´¯./"
    "\n..............................,/¯../ "
    "\n............................./..../ "
    "\n............................/´¯/"
    "\n........................../´¯./"
    "\n........................,/¯../ "
    "\n......................./..../ "
    "\n....................../´¯/"
    "\n....................,/¯../ "
    "\n.................../..../ "
    "\n............./´¯/'...'/´¯¯`·¸ "
    "\n........../'/.../..../......./¨¯\ "
    "\n........('(...´...´.... ¯~/'...') "
    "\n.........\.................'...../ "
    "\n..........''...\.......... _.·´ "
    "\n............\..............( "
    "\n..............\.............\..."
)

@catub.cat_cmd(
    pattern="^خد$",
    command=("خد", plugin_category),
)
async def kakashi(mf):
    """اوامر التحشيش ."""
    await edit_or_reply(mf, C)

@catub.cat_cmd(
    pattern="^رفع مرتي(?:\s|$)([\s\S]*)",
    command=("رفع مرتي", plugin_category),
)
async def permalink(mention):
    """اوامر التحشيش ."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 1694386561:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    if user.id == 1657933680:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    if user.id == 1715051616:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور **")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌔︙ المستخدم [{tag}](tg://user?id={user.id}) \n⌔︙  تـم رفعـه مـࢪتك مـشي نخـلف 😹🤤")

@catub.cat_cmd(
    pattern="^رفع جلب(?:\s|$)([\s\S]*)",
    command=("رفع جلب", plugin_category),
)
async def permalink(mention):
    """اوامر التحشيش ."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 1694386561:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    if user.id == 1657933680:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    if user.id == 1715051616:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور **")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌔︙ المستخدم [{tag}](tg://user?id={user.id}) \n⌔︙  تـم رفعـه جلب خليه خله ينبح 😂🐶")

@catub.cat_cmd(
    pattern="^رفع تاج(?:\s|$)([\s\S]*)",
    command=("رفع تاج", plugin_category),
)
async def permalink(mention):
    """اوامر التحشيش ."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌔︙ المستخدم [{tag}](tg://user?id={user.id}) \n⌔︙  تـم رفعـه تاج 👑🔥")

@catub.cat_cmd(
    pattern="^رفع قرد(?:\s|$)([\s\S]*)",
    command=("رفع قرد", plugin_category),
)
async def permalink(mention):
    """اوامر التحشيش ."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 1694386561:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    if user.id == 1657933680:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    if user.id == 1715051616:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور **")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌔︙ المستخدم [{tag}](tg://user?id={user.id}) \n⌔︙  تـم رفعـه قرد واعطائه موزة 🐒🍌")

@catub.cat_cmd(
    pattern="^رفع بكلبي(?:\s|$)([\s\S]*)",
    command=("رفع بكلبي", plugin_category),
)
async def permalink(mention):
    """اوامر التحشيش ."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌔︙ المستخدم [{tag}](tg://user?id={user.id}) \n⌔︙  تـم رفعـه بڪلبك 🖤 ")
    
    
@catub.cat_cmd(
    pattern="^رفع مطي(?:\s|$)([\s\S]*)",
    command=("رفع مطي", plugin_category),
)
async def permalink(mention):
    """اوامر التحشيش ."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 1694386561:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    if user.id == 1657933680:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    if user.id == 1715051616:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور **")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌔︙ المستخدم [{tag}](tg://user?id={user.id}) \n⌔︙  تـم رفـعه مطي هـنا ")
    
@catub.cat_cmd(
    pattern="^رفع زوجي(?:\s|$)([\s\S]*)",
    command=("رفع زوجي", plugin_category),
)
async def permalink(mention):
    """اوامر التحشيش ."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌔︙ المستخدم [{tag}](tg://user?id={user.id}) \n⌔︙ تـم رفعه زوجج روحوا خلفوا 🤤😂")
