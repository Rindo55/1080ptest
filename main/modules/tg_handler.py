import asyncio

import sys

from main.modules.compressor import compress_video

from main.modules.utils import episode_linker, get_duration, get_epnum, status_text

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from main.modules.uploader import upload_video

import os

from main.modules.db import del_anime, save_uploads

from main.modules.downloader import downloader

from main.modules.anilist import get_anilist_data, get_anime_img, get_anime_name

from config import INDEX_USERNAME, UPLOADS_USERNAME, UPLOADS_ID, INDEX_ID, PROGRESS_ID, LINK_ID

from main import app, queue, status

from pyrogram.errors import FloodWait

from pyrogram import filters

from main.inline import button1

status: Message

async def tg_handler():

    while True:

        try:

            if len(queue) != 0:

                i = queue[0]  

                queue.remove(i)

                val, id, name, ep_num, video = await start_uploading(i)

                await del_anime(i["title"])

                await save_uploads(i["title"])

                await status.edit(await status_text(f"Adding Links To Index Channel ({INDEX_USERNAME})..."),reply_markup=button1)

                await channel_handler(val,id,name,ep_num, video)

                await status.edit(await status_text("Sleeping For 5 Minutes..."),reply_markup=button1)

                await asyncio.sleep(30)

            else:                

                if "Idle..." in status.text:

                    try:

                        await status.edit(await status_text("Idle..."),reply_markup=button1)

                    except:

                        pass

                await asyncio.sleep(30)

                

        except FloodWait as e:

            flood_time = int(e.x) + 5

            try:

                await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"),reply_markup=button1)

            except:

                pass

            await asyncio.sleep(flood_time)

        except:

            pass

            

async def start_uploading(data):

    try:

        title = data["title"]
        title = title.replace("Shinka", "Shin Shinka")
        title = title.replace("Ijiranaide, Nagatoro-san S2", "Ijiranaide, Nagatoro-san 2")
        link = data["link"]

        size = data["size"]

        name, ext = title.split(".")

        name += f" @animxt." + ext

        fpath = "downloads/" + name
        KAYO_ID = -1001591697490
        name = name.replace(f" @animxt.","").replace(ext,"").strip()
        id, img, tit = await get_anime_img(get_anime_name(title))
        msg = await app.send_photo(UPLOADS_ID,photo=img,caption=title)
        img, caption = await get_anilist_data(title)

        print("Downloading --> ",name)

        await status.edit(await status_text(f"Downloading {name}"),reply_markup=button1)

        file = await downloader(msg,link,size,title)

        await msg.edit(f"Download Complete : {name}")

        print("Encoding --> ",name)

        await status.edit(await status_text(f"Encoding {name}"),reply_markup=button1)

        duration = get_duration(file)
        filed = os.path.basename(file)
        filed = filed.rsplit(' ', 1)[0]
        filed = filed.replace("[SubsPlease]", "")
        filed = filed.replace("Shinka", "Shin Shinka")
        filed = filed.replace("(1080p)", "[1080p Web-DL].mkv")
        ghostname = name
        ghostname = ghostname.replace("(1080p)", "")
        main = await app.send_photo(KAYO_ID,photo=img,caption=caption)
        guessname = f"**{ghostname}**" + "\n" + "✓  `1080p x264 Web-DL`" + "\n" + "✓  `English Sub`" + "\n" + f"__({tit})__" + "\n"+ "#Source #WebDL"
        

        videox = await app.send_document(

                KAYO_ID,

            document=file,
            
            caption=guessname,

            file_name=filed,

            force_document=True

            )        
        videox_id = videox.message_id
        videox_id = int(videox_id)
        
        os.rename(file,"video.mkv")


        

        compressed = await compress_video(duration,videox,name,guessname)
        
        dingdong = await videox.edit(guessname)


        if compressed == "None" or compressed == None:

            print("Encoding Failed Uploading The Original File")

            os.rename("video.mkv",fpath)

        else:

            os.rename("out.mkv",fpath)

        print("Uploading --> ",name)

        await status.edit(await status_text(f"Uploading {name }"),reply_markup=button1)

        message_id = int(msg.message_id) + 1

        video = await upload_video(msg,fpath,id,tit,name,size)   

        try:

            os.remove("video.mkv")

            os.remove("out.mkv")

            os.remove(file)

            os.remove(fpath)

        except:

            pass     

    except FloodWait as e:

        flood_time = int(e.x) + 5

        try:

            await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"),reply_markup=button1)

        except:

            pass

        await asyncio.sleep(flood_time)

    return message_id, id, tit, name, video
