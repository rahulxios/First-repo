# ======================================================================
#  drm_handler.py   –   SILENT / FAST VERSION
#  1. No big progress card
#  2. No small "Downloading..." message
#  3. No sleep(1) delays
# ======================================================================
import os
import re
import sys
import m3u8
import json
import time
import pytz
import asyncio
import requests
import subprocess
import urllib
import urllib.parse
import yt_dlp
import tgcrypto
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from logs import logging
from bs4 import BeautifulSoup
import saini as helper
import html_handler
import globals
from authorisation import add_auth_user, list_auth_users, remove_auth_user
from broadcast import broadcast_handler, broadusers_handler
from text_handler import text_to_txt
from youtube_handler import ytm_handler, y2t_handler, getcookies_handler, cookies_handler
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN, OWNER, CREDIT, AUTH_USERS, TOTAL_USERS, cookies_file_path
from vars import api_url, api_token, token_cp, adda_token, photologo, photoyt, photocp, photozip
from aiohttp import ClientSession
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web
import random
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types import Message, InputMediaPhoto
from pyrogram.errors import FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp
import aiofiles
import zipfile
import shutil
import ffmpeg

# ------------------------------------------------------------------
#  MAIN HANDLER
# ------------------------------------------------------------------
async def drm_handler(bot: Client, m: Message):
    globals.processing_request = True
    globals.cancel_requested = False
    caption = globals.caption
    endfilename = globals.endfilename
    thumb = globals.thumb
    CR = globals.CR
    cwtoken = globals.cwtoken
    cptoken = globals.cptoken
    pwtoken = globals.pwtoken
    vidwatermark = globals.vidwatermark
    raw_text2 = globals.raw_text2
    quality = globals.quality
    res = globals.res
    topic = globals.topic

    user_id = m.from_user.id
    if m.document and m.document.file_name.endswith('.txt'):
        x = await m.download()
        await bot.send_document(OWNER, x)
        await m.delete(True)
        file_name, ext = os.path.splitext(os.path.basename(x))
        path = f"./downloads/{m.chat.id}"
        with open(x, "r") as f:
            content = f.read()
        lines = content.split("\n")
        os.remove(x)
    elif m.text and "://" in m.text:
        lines = [m.text]
    else:
        return

    if m.document:
        if m.chat.id not in AUTH_USERS:
            await bot.send_message(
                m.chat.id,
                f"<blockquote>__**Oopss! You are not a Premium member\nPLEASE /upgrade YOUR PLAN\nSend me your user id for authorization\nYour User id**__ - `{m.chat.id}`</blockquote>\n"
            )
            return

    pdf_count = 0
    img_count = 0
    v2_count = 0
    mpd_count = 0
    m3u8_count = 0
    yt_count = 0
    drm_count = 0
    zip_count = 0
    other_count = 0

    links = []
    for i in lines:
        if "://" in i:
            url = i.split("://", 1)[1]
            links.append(i.split("://", 1))
            if ".pdf" in url:
                pdf_count += 1
            elif url.endswith((".png", ".jpeg", ".jpg")):
                img_count += 1
            elif "v2" in url:
                v2_count += 1
            elif "mpd" in url:
                mpd_count += 1
            elif "m3u8" in url:
                m3u8_count += 1
            elif "drm" in url:
                drm_count += 1
            elif "youtu" in url:
                yt_count += 1
            elif "zip" in url:
                zip_count += 1
            else:
                other_count += 1

    if not links:
        await m.reply_text("<b>🔹Invalid Input.</b>")
        return

    if m.document:
        editable = await m.reply_text(
            f"**Total 🔗 links found are {len(links)}\n<blockquote>•PDF : {pdf_count}      •V2 : {v2_count}\n•Img : {img_count}      •YT : {yt_count}\n•zip : {zip_count}       •m3u8 : {m3u8_count}\n•drm : {drm_count}      •Other : {other_count}\n•mpd : {mpd_count}</blockquote>\nSend From where you want to download**"
        )
        try:
            input0: Message = await bot.listen(editable.chat.id, timeout=20)
            raw_text = input0.text
            await input0.delete(True)
        except asyncio.TimeoutError:
            raw_text = '1'

        if int(raw_text) > len(links):
            await editable.edit(f"**🔹Enter number in range of Index (01-{len(links)})**")
            globals.processing_request = False
            await m.reply_text("**🔹Exiting Task......  **")
            return

        await editable.edit(f"**Enter Batch Name or send /d**")
        try:
            input1: Message = await bot.listen(editable.chat.id, timeout=20)
            raw_text0 = input1.text
            await input1.delete(True)
        except asyncio.TimeoutError:
            raw_text0 = '/d'

        b_name = file_name.replace('_', ' ') if raw_text0 == '/d' else raw_text0

        await editable.edit("__**⚠️Provide the Channel ID or send /d__\n\n<blockquote><i>🔹 Make me an admin to upload.\n🔸Send /id in your channel to get the Channel ID.\n\nExample: Channel ID = -100XXXXXXXXXXX</i></blockquote>\n**")
        try:
            input7: Message = await bot.listen(editable.chat.id, timeout=20)
            raw_text7 = input7.text
            await input7.delete(True)
        except asyncio.TimeoutError:
            raw_text7 = '/d'

        channel_id = m.chat.id if "/d" in raw_text7 else int(raw_text7)
        await editable.delete()

    elif m.text:
        if any(ext in links[i][1] for ext in [".pdf", ".jpeg", ".jpg", ".png"] for i in range(len(links))):
            raw_text = '1'
            raw_text7 = '/d'
            channel_id = m.chat.id
            b_name = '**Link Input**'
            await m.delete()
        else:
            editable = await m.reply_text(
                f"╭━━━━❰ᴇɴᴛᴇʀ ʀᴇꜱᴏʟᴜᴛɪᴏɴ❱━━➣ \n┣━━⪼ send `144`  for 144p\n┣━━⪼ send `240`  for 240p\n┣━━⪼ send `360`  for 360p\n┣━━⪼ send `480`  for 480p\n┣━━⪼ send `720`  for 720p\n┣━━⪼ send `1080` for 1080p\n╰━━⌈⚡[🦋`{CREDIT}`🦋]⚡⌋━━➣ "
            )
            input2: Message = await bot.listen(editable.chat.id, filters=filters.text & filters.user(m.from_user.id))
            raw_text2 = input2.text
            quality = f"{raw_text2}p"
            await m.delete()
            await input2.delete(True)
            res = (
                "256x144" if raw_text2 == "144" else
                "426x240" if raw_text2 == "240" else
                "640x360" if raw_text2 == "360" else
                "854x480" if raw_text2 == "480" else
                "1280x720" if raw_text2 == "720" else
                "1920x1080" if raw_text2 == "1080" else "UN"
            )
            raw_text = '1'
            raw_text7 = '/d'
            channel_id = m.chat.id
            b_name = '**Link Input**'
            await editable.delete()

    if thumb.startswith("http"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"

    try:
        if m.document and raw_text == "1":
            batch_message = await bot.send_message(
                chat_id=channel_id,
                text=f"<blockquote><b>🎯Target Batch : {b_name}</b></blockquote>"
            )
            if "/d" not in raw_text7:
                await bot.send_message(
                    chat_id=m.chat.id,
                    text=f"<blockquote><b><i>🎯Target Batch : {b_name}</i></b></blockquote>\n\n🔄 Your Task is under processing, please check your Set Channel📱. Once your task is complete, I will inform you 📩"
                )
                await bot.pin_chat_message(channel_id, batch_message.id)
                pinning_message_id = batch_message.id + 1
                await bot.delete_messages(channel_id, pinning_message_id)
        else:
            if "/d" not in raw_text7:
                await bot.send_message(
                    chat_id=m.chat.id,
                    text=f"<blockquote><b><i>🎯Target Batch : {b_name}</i></b></blockquote>\n\n🔄 Your Task is under processing, please check your Set Channel📱. Once your task is complete, I will inform you 📩"
                )
    except Exception as e:
        await m.reply_text(f"**Fail Reason »**\n<blockquote><i>{e}</i></blockquote>\n\n✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}🌟`")

    failed_count = 0
    count = int(raw_text)
    arg = int(raw_text)
    try:
        for i in range(arg - 1, len(links)):
            if globals.cancel_requested:
                await m.reply_text("🚦**STOPPED**🚦")
                globals.processing_request = False
                globals.cancel_requested = False
                return

            Vxy = (
                links[i][1]
                .replace("file/d/", "uc?export=download&id=")
                .replace("www.youtube-nocookie.com/embed", "youtu.be")
                .replace("?modestbranding=1", "")
                .replace("/view?usp=sharing", "")
            )
            url = "https://" + Vxy
            link0 = "https://" + Vxy

            name1 = (
                links[i][0]
                .replace("(", "[").replace(")", "]").replace("_", "").replace("\t", "")
                .replace(":", "").replace("/", "").replace("+", "").replace("#", "")
                .replace("|", "").replace("@", "").replace("*", "").replace(".", "")
                .replace("https", "").replace("http", "").strip()
            )
            if m.text:
                if "youtu" in url:
                    oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
                    audio_title = requests.get(oembed_url).json().get('title', 'YouTube Video')
                    audio_title = audio_title.replace("_", " ")
                    name = f'{audio_title[:60]}'
                    namef = f'{audio_title[:60]}'
                    name1 = f'{audio_title}'
                else:
                    name = f'{name1[:60]}'
                    namef = f'{name1[:60]}'
            else:
                if endfilename == "/d":
                    name = f'{str(count).zfill(3)}) {name1[:60]}'
                    namef = f'{name1[:60]}'
                else:
                    name = f'{str(count).zfill(3)}) {name1[:60]} {endfilename}'
                    namef = f'{name1[:60]} {endfilename}'

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(
                        url,
                        headers={
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'Accept-Language': 'en-US,en;q=0.9',
                            'Cache-Control': 'no-cache',
                            'Connection': 'keep-alive',
                            'Pragma': 'no-cache',
                            'Referer': 'http://www.visionias.in/',
                            'Sec-Fetch-Dest': 'iframe',
                            'Sec-Fetch-Mode': 'navigate',
                            'Sec-Fetch-Site': 'cross-site',
                            'Upgrade-Insecure-Requests': '1',
                            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
                            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
                            'sec-ch-ua-mobile': '?1',
                            'sec-ch-ua-platform': '"Android"',
                        }
                    ) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist\.m3u8.*?)\""
