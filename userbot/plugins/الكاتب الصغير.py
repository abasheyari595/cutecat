# dont argue with credit and copyriart, i m just a user of UserBot, not having personal connection with Admins of CatUB, I know, Ultroid made writer.py, afterwards i change something more in that and made as per CatUB for my personal use only. I don't have intensity to Promote/demote any community, Bye :) @insane_119 

"""
✘ Commands Available -

• `{i}write <text or reply to text>`
   It will write on a paper.

• `{i}image <text or reply to html or any doc file>`
   Write a image from html or any text.
"""

import os

from htmlwebshot import WebShot
from PIL import Image, ImageDraw, ImageFont

from . import eod, get_string, text_set
from . import *


@catub.cat_cmd(pattern="^image( (.*)|$)")
async def f2i(e):
    txt = e.pattern_match.group(1).strip()
    html = None
    if txt:
        html = e.text.split(maxsplit=1)[1]
    elif e.reply_to:
        r = await e.get_reply_message()
        if r.media:
            html = await e.client.download_media(r.media)
        elif r.text:
            html = r.text
    if not html:
        return await eod(e, "`Either reply to any file or give any text`")
    html = html.replace("\n", "<br>")
    shot = WebShot(quality=85)
    css = "body {background: white;} p {color: red;}"
    pic = await shot.create_pic_async(html=html, css=css)
    await e.reply(file=pic, force_document=True)
    os.remove(pic)
    if os.path.exists(html):
        os.remove(html)


@catub.cat_cmd(pattern="^write( (.*)|$)")
async def writer(e):
    if e.reply_to:
        reply = await e.get_reply_message()
        text = reply.message
    elif e.pattern_match.group(1).strip():
        text = e.text.split(maxsplit=1)[1]
    else:
        return await eod(e, get_string("writer_1"))
    k = await e.eor(get_string("com_1"))
    img = Image.open("https://raw.githubusercontent.com/abasheyari595/maker/main/template.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("https://github.com/abasheyari595/maker/blob/main/assfont.ttf?raw=true", 30)
    x, y = 150, 140
    lines = text_set(text)
    line_height = font.getsize("hg")[1]
    for line in lines:
        draw.text((x, y), line, fill=(1, 22, 55), font=font)
        y = y + line_height - 5
    file = "ult.jpg"
    img.save(file)
    await e.reply(file=file)
    os.remove(file)
    await k.delete()
    
    
@catub.cat_cmd(pattern="^كتابه( (.*)|$)")
async def writer(e):
    if e.reply_to:
        reply = await e.get_reply_message()
        text = reply.message
    elif e.pattern_match.group(1).strip():
        text = e.text.split(maxsplit=1)[1]
    else:
        return await eod(e, get_string("writer_1"))
    k = await e.eor(get_string("com_1"))
    img = Image.open("https://raw.githubusercontent.com/abasheyari595/maker/main/template.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("https://github.com/abasheyari595/maker/blob/main/Gold.ttf?raw=true", 30)
    x, y = 150, 140
    lines = text_set(text)
    line_height = font.getsize("hg")[1]
    for line in lines:
        draw.text((x, y), line, fill=(1, 22, 55), font=font)
        y = y + line_height - 5
    file = "ult.jpg"
    img.save(file)
    await e.reply(file=file)
    os.remove(file)
    await k.delete()
