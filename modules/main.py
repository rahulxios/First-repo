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
from html_handler import html_handler
from drm_handler import drm_handler
import globals
from authorisation import add_auth_user, list_auth_users, remove_auth_user
from broadcast import broadcast_handler, broadusers_handler
from text_handler import text_to_txt
from youtube_handler import ytm_handler, y2t_handler, getcookies_handler, cookies_handler
from utils import progress_bar
from vars import api_url, api_token, token_cp, adda_token, photologo, photoyt, photocp, photozip
from vars import API_ID, API_HASH, BOT_TOKEN, OWNER, CREDIT, AUTH_USERS, TOTAL_USERS, cookies_file_path
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

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command("start"))
async def start(bot, m: Message):
    user_id = m.chat.id
    if user_id not in TOTAL_USERS:
        TOTAL_USERS.append(user_id)
    user = await bot.get_me()

    mention = user.mention
    caption = f"🌟 Welcome {m.from_user.mention} ! 🌟"
    start_message = await bot.send_photo(
        chat_id=m.chat.id,
        photo="https://i.postimg.cc/FRySPJM0/backiee-330776-landscape.jpg",
        caption=caption
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"Initializing Uploader bot... 🤖\n\n"
        f"Progress: [⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️] 0%\n\n"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"Loading features... ⏳\n\n"
        f"Progress: [🟥🟥🟥⬜️⬜️⬜️⬜️⬜️⬜️⬜️] 25%\n\n"
    )
    
    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"This may take a moment, sit back and relax! 😊\n\n"
        f"Progress: [🟧🟧🟧🟧🟧⬜️⬜️⬜️⬜️⬜️] 50%\n\n"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"Checking subscription status... 🔍\n\n"
        f"Progress: [🟨🟨🟨🟨🟨🟨🟨🟨⬜️⬜️] 75%\n\n"
    )

    await asyncio.sleep(1)
    if m.chat.id in AUTH_USERS:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ Commands", callback_data="cmd_command")],
            [InlineKeyboardButton("💎 Features", callback_data="feat_command"), InlineKeyboardButton("⚙️ Settings", callback_data="setttings")],
            [InlineKeyboardButton("💳 Plans", callback_data="upgrade_command")],
            [InlineKeyboardButton(text="📞 Contact", url=f"tg://openmessage?user_id={OWNER}"), InlineKeyboardButton(text="🛠️ Repo", url="https://github.com/nikhilsainiop/saini-txt-direct")],
        ])
        
        await start_message.edit_text(
            f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
            f"Great! You are a premium member!\n"
            f"Use button : **✨ Commands** to get started 🌟\n\n"
            f"If you face any problem contact -  [{CREDIT}⁬](tg://openmessage?user_id={OWNER})\n", disable_web_page_preview=True, reply_markup=keyboard
        )
    else:
        await asyncio.sleep(2)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ Commands", callback_data="cmd_command")],
            [InlineKeyboardButton("💎 Features", callback_data="feat_command"), InlineKeyboardButton("⚙️ Settings", callback_data="setttings")],
            [InlineKeyboardButton("💳 Plans", callback_data="upgrade_command")],
            [InlineKeyboardButton(text="📞 Contact", url=f"tg://openmessage?user_id={OWNER}"), InlineKeyboardButton(text="🛠️ Repo", url="https://github.com/nikhilsainiop/saini-txt-direct")],
        ])
        await start_message.edit_text(
           f" 🎉 Welcome {m.from_user.first_name} to DRM Bot! 🎉\n\n"
           f"**You are currently using the free version.** 🆓\n\n<blockquote expandable>I'm here to make your life easier by downloading videos from your **.txt** file 📄 and uploading them directly to Telegram!</blockquote>\n\n**Want to get started? Press /id**\n\n💬 Contact : [{CREDIT}⁬](tg://openmessage?user_id={OWNER}) to Get The Subscription 🎫 and unlock the full potential of your new bot! 🔓\n", disable_web_page_preview=True, reply_markup=keyboard
    )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("back_to_main_menu"))
async def back_to_main_menu(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id}) in My uploader bot**"
    keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ Commands", callback_data="cmd_command")],
            [InlineKeyboardButton("💎 Features", callback_data="feat_command"), InlineKeyboardButton("⚙️ Settings", callback_data="setttings")],
            [InlineKeyboardButton("💳 Plans", callback_data="upgrade_command")],
            [InlineKeyboardButton(text="📞 Contact", url=f"tg://openmessage?user_id={OWNER}"), InlineKeyboardButton(text="🛠️ Repo", url="https://github.com/nikhilsainiop/saini-txt-direct")],
        ])
    
    await callback_query.message.edit_media(
      InputMediaPhoto(
        media="https://envs.sh/GVI.jpg",
        caption=caption
      ),
      reply_markup=keyboard
    )
    await callback_query.answer()  

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("cmd_command"))
async def cmd(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id})\nChoose Button to select Commands**"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚻 User", callback_data="user_command"), InlineKeyboardButton("🚹 Owner", callback_data="owner_command")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]
    ])
    await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_00000000fc2461fbbdd6bc500cecbff8_conversation_id6874702c-9760-800e-b0bf-8e0bcf8a3833message_id964012ce-7ef5-4ad4-88e0-1c41ed240c03-1-1.jpg",
      caption=caption
    ),
    reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("user_command"))
async def help_button(client, callback_query):
  user_id = callback_query.from_user.id
  first_name = callback_query.from_user.first_name
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Commands", callback_data="cmd_command")]])
  caption = (
        f"💥 𝐁𝐎𝐓𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒\n"
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n" 
        f"📌 𝗠𝗮𝗶𝗻 𝗙𝗲𝗮𝘁𝘂𝗿𝗲𝘀:\n\n"  
        f"➥ /start – Bot Status Check\n"
        f"➥ /y2t – YouTube → .txt Converter\n"  
        f"➥ /ytm – YouTube → .mp3 downloader\n"  
        f"➥ /t2t – Text → .txt Generator\n"
        f"➥ /t2h – .txt → .html Converter\n" 
        f"➥ /stop – Cancel Running Task\n"
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰ \n" 
        f"⚙️ 𝗧𝗼𝗼𝗹𝘀 & 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀: \n\n" 
        f"➥ /cookies – Update YT Cookies\n" 
        f"➥ /id – Get Chat/User ID\n"  
        f"➥ /info – User Details\n"  
        f"➥ /logs – View Bot Activity\n"
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
        f"💡 𝗡𝗼𝘁𝗲:\n\n"  
        f"• Send any link for auto-extraction\n"
        f"• Send direct .txt file for auto-extraction\n"
        f"• Supports batch processing\n\n"  
        f"╭────────⊰◆⊱────────╮\n"   
        f" ➠ 𝐌𝐚𝐝𝐞 𝐁𝐲 : {CREDIT} 💻\n"
        f"╰────────⊰◆⊱────────╯\n"
  )
    
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_00000000fc2461fbbdd6bc500cecbff8_conversation_id6874702c-9760-800e-b0bf-8e0bcf8a3833message_id964012ce-7ef5-4ad4-88e0-1c41ed240c03-1-1.jpg",
      caption=caption
    ),
    reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("owner_command"))
async def help_button(client, callback_query):
  user_id = callback_query.from_user.id
  first_name = callback_query.from_user.first_name
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Commands", callback_data="cmd_command")]])
  caption = (
        f"👤 𝐁𝐨𝐭 𝐎𝐰𝐧𝐞𝐫 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬\n\n" 
        f"➥ /addauth xxxx – Add User ID\n" 
        f"➥ /rmauth xxxx – Remove User ID\n"  
        f"➥ /users – Total User List\n"  
        f"➥ /broadcast – For Broadcasting\n"  
        f"➥ /broadusers – All Broadcasting Users\n"  
        f"➥ /reset – Reset Bot\n"
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"  
        f"╭────────⊰◆⊱────────╮\n"   
        f" ➠ 𝐌𝐚𝐝𝐞 𝐁𝐲 : {CREDIT} 💻\n"
        f"╰────────⊰◆⊱────────╯\n"
  )
    
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_00000000fc2461fbbdd6bc500cecbff8_conversation_id6874702c-9760-800e-b0bf-8e0bcf8a3833message_id964012ce-7ef5-4ad4-88e0-1c41ed240c03-1-1.jpg",
      caption=caption
    ),
    reply_markup=keyboard
  )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("upgrade_command"))
async def upgrade_button(client, callback_query):
  user_id = callback_query.from_user.id
  first_name = callback_query.from_user.first_name
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]])
  caption = (
           f" 🎉 Welcome [{first_name}](tg://user?id={user_id}) to DRM Bot! 🎉\n\n"
           f"You can have access to download all Non-DRM+AES Encrypted URLs 🔐 including\n\n"
           f"<blockquote>• 📚 Appx Zip+Encrypted Url\n"
           f"• 🎓 Classplus DRM+ NDRM\n"
           f"• 🧑‍🏫 PhysicsWallah DRM\n"
           f"• 📚 CareerWill + PDF\n"
           f"• 🎓 Khan GS\n"
           f"• 🎓 Study Iq DRM\n"
           f"• 🚀 APPX + APPX Enc PDF\n"
           f"• 🎓 Vimeo Protection\n"
           f"• 🎓 Brightcove Protection\n"
           f"• 🎓 Visionias Protection\n"
           f"• 🎓 Zoom Video\n"
           f"• 🎓 Utkarsh Protection(Video + PDF)\n"
           f"• 🎓 All Non DRM+AES Encrypted URLs\n"
           f"• 🎓 MPD URLs if the key is known (e.g., Mpd_url?key=key XX:XX)</blockquote>\n\n"
           f"<b>💵 Monthly Plan: 100 INR</b>\n\n"
           f"If you want to buy membership of the bot, feel free to contact [{CREDIT}](tg://user?id={OWNER})\n"
    )  
    
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://envs.sh/GVI.jpg",
      caption=caption
    ),
    reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("setttings"))
async def settings_button(client, callback_query):
    caption = "✨ <b>My Premium BOT Settings Panel</b> ✨"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Caption Style", callback_data="caption_style_command"), InlineKeyboardButton("🖋️ File Name", callback_data="file_name_command")],
        [InlineKeyboardButton("🌅 Thumbnail", callback_data="thummbnail_command")],
        [InlineKeyboardButton("✍️ Add Credit", callback_data="add_credit_command"), InlineKeyboardButton("🔏 Set Token", callback_data="set_token_command")],
        [InlineKeyboardButton("💧 Watermark", callback_data="wattermark_command")],
        [InlineKeyboardButton("📽️ Video Quality", callback_data="quality_command"), InlineKeyboardButton("🏷️ Topic", callback_data="topic_command")],
        [InlineKeyboardButton("🔄 Reset", callback_data="resset_command")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]
    ])

    await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://envs.sh/GVI.jpg",
      caption=caption
    ),
    reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("thummbnail_command"))
async def cmd(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id})\nChoose Button to set Thumbnail**"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Video", callback_data="viideo_thumbnail_command"), InlineKeyboardButton("📑 PDF", callback_data="pddf_thumbnail_command")],
        [InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]
    ])
    await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_00000000fc2461fbbdd6bc500cecbff8_conversation_id6874702c-9760-800e-b0bf-8e0bcf8a3833message_id964012ce-7ef5-4ad4-88e0-1c41ed240c03-1-1.jpg",
      caption=caption
    ),
    reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("wattermark_command"))
async def cmd(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id})\nChoose Button to set Watermark**"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Video", callback_data="video_watermark_command"), InlineKeyboardButton("📑 PDF", callback_data="pdf_watermark_command")],
        [InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]
    ])
    await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_00000000fc2461fbbdd6bc500cecbff8_conversation_id6874702c-9760-800e-b0bf-8e0bcf8a3833message_id964012ce-7ef5-4ad4-88e0-1c41ed240c03-1-1.jpg",
      caption=caption
    ),
    reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("set_token_command"))
async def cmd(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id})\nChoose Button to set Token**"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Classplus", callback_data="cp_token_command")],
        [InlineKeyboardButton("Physics Wallah", callback_data="pw_token_command"), InlineKeyboardButton("Carrerwill", callback_data="cw_token_command")],
        [InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]
    ])
    await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_00000000fc2461fbbdd6bc500cecbff8_conversation_id6874702c-9760-800e-b0bf-8e0bcf8a3833message_id964012ce-7ef5-4ad4-88e0-1c41ed240c03-1-1.jpg",
      caption=caption
    ),
    reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("caption_style_command"))
async def handle_caption(client, callback_query):
    user_id = callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]])
    editable = await callback_query.message.edit(
        "**Caption Style 1**\n"
        "<blockquote expandable><b>[🎥]Vid Id</b> : {str(count).zfill(3)}\n"
        "**Video Title :** `{name1} [{res}p].{ext}`\n"
        "<blockquote><b>Batch Name :</b> {b_name}</blockquote>\n\n"
        "**Extracted by➤**{CR}</blockquote>\n\n"
        "**Caption Style 2**\n"
        "<blockquote expandable>**——— ✦ {str(count).zfill(3)} ✦ ———**\n\n"
        "🎞️ **Title** : `{name1}`\n"
        "**├── Extention :  {extension}.{ext}**\n"
        "**├── Resolution : [{res}]**\n"
        "📚 **Course : {b_name}**\n\n"
        "🌟 **Extracted By : {credit}**</blockquote>\n\n"
        "**Caption Style 3**\n"
        "<blockquote expandable>**{str(count).zfill(3)}.** {name1} [{res}p].{ext}</blockquote>\n\n"
        "**Send Your Caption Style eg. /cc1 or /cc2 or /cc3**", reply_markup=keyboard)
    input_msg = await bot.listen(editable.chat.id)
    try:
        if input_msg.text.lower() == "/cc1":
            globals.caption = '/cc1'
            await editable.edit(f"✅ Caption Style 1 Updated!", reply_markup=keyboard)
        elif input_msg.text.lower() == "/cc2":
            globals.caption = '/cc2'
            await editable.edit(f"✅ Caption Style 2 Updated!", reply_markup=keyboard)
        else:
            globals.caption = input_msg.text
            await editable.edit(f"✅ Caption Style 3 Updated!", reply_markup=keyboard)
            
    except Exception as e:
        await editable.edit(f"<b>❌ Failed to set Caption Style:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
    finally:
        await input_msg.delete()
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("file_name_command"))
async def handle_caption(client, callback_query):
    user_id = callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]])
    editable = await callback_query.message.edit("**Send End File Name or Send /d**", reply_markup=keyboard)
    input_msg = await bot.listen(editable.chat.id)
    try:
        if input_msg.text.lower() == "/d":
            globals.endfilename = '/d'
            await editable.edit(f"✅ End File Name Disabled !", reply_markup=keyboard)
        else:
            globals.endfilename = input_msg.text
            await editable.edit(f"✅ End File Name `{globals.endfilename}` is enabled!", reply_markup=keyboard)
            
    except Exception as e:
        await editable.edit(f"<b>❌ Failed to set End File Name:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
    finally:
        await input_msg.delete()
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("viideo_thumbnail_command"))
async def video_thumbnail(client, callback_query):
    user_id = callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="thumm
