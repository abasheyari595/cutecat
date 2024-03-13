# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import json
import logging

import requests

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)

TEMPAT = ''


@borg.on(admin_cmd(pattern=("مؤذن ?(.*)")))
async def get_adzan(adzan):
    if not adzan.text.startswith("."):
        return ""

    if not adzan.pattern_match.group(1):
        LOKASI = TEMPAT
        if not LOKASI:
            await adzan.edit("يرجى تحديد المدينة او المحافظه.")
            return
    else:
        LOKASI = adzan.pattern_match.group(1)

    url = f'http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc'
    request = requests.get(url)
    result = json.loads(request.text)

    if request.status_code != 200:
        await adzan.edit(f"{result['status_description']}")
        return

    tanggal = result["items"][0]["date_for"]
    lokasi = result["query"]
    lokasi2 = result["country"]
    lokasi3 = result["address"]
    lokasi4 = result["state"]

    subuh = result["items"][0]["fajr"]
    syuruk = result["items"][0]["shurooq"]
    zuhur = result["items"][0]["dhuhr"]
    ashar = result["items"][0]["asr"]
    maghrib = result["items"][0]["maghrib"]
    isya = result["items"][0]["isha"]

    textkirim = (f"**جـــدول صــــــل⏱وآت **🌷🌹 :\n"
        f"📅 آلتآريـﮯخ | `{tanggal}` :\n" +
                 f"`{lokasi} | {lokasi2} | {lokasi3} | {lokasi4}`\n\n" +
        f"الـفـجـــر : {subuh}\n"
        f"الـظــهــر : {zuhur}\n"
        f"الـعصـــر : {ashar}\n"
        f"الـمـغـرب : {maghrib}\n"
        f"الـعشـ ـآء : {isya}\n"
    f"          ↠━━━━ღ◆ღ━━━━↞\n")

    await adzan.edit(textkirim)