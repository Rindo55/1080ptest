import asyncio
import os
import time
import aiohttp
import requests
import aiofiles

from main.modules.utils import format_time, get_duration, get_epnum, get_filesize, status_text, tags_generator

from main.modules.anilist import get_anime_name

from main.modules.anilist import get_anime_img

from main.modules.thumbnail import generate_thumbnail

from config import UPLOADS_ID

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from main.modules.progress import progress_for_pyrogram

from os.path import isfile

import os

import time

from main import app, status

from pyrogram.errors import FloodWait

from main.inline import button1

async def upload_video(msg: Message,file,id,tit,name,ttl):

    try:

    

        fuk = isfile(file)

        if fuk:

            r = msg

            c_time = time.time()

            duration = get_duration(file)

            size = get_filesize(file)

            ep_num = get_epnum(name)
            
            rest = tit

            thumbnail = await generate_thumbnail(id,file,tit,ep_num,size,format_time(duration))

            tags = tags_generator(tit)

            buttons = InlineKeyboardMarkup([

                [

                    InlineKeyboardButton(text="Info", url="https://t.me/AnimeXT"),

                    InlineKeyboardButton(text="Comments", url=f"https://t.me/ANIMECHATTERBOX")

                ]

            ])
            filed = os.path.basename(file)
            filed = filed.replace("(1080p)", "[720p x265]")
            caption = f"{name}"
            caption = caption.replace("(1080p)", "")
            gcaption=f"**{caption}**" + "\n" + "✓  `720p x265 10Bit`" + "\n" + "✓  `English Sub`" + "\n" + f"__({tit})__" + "\n" + "#Encoded #HEVC"
            kayo_id = -1001591697490
            x = await app.send_document(

                kayo_id,

            document=file,

            caption=gcaption,

            file_name=filed,

            force_document=True,

            progress=progress_for_pyrogram,
 
            progress_args=(

                os.path.basename(file),

                r,

                c_time,

                ttl

            )

            ) 
        files = {'file': open(file, 'rb')}
        nanix = await x.edit(gcaption + "\n" "━━━━━━━━━━━━━━━━━━━" + "\n" + "Generating Link**", parse_mode = "markdown")
        callapi = requests.post("https://api.filechan.org/upload", files=files)
        text = callapi.json()
        long_url = text['data']['file']['url']['full']
        api_url = f"https://tnlink.in/api?api=fea911843f6e7bec739708f3e562b56184342089&url={long_url}&format=text"
        result = requests.get(api_url)
        nai_text = result.text
        da_url = "https://da.gd/"
        url = nai_text
        shorten_url = f"{da_url}shorten"
        response = requests.get(shorten_url, params={"url": url})
        nyaa_text = response.text.strip()                                     
        output = f"""
{gcaption}
━━━━━━━━━━━━━━━━━━━
[🔗Download Link]({nyaa_text})"""
        daze = await x.edit(output, parse_mode = "markdown")
    except Exception:
       await app.send_message(message.chat.id, text="Something Went Wrong!")
    try:

            await r.delete()

            os.remove(file)

            os.remove(thumbnail)

    except:

        pass

    return x.message_id
