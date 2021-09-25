# dont argue with credit and copyright, i m just a user of UserBot, not having personal connection with Admins of CatUB, I know, Ultroid made writer.py, afterwards i change something more in that and made as per CatUB for my personal use only. I don't have intensity to Promote/demote any community, Bye :) @insane_119 

"""
✘ Commands Available -
`{tr}write <text or reply to text>`
   It will write on a paper.
"""

import os
import urllib
import requests
from PIL import Image, ImageDraw, ImageFont
from userbot import catub
import json
import textwrap
from ..core.managers import edit_delete, edit_or_reply
from . import *



plugin_category = "extra"


@catub.cat_cmd(
    pattern="write ?(.*)",
    command=("write", plugin_category),
    info={
        "header": "Write anything in a page",
        "description": "Good notepad :)\ncredit goes to real owner of writer's codes. Fully modified as per CatUb by [insane](tg://user?id=1325747068)",
        "flags": {
            "NH": "To use Normal  handwriting",
            "CH": "To use Cursive handwriting",
            "SH": "To use Super cursive handwriting",
            "FH": "To use Fair handwriting",
            "UH": "To use Ultra fair handwriting",            
        },
        "usage": [
            "{tr}write <text>",
            "{tr}write <reply to text>",
            "{tr}write <flag> <text/reply to text>",   
        ],
        "examples": [
            "{tr}write Cat is the cutest animal",
            "{tr}write UH Cat is the cutest animal",    
        ],
    },
)

async def writer(e):
    if e.reply_to:
        reply = await e.get_reply_message()
        text = reply.message
        reply_not_true = False
    elif e.pattern_match.group(1):
        text = e.text.split(maxsplit=1)[1] 
        reply_not_true = True
    else:
        return await edit_or_reply(e, "`Give some text too`")
    reply_to_id = await reply_id(e)
    catevent = await edit_or_reply(e, "`Processing.....`")    
    input_str = "".join(e.text.split(maxsplit=1)[1:]).split(" ", 2)
    fnt = input_str[0]
  

    data = json.loads('{"NH":"https://github.com/Hex231/Res/blob/main/TalkingToTheMoon.ttf?raw=true","CH":"https://github.com/Hex231/Res/blob/main/Mumsies.ttf?raw=true","SH":"https://github.com/Hex231/Res/blob/main/Always%20In%20My%20Heart.ttf?raw=true","FH":"https://github.com/Hex231/Res/blob/main/Husband%20of%20the%20Millennium.ttf?raw=true","GH":"https://github.com/Hex231/Res/blob/main/Quikhand.ttf?raw=true"}')
    data_w = json.loads('{"NH":55,"CH":40,"SH":75,"FH":45,"GH":65}') 
    fontdtyli = f"https://github.com/Hex231/Res/blob/main/assfont.ttf?raw=true"

    if fnt in ['NH', 'CH', 'SH', 'FH', 'GH']:
        fontdtyli = data[fnt]
        font_w = data_w[fnt]
        if reply_not_true:
            text = text.split(' ', 1)[1]     
    else:
        font_w = 55  	    
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    if not os.path.exists("temp/template.jpg"):
        urllib.request.urlretrieve(f"https://raw.githubusercontent.com/Hex231/Res/main/template.jpg", "temp/template.jpg")
    img = Image.open("./temp/template.jpg")
    draw = ImageDraw.Draw(img)   
    if not os.path.exists("temp/Pen.ttf"):    	
        urllib.request.urlretrieve(fontdtyli, "temp/Pen.ttf")
 
    font = ImageFont.truetype("temp/Pen.ttf", 30)    
    x, y = 150, 140
    txt_ar = text.split("\n")
    av,txt_fnl = 0,""
    for av in range(len(txt_ar)):
      co = txt_ar[av]
      txt_fnl = txt_fnl + textwrap.fill(co, font_w) + "\n"  
      av = av + 1
    line_height = font.getsize("hg")[1]
    draw.text((x, y), txt_fnl, fill=(1, 22, 55), font=font)

    file = "ult.jpg"
    img.save(file)
    if reply_to_id:
    	e = reply
    await e.reply(file=file)
    os.remove(file)
    os.remove("temp/Pen.ttf")
    await catevent.delete()
