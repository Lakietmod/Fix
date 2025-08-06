import os
import io
import time
import json
import math
import queue
from colorama import Fore, Back, Style
import random
import logging
from queue import Queue
import tempfile
import threading
import subprocess
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import requests
import pytz
from tempfile import NamedTemporaryFile
import emoji
from io import BytesIO
import glob
import re
import colorsys

# Import các module chức năng
from modules.group.pro_group import handle_group_command
from PIL import Image, ImageDraw, ImageOps, ImageFont, ImageFilter, ImageEnhance
from bs4 import BeautifulSoup
from colorama import Style, init
import pyfiglet
# FIX: Added specific imports for autosend handlers
from modules.func_autosend.pro_autosend import (
    start_autosend_thread, 
    handle_autosend_command, 
    handle_autosend_on, 
    handle_autosend_off, 
    get_autosend_status, 
    list_autosend_groups
)
from zlapi import ZaloAPI
from zlapi.models import Message, ThreadType, Mention, GroupEventType
from core.bot_sys import *

# Toàn bộ import module lệnh của bạn
from modules.ff.pro_ff import handle_ff_command
from modules.rao.pro_rao import start_rao_handle
from modules.creat_menu.pro_ip import handle_ip_commands
from modules.ff.pro_ping import handle_ping_command
from modules.rank.pro_rank import handle_rank_command
from modules.mail10p.pro_mail10p import handle_mail10p_command
from modules.qrcode.pro_qrcode import handle_qrcode_command
from modules.qrcode.pro_detail import handle_detail_command
from modules.qrcode.pro_scanqr import handle_scanqr_command
from modules.qrcode.pro_groupinfo import handle_groupinfo_command
from modules.qrcode.pro_cardinfo import handle_cardinfo_command
from modules.qrcode.pro_duyetmem import handle_duyetmem_command
from modules.vdtiktok.pro_vdtiktok import handle_vdtiktok_command
from modules.info.pro_info import handle_info_command
from modules.img.pro_img import handle_img_command
from modules.chiase.pro_chiase import handle_chiase_command
from modules.func_spaman.pro_spaman import handle_spaman_command
from modules.func_tdm.pro_tdm import handle_tdm_command
from modules.voice.pro_voice import handle_voice_command
from modules.ngl.pro_ngl import handle_ngl_command
from modules.qrbank.pro_qrbank import handle_qrbank_command
from modules.ff.pro_spamff import handle_kb_command
from modules.save.pro_save import handle_save_command
from modules.attack.pro_attack import handle_attack_command
from modules.stkxp.pro_stkxp import handle_stkxp_command
from modules.reghotmail.pro_reghotmail import handle_reghotmail_command
from modules.doff.pro_doff import handle_doff_command
from modules.AI_GEMINI.pro_gemini import handle_chat_command as handle_chat_ai
from modules.AI_GEMINI.gemini_pro import handle_chat_command as handle_as_ai
from modules.anhgai.pro_anhgai import handle_anhgai_command
from modules.cauthinh.pro_thinh import handle_tha_thinh_command
from modules.creat_menu.menu_or import handle_menu_or_commands
from modules.creat_menu.menu_zl import handle_menu_zl_command
from modules.creat_menu.pro_hiden import handle_hiden_commands
from modules.creat_menu.pro_menu import handle_menu_commands
from modules.dhbc.pro_dhbc import handle_dhbc_command
from modules.func_allan.pro_allan import command_allan_for_link, command__allan_cd
from modules.func_disbox.pro_disbox import handle_disbox
from modules.func_friend.pro_friend import addallfriongr, addfrito, blockto, removefrito, unblockto
from modules.func_giavang.pro_giavang import handle_gia_vang_command
from modules.func_kickall.pro_kickall import kick_member_group
from modules.func_leave.pro_leave import handle_leave_group_command
from modules.func_make.make import handle_make_command
from modules.func_meme.pro_meme import meme
from modules.func_mst.mst import mst
from modules.func_news.pro_news import news
from modules.func_phatnguoi.pro_phatnguoi import phatnguoi
from modules.func_pin.pro_pin import handle_pro_pin
from modules.func_pixi.pro_pixi import pixitimkiem
from modules.func_share.pro_share import handle_share_command
from modules.func_spam_call.pro_spamcall import handle_spamcall_command
from modules.func_spamsms.pro_spamsms import handle_sms_command
from modules.func_src.pro_src import src
from modules.func_stk.pro_stk import handle_stk_command
from modules.func_tygia.pro_tygia import handle_hoan_doi_command
from modules.func_war.allwar import handle_allwar_command
from modules.get_link.pro_getlink import handle_getlink_command
from modules.get_voice.pro_getvoice import handle_getvoice_command
from modules.join_gr.join import handle_join_command
from modules.join_gr.join1 import handle_join1_command
from modules.nhac_scl.pro_nhac import handle_nhac_command
from modules.taixiu.pro_taixiu import handle_tx_command
from modules.text.pro_text import handle_create_image_command
from modules.thue_bot.pro_thue_bot import handle_thuebot_command
from modules.translate.pro_dich import handle_translate_command
from modules.vdgai.pro_vdgai import handle_vdgai_command
from modules.weather.pro_weather import handle_weather_command
import asyncio
import string # FIX: Added missing import

current_word = None; wrong_attempts = 0; correct_attempts = 0; timeout_thread = None; timeout_duration = 30; current_player = None; used_words = set(); game_active = False; leaderboard = {}; leaderboard_file = "leaderboard.json"; words = []
user_selection_data = {}; session = requests.Session()

def load_words():
    global words
    try:
        with open('words.txt', 'r', encoding='utf-8') as file:
            words = [line.strip() for line in file if line.strip()]
        return words
    except FileNotFoundError:
        words = []
        return words

words = load_words()

def load_leaderboard(uid):
    global leaderboard
    data_file_path = f"{uid}_{leaderboard_file}"
    try:
        with open(data_file_path, 'r', encoding='utf-8') as f:
            leaderboard = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard = {}

def save_leaderboard(uid):
    data_file_path = f"{uid}_{leaderboard_file}"
    try:
        with open(data_file_path, 'w', encoding='utf-8') as f:
            json.dump(leaderboard, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving leaderboard: {e}")

def save_word_to_file(word):
    try:
        with open('words.txt', 'a', encoding='utf-8') as file:
            file.write(f"\n{word}")
        if word not in words:
            words.append(word)
    except Exception as e:
        print(f"Error saving word: {e}")

def remove_word_from_file(word):
    global words
    if word in words:
        try:
            with open('words.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
            with open('words.txt', 'w', encoding='utf-8') as file:
                for line in lines:
                    if line.strip() != word:
                        file.write(line)
            words = load_words()
            return True
        except Exception as e:
            print(f"Error removing word: {e}")
    return False

def reset_game():
    global current_word, wrong_attempts, correct_attempts, timeout_thread, current_player, used_words, game_active
    if timeout_thread and timeout_thread.is_alive():
        timeout_thread.cancel()
    
    current_word = None
    wrong_attempts = 0
    correct_attempts = 0
    timeout_thread = None
    current_player = None
    used_words.clear()
    game_active = False

def handle_undo_message(bot, message_object, thread_id, thread_type, author_id):
    settings = read_settings(bot.uid)
    undo_enabled = settings.get('undo_enabled', {}).get(thread_id, True)

    if not undo_enabled:
        return

    if message_object.msgType != 'chat.undo':
        return

    cli_msg_id = str(message_object.content.get('cliMsgId', ''))
    if not cli_msg_id:
        return

    try:
        with open('undo.json', 'r', encoding='utf-8') as f:
            undo_data = json.load(f)
    except:
        undo_data = []

    data = next((msg for msg in undo_data if msg.get('cliMsgId') == cli_msg_id), None)
    if not data:
        return

    uid_from = message_object.uidFrom
    mention = Mention(uid_from, offset=0, length=1)
    formatted_time = time.strftime("%H:%M:%S %d/%m/%Y", time.localtime())
    content = data.get("content", {})
    msg_type = data.get("msgType", "")

    if msg_type == "chat.text":
        text = content.get("text", "")
        bot.replyMessage(
            Message(text=f"@ Vua thu hoi tin nhan:\n{text}\n🕒 {formatted_time}", mention=mention),
            message_object, thread_id, thread_type
        )

    elif msg_type == "chat.image" and "href" in content:
        bot.sendRemoteImage(content["href"], thumbnailUrl=content.get("thumb"), thread_id=thread_id, thread_type=thread_type)
        bot.replyMessage(
            Message(text=f"@ Vua thu hoi anh\n🕒 {formatted_time}", mention=mention),
            message_object, thread_id, thread_type
        )

    elif msg_type == "chat.video" and "href" in content:
        params = json.loads(content.get("params", "{}"))
        bot.sendRemoteVideo(
            videoUrl=content["href"],
            thumbnailUrl=content.get("thumb"),
            duration=params.get("duration", ""),
            width=params.get("video_width", ""),
            height=params.get("video_height", ""),
            thread_id=thread_id, thread_type=thread_type
        )
        bot.replyMessage(
            Message(text=f"@ Vua thu hoi video\n🕒 {formatted_time}", mention=mention),
            message_object, thread_id, thread_type
        )

    elif msg_type == "chat.voice" and "href" in content:
        bot.sendRemoteVoice(content["href"], thread_id=thread_id, thread_type=thread_type)
        bot.replyMessage(
            Message(text=f"@ Vua thu hoi voice\n🕒 {formatted_time}", mention=mention),
            message_object, thread_id, thread_type
        )

    elif msg_type == "chat.file" and "href" in content:
        file_name = content.get("fileName", "file")
        bot.sendRemoteFile(content["href"], filename=file_name, thread_id=thread_id, thread_type=thread_type)
        bot.replyMessage(
            Message(text=f"@ Vua thu hoi file: {file_name}\n🕒 {formatted_time}", mention=mention),
            message_object, thread_id, thread_type
        )

    elif msg_type == "chat.sticker":
        catId = data.get('catId')
        msgId = data.get('id')
        bot.sendSticker(msgId, catId, thread_id, thread_type)
        bot.replyMessage(
            Message(text=f"@ Vua thu hoi sticker\n🕒 {formatted_time}", mention=mention),
            message_object, thread_id, thread_type
        )

    else:
        bot.replyMessage(
            Message(text=f"@ Vua thu hoi mot loai tin nhan khong xac đinh\n🕒 {formatted_time}", mention=mention),
            message_object, thread_id, thread_type
        )

def handle_timeout(bot, message_object, thread_id, thread_type):
    global game_active
    if not game_active:
        return
    bot.sendReaction(message_object, "❌", thread_id, thread_type)
    bot.replyMessage(Message(text="➜ ❌ Ban đa het thoi gian tra loi! Tro choi ket thuc."), 
                    message_object, thread_id=thread_id, thread_type=thread_type)
    reset_game()

def start_timeout(bot, message_object, thread_id, thread_type):
    global timeout_thread, game_active
    if timeout_thread and timeout_thread.is_alive():
        timeout_thread.cancel()
    game_active = True
    timeout_thread = threading.Timer(timeout_duration, lambda: handle_timeout(bot, message_object, thread_id, thread_type))
    timeout_thread.start()

def fetch_webpage(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching webpage: {str(e)}")
        return None

def get_wikipedia_info(search_term):
    base_url = "https://vi.wikipedia.org/wiki/"
    search_url = base_url + search_term.replace(" ", "_")
    
    page_content = fetch_webpage(search_url)
    if not page_content:
        return {"Loi": "Khong the lay thong tin tu Wikipedia."}

    soup = BeautifulSoup(page_content, "html.parser")
    image_url = "Khong tim thay anh"
    infobox = soup.find("table", {"class": "infobox"})
    
    if infobox:
        image_tag = infobox.find("img")
        if image_tag and "src" in image_tag.attrs:
            image_url = "https:" + image_tag["src"]

    info = {}
    if infobox:
        rows = infobox.find_all("tr")
        for row in rows:
            header = row.find("th")
            data = row.find("td")
            if header and data:
                links = data.find_all("a", href=True)
                if links:
                    info[header.text.strip()] = [f"https://vi.wikipedia.org{link['href']}" for link in links]
                else:
                    info[header.text.strip()] = data.text.strip()

    paragraphs = soup.find_all("p")
    content = "\n\n".join([p.text.strip() for p in paragraphs[:2] if p.text.strip()])

    return {
        "Hinh anh": image_url,
        "Thong tin": info,
        "Mo ta": content
    }

def check_word(player_word, last_part):
    if not player_word or not last_part:
        return False
    if player_word in words and player_word.split()[0] == last_part:
        return True
    wiki_info = get_wikipedia_info(player_word)
    if "Loi" not in wiki_info and wiki_info["Mo ta"]:
        if player_word.split()[0] == last_part:
            save_word_to_file(player_word)
            return True
    return False

def update_leaderboard(bot, user_id, user_name, words_used):
    global leaderboard
    load_leaderboard(bot.uid)
    
    if user_id not in leaderboard:
        leaderboard[user_id] = {"name": user_name, "score": 0, "correct_answers": 0}
    
    leaderboard[user_id]["score"] += words_used
    leaderboard[user_id]["correct_answers"] += words_used
    leaderboard[user_id]["name"] = user_name
    
    save_leaderboard(bot.uid)
    return leaderboard[user_id]

def get_user_rank(bot, user_id):
    load_leaderboard(bot.uid)
    if not leaderboard or user_id not in leaderboard:
        return None
    
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]["score"], reverse=True)
    for rank, (uid, _) in enumerate(sorted_leaderboard, 1):
        if uid == user_id:
            return rank
    return None

def handle_victory(bot, message_object, author_id, thread_id, thread_type):
    user_name = get_user_name_by_id(bot, author_id)
    words_used = correct_attempts
    user_data = update_leaderboard(bot, author_id, user_name, words_used)
    user_rank = get_user_rank(bot, author_id)
    
    message = f"🚦 {user_name}\n"
    message += "🎈 Xin chuc mung ban đa chien thang!\n"
    message += f"💯 Khich le: +{words_used} 🍫\n"
    message += f"🏅 Thanh tich: {words_used} tu\n"
    
    if user_rank and user_rank <= 10:
        medal_emojis = {1: "🥇", 2: "🥈", 3: "🥉"}
        medal = medal_emojis.get(user_rank, f"{user_rank}")
        message += f"🎉 Ban đa lap ky luc moi đung {medal} trong BXH!"
    
    bot.replyMessage(Message(text=message, mention=Mention(author_id, length=len(user_name), offset=3)), 
                    message_object, thread_id=thread_id, thread_type=thread_type)
    reset_game()

def handle_defeat(bot, message_object, author_id, thread_id, thread_type):
    user_name = get_user_name_by_id(bot, author_id)
    correct_answers = correct_attempts
    
    if correct_answers > 0:
        user_data = update_leaderboard(bot, author_id, user_name, correct_answers)
        user_rank = get_user_rank(bot, author_id)
    else:
        user_rank = None
    
    message = f"🚦 {user_name}\n"
    message += "😢 Ban đa sai qua nhieu lan. Thua roi!\n"
    message += f"🎖️ Thanh tich: {correct_answers} tu\n"
    
    if user_rank and user_rank <= 10:
        medal_emojis = {1: "🥇", 2: "🥈", 3: "🥉"}
        medal = medal_emojis.get(user_rank, f"{user_rank}")
        message += f"🎉 Ban đa lap ky luc moi đung {medal} trong BXH!"
    
    bot.replyMessage(Message(text=message, mention=Mention(author_id, length=len(user_name), offset=3)), 
                    message_object, thread_id=thread_id, thread_type=thread_type)
    reset_game()

def handle_wrong_attempt(bot, message_object, thread_id, thread_type):
    global wrong_attempts
    wrong_attempts += 1
    for _ in range(wrong_attempts):
        bot.sendReaction(message_object, "❌", thread_id, thread_type)
    if wrong_attempts >= 3:
        handle_defeat(bot, message_object, current_player, thread_id, thread_type)
        return True
    return False

def get_leaderboard_display(bot):
    load_leaderboard(bot.uid)
    
    if not leaderboard:
        return "🚦 BXH 🏅 Top Game Noi Tu:\n➜ Chua co du lieu xep hang!"
    
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]["score"], reverse=True)
    
    display_text = "🚦 BXH 🏅 Top 10 Game Noi Tu:\n"
    medals = ["🥇", "🥈", "🥉"] + [f"{i}" for i in range(4, 11)]
    
    for i, (user_id, data) in enumerate(sorted_leaderboard[:10], 1):
        medal = medals[i-1]
        name = data["name"]
        score = data["score"]
        display_text += f"➜ {medal} {name} - {score} tu\n"
    
    return display_text.strip()

def nt_bxh(bot, message_object, thread_id, thread_type):
    display_text = get_leaderboard_display(bot)
    bot.replyMessage(Message(text=display_text), 
                    message_object, thread_id=thread_id, thread_type=thread_type)

def process_valid_word(bot, message_object, author_id, thread_id, thread_type, player_word):
    global current_word, wrong_attempts, correct_attempts, used_words
    player_last_part = player_word.split()[-1]
    used_words.add(player_word)
    
    next_word = next(
        (word for word in words 
         if word.split()[0] == player_last_part
         and word not in used_words 
         and len(word.split()) == 2),
        None
    )
    
    if next_word:
        current_word = next_word
        used_words.add(next_word)
        wrong_attempts = 0
        correct_attempts += 1
        
        for _ in range(correct_attempts):
            bot.sendReaction(message_object, "✅", thread_id, thread_type)
        
        response = f"{get_user_name_by_id(bot, author_id)} {next_word}"
        start_timeout(bot, message_object, thread_id, thread_type)
        bot.replyMessage(Message(text=response, mention=Mention(author_id, length=len(f"{get_user_name_by_id(bot, author_id)}"), offset=0)), 
                       message_object, thread_id=thread_id, thread_type=thread_type)
    else:
        handle_victory(bot, message_object, author_id, thread_id, thread_type)

def start_new_game(bot, message_object, author_id, thread_id, thread_type):
    global current_word, current_player, used_words, game_active
    if not words:
        bot.replyMessage(Message(text="➜ ❌ File words.txt khong chua tu nao!"), 
                       message_object, thread_id=thread_id, thread_type=thread_type)
        return
    current_word = random.choice(words)
    used_words.add(current_word)
    current_player = author_id
    game_active = True
    response = f"➜ Tu khoi đau: '{current_word}'\n"
    start_timeout(bot, message_object, thread_id, thread_type)
    bot.replyMessage(Message(text=response), message_object,
                   thread_id=thread_id, thread_type=thread_type)

def nt_check(bot, message_object, author_id, thread_id, thread_type, message):
    parts = message.strip().split()
    if len(parts) < 3 or parts[1].lower() != "check":
        bot.replyMessage(Message(text="➜ Cu phap khong đung! Su dung: /nt check <tu>"), 
                        message_object, thread_id=thread_id, thread_type=thread_type)
        return
    
    search_term = " ".join(parts[2:])
    wiki_info = get_wikipedia_info(search_term)
    
    if "Loi" in wiki_info or not wiki_info["Mo ta"]:
        response = f"➜ Tu '{search_term}' khong đuoc tim thay tren Wikipedia hoac khong co nghia ro rang."
    else:
        response = (
            f"➜ Ket qua cho '{search_term}':\n"
            f"📝 Mo ta: {wiki_info['Mo ta'][:200]}...\n"
            f"🖼️ Hinh anh: {wiki_info['Hinh anh']}\n"
            f"🔗 Link: https://vi.wikipedia.org/wiki/{search_term.replace(' ', '_')}"
        )
        if search_term not in words:
            save_word_to_file(search_term)
            response += f"\n✅ Đa them '{search_term}' vao danh sach tu vung!"

    bot.replyMessage(Message(text=response), message_object, 
                    thread_id=thread_id, thread_type=thread_type)

def nt_add(bot, message_object, author_id, thread_id, thread_type, message):
    parts = message.strip().split()
    if len(parts) < 3 or parts[1].lower() != "add":
        bot.replyMessage(Message(text="➜ Cu phap khong đung! Su dung: /nt add <tu>"), 
                        message_object, thread_id=thread_id, thread_type=thread_type)
        return
    
    new_word = " ".join(parts[2:])
    if new_word in words:
        response = f"🚦 {get_user_name_by_id(bot, author_id)} Tu '{new_word}' đa ton tai trong tu đien! ⚠️"
    else:
        save_word_to_file(new_word)
        response = f"🚦 {get_user_name_by_id(bot, author_id)} Đa them tu '{new_word}' vao tu đien thanh cong! ✅"
    
    bot.replyMessage(Message(text=response, mention=Mention(author_id, length=len(f"{get_user_name_by_id(bot, author_id)}"), offset=3)), 
                    message_object, thread_id=thread_id, thread_type=thread_type)

def nt_del(bot, message_object, author_id, thread_id, thread_type, message):
    parts = message.strip().split()
    if len(parts) < 3 or parts[1].lower() != "del":
        bot.replyMessage(Message(text="➜ Cu phap khong đung! Su dung: /nt del <tu>"), 
                        message_object, thread_id=thread_id, thread_type=thread_type)
        return
    
    word_to_remove = " ".join(parts[2:])
    if remove_word_from_file(word_to_remove):
        response = f"🚦 Đa xoa tu '{word_to_remove}' khoi tu đien ✅"
    else:
        response = f"➜ Tu '{word_to_remove}' khong co trong tu đien 🤧"
    
    bot.replyMessage(Message(text=response), message_object, 
                    thread_id=thread_id, thread_type=thread_type)

def nt_go(bot, message_object, author_id, thread_id, thread_type, message):
    global current_word, wrong_attempts, current_player, used_words, game_active
    message_text = message.strip()
    
    # FIX: Use getattr to prevent crash if bot.prefix is not set
    prefix = getattr(bot, 'prefix', '/')

    if message_text.startswith(f"{prefix}nt bxh"):
        return nt_bxh(bot, message_object, thread_id, thread_type)
    elif message_text.startswith(f"{prefix}nt check"):
        return nt_check(bot, message_object, author_id, thread_id, thread_type, message)
    elif message_text.startswith(f"{prefix}nt add"):
        return nt_add(bot, message_object, author_id, thread_id, thread_type, message)
    elif message_text.startswith(f"{prefix}nt del"):
        return nt_del(bot, message_object, author_id, thread_id, thread_type, message)
    elif message_text == f"{prefix}nt":
        return show_menu(bot, message_object, message, author_id, thread_id, thread_type)
    
    if not game_active or current_player is None:
        return start_new_game(bot, message_object, author_id, thread_id, thread_type)
    
    if game_active and author_id != current_player:
        return

    if author_id != current_player:
        return
    
    player_word = message_text.replace(f"{prefix}nt", "").strip()
    if len(player_word.split()) != 2:
        if handle_wrong_attempt(bot, message_object, thread_id, thread_type):
            return
        start_timeout(bot, message_object, thread_id, thread_type)
        return
    
    if player_word in used_words:
        if handle_wrong_attempt(bot, message_object, thread_id, thread_type):
            return
        start_timeout(bot, message_object, thread_id, thread_type)
        return
    
    last_part = current_word.split()[-1]
    if not check_word(player_word, last_part):
        if handle_wrong_attempt(bot, message_object, thread_id, thread_type):
            return
        start_timeout(bot, message_object, thread_id, thread_type)
        return
    
    if timeout_thread and timeout_thread.is_alive():
        timeout_thread.cancel()
    
    process_valid_word(bot, message_object, author_id, thread_id, thread_type, player_word)

def show_menu(bot, message_object, message, author_id, thread_id, thread_type):
    content = message.strip().split()
    message_text = message.strip()
    # FIX: Use getattr to prevent crash if bot.prefix is not set
    prefix = getattr(bot, 'prefix', '/')
    if message_text.startswith(f"{prefix}nt"):
        if len(content) == 1:
            menu_nt = {
                f"{prefix}nt go": "🔠 Bat dau game",
                f"{prefix}nt check [tu vung]": "✅ Kiem tra y nghia tu vung",
                f"{prefix}nt bxh": "🏆 Top 10 BXH",
                f"{prefix}nt add [tu vung]": "✚ Them tu vung (BMT)",
                f"{prefix}nt del [tu vung]": "🗑️ Xoa tu vung"
            }
            temp_image_path, menu_message = create_menu_nt_image(menu_nt, bot, author_id)
            bot.sendLocalImage(
                temp_image_path, thread_id=thread_id, thread_type=thread_type,
                message=Message(text=menu_message), height=500, width=1280
            )
            os.remove(temp_image_path)
            return

def create_gradient_colors(num_colors: int) -> List[tuple[int, int, int]]:
    return [(random.randint(80, 220), random.randint(80, 220), random.randint(80, 220)) 
            for _ in range(num_colors)]

def interpolate_colors(colors: List[tuple[int, int, int]], text_length: int, change_every: int) -> List[tuple[int, int, int]]:
    gradient = []
    num_segments = len(colors) - 1
    steps_per_segment = max((text_length // change_every) + 1, 1)

    for i in range(num_segments):
        for j in range(steps_per_segment):
            if len(gradient) < text_length:
                ratio = j / steps_per_segment
                interpolated_color = (
                    int(colors[i][0] * (1 - ratio) + colors[i + 1][0] * ratio),
                    int(colors[i][1] * (1 - ratio) + colors[i + 1][1] * ratio),
                    int(colors[i][2] * (1 - ratio) + colors[i + 1][2] * ratio)
                )
                gradient.append(interpolated_color)

    while len(gradient) < text_length:
        gradient.append(colors[-1])
    return gradient[:text_length]

def is_emoji(character: str) -> bool:
    return character in emoji.EMOJI_DATA

def draw_text_with_emoji(draw: ImageDraw.Draw, text: str, position: tuple[int, int],
                        font: ImageFont.FreeTypeFont, emoji_font: ImageFont.FreeTypeFont,
                        gradient_colors: List[tuple[int, int, int]]) -> int:
    current_x = position[0]
    y = position[1]
    gradient = interpolate_colors(gradient_colors, len(text), 1)
    
    for i, char in enumerate(text):
        try:
            selected_font = emoji_font if is_emoji(char) else font
            font_size = selected_font.size
            offset_y = y - (font_size // 4) if is_emoji(char) else y
            
            draw.text((current_x, offset_y), char, 
                     fill=tuple(gradient[i]), 
                     font=selected_font)
            
            text_bbox = draw.textbbox((current_x, offset_y), char, font=selected_font)
            text_width = text_bbox[2] - text_bbox[0]
            current_x += text_width + (2 if is_emoji(char) else 0)
            
        except Exception as e:
            print(f"Loi khi ve ky tu '{char}': {e}")
            continue
    
    return current_x

def create_menu_nt_image(command_names, bot, author_id, nt_status=True):
    # FIX: Use getattr to prevent crash
    prefix = getattr(bot, 'prefix', '/')
    avatar_url = bot.fetchUserInfo(author_id).changed_profiles.get(author_id).avatar
    current_page_commands = list(command_names.items())
    numbered_commands = [f"{name}: {desc}" for name, desc in current_page_commands]
    menu_message = f"{get_user_name_by_id(bot, author_id)}\n" + "\n".join(numbered_commands)

    background_dir = "background"
    background_path = random.choice([f for f in os.listdir(background_dir) 
                                   if f.endswith(('.png', '.jpg'))])
    image = Image.open(f"background/" + background_path).convert("RGBA").resize((1280, 500))
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    rect_x0, rect_y0, rect_x1, rect_y1 = (1280 - 1100) // 2, (500 - 300) // 2, \
                                        (1280 - 1100) // 2 + 1100, (500 - 300) // 2 + 300
    draw.rounded_rectangle([rect_x0, rect_y0, rect_x1, rect_y1], radius=50, 
                         fill=(255, 255, 255, 200))

    if avatar_url:
        try:
            avatar_image = Image.open(BytesIO(requests.get(avatar_url).content)).convert("RGBA").resize((100, 100))
            gradient_size = 110
            gradient_colors = create_gradient_colors(7)
            gradient_overlay = Image.new("RGBA", (gradient_size, gradient_size), (0, 0, 0, 0))
            gradient_draw = ImageDraw.Draw(gradient_overlay)
            
            for i, color in enumerate(gradient_colors):
                gradient_draw.ellipse((i, i, gradient_size - i, gradient_size - i), 
                                    outline=color, width=1)
            
            mask = Image.new("L", avatar_image.size, 0)
            ImageDraw.Draw(mask).ellipse((0, 0, 100, 100), fill=255)
            gradient_overlay.paste(avatar_image, (5, 5), mask)
            overlay.paste(gradient_overlay, (rect_x0 + 20, rect_y0 + 100), gradient_overlay)
        except Exception as e:
            print(f"Loi khi xu ly avatar: {e}")

    text_hi = f"Hi, {get_user_name_by_id(bot, author_id)}"
    text_welcome = f"🎊 Chao mung đen voi menu 🔠 game noi tu"
    text_nt_status = f"{prefix}nt on/off: bat/tat tinh nang"
    text_bot_ready = f"♥️ bot san sang phuc vu"
    text_bot_info = f"🤖 Bot: {get_user_name_by_id(bot, bot.uid)} 💻 version 2.0 🗓️ update 08-01-24"

    font_path = "arial unicode ms.otf"
    emoji_font_path = "NotoEmoji-Bold.ttf"
    
    font_hi = ImageFont.truetype(font_path, size=50) if os.path.exists(font_path) else ImageFont.load_default()
    font_welcome = ImageFont.truetype(font_path, size=35) if os.path.exists(font_path) else ImageFont.load_default()
    font_nt = ImageFont.truetype(font_path, size=40) if os.path.exists(font_path) else ImageFont.load_default()
    emoji_font = ImageFont.truetype(emoji_font_path, size=35) if os.path.exists(emoji_font_path) else ImageFont.load_default()

    total_height = 300
    line_spacing = total_height // 5
    center_x = 1280 // 2

    y_pos = rect_y0 + 10
    draw_text_with_emoji(draw, text_hi, (center_x - 200, y_pos),
                        font_hi, emoji_font, create_gradient_colors(5))
    
    y_pos += line_spacing
    draw_text_with_emoji(draw, text_welcome, (center_x - 370, y_pos), 
                        font_welcome, emoji_font, create_gradient_colors(5))
    
    y_pos += line_spacing
    draw_text_with_emoji(draw, text_nt_status, (center_x - 250, y_pos), 
                        font_nt, emoji_font, create_gradient_colors(5))
    
    y_pos += line_spacing
    draw_text_with_emoji(draw, text_bot_ready, (center_x - 250, y_pos), 
                        font_welcome, emoji_font, create_gradient_colors(5))
    
    y_pos += line_spacing - 10
    draw_text_with_emoji(draw, text_bot_info, (center_x - 460, y_pos), 
                        font_welcome, emoji_font, create_gradient_colors(7))

    final_image = Image.alpha_composite(image, overlay)
    temp_image_path = "nt_menu.png"
    final_image.save(temp_image_path)
    
    return temp_image_path, menu_message

user_selection_data = {}
session = requests.Session()
BACKGROUND_PATH = "background/"
CACHE_PATH = "modules/cache/"
OUTPUT_IMAGE_PATH = os.path.join(CACHE_PATH, "donghua.png")

def get_dominant_color(image_path):
    try:
        if not os.path.exists(image_path):
            print(f"File anh khong ton tai: {image_path}")
            return (0, 0, 0)

        img = Image.open(image_path).convert("RGB")
        img = img.resize((150, 150), Image.Resampling.LANCZOS)
        pixels = img.getdata()

        if not pixels:
            print(f"Khong the lay du lieu pixel tu anh: {image_path}")
            return (0, 0, 0)

        r, g, b = 0, 0, 0
        for pixel in pixels:
            r += pixel[0]
            g += pixel[1]
            b += pixel[2]
        total = len(pixels)
        if total == 0:
            return (0, 0, 0)
        r, g, b = r // total, g // total, b // total
        return (r, g, b)

    except Exception as e:
        print(f"Loi khi phan tich mau noi bat: {e}")
        return (0, 0, 0)

def get_contrasting_color(base_color, alpha=255):
    r, g, b = base_color[:3]
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return (255, 255, 255, alpha) if luminance < 0.5 else (0, 0, 0, alpha)

def random_contrast_color(base_color):
    r, g, b, _ = base_color
    box_luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    
    if box_luminance > 0.5:
        r = random.randint(0, 50)
        g = random.randint(0, 50)
        b = random.randint(0, 50)
    else:
        r = random.randint(200, 255)
        g = random.randint(200, 255)
        b = random.randint(200, 255)
    
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    s = min(1.0, s + 0.9)
    v = min(1.0, v + 0.7)
    
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    
    text_luminance = (0.299 * r + 0.587 * g + 0.114 * b)
    if abs(text_luminance - box_luminance) < 0.3:
        if box_luminance > 0.5:
            r, g, b = colorsys.hsv_to_rgb(h, s, min(1.0, v * 0.4))
        else:
            r, g, b = colorsys.hsv_to_rgb(h, s, min(1.0, v * 1.7))
    
    return (int(r * 255), int(g * 255), int(b * 255), 255)

def download_avatar(avatar_url, save_path=os.path.join(CACHE_PATH, "user_avatar.png")):
    if not avatar_url:
        return None
    try:
        resp = requests.get(avatar_url, stream=True, timeout=5)
        if resp.status_code == 200:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)
            return save_path
    except Exception as e:
        print(f"❌ Loi tai avatar: {e}")
    return None

def generate_menu_image(bot, author_id, thread_id, thread_type):
    images = glob.glob(os.path.join(BACKGROUND_PATH, "*.jpg")) + \
             glob.glob(os.path.join(BACKGROUND_PATH, "*.png")) + \
             glob.glob(os.path.join(BACKGROUND_PATH, "*.jpeg"))
    if not images:
        print("❌ Khong tim thay anh trong thu muc background/")
        return None

    image_path = random.choice(images)

    try:
        size = (1920, 600)
        final_size = (1280, 380)
        bg_image = Image.open(image_path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
        bg_image = bg_image.filter(ImageFilter.GaussianBlur(radius=7))
        overlay = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        dominant_color = get_dominant_color(image_path)
        r, g, b = dominant_color
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

        box_colors = [
            (255, 20, 147, 90),
            (128, 0, 128, 90),
            (0, 100, 0, 90),
            (0, 0, 139, 90),
            (184, 134, 11, 90),
            (138, 3, 3, 90),
            (0, 0, 0, 90)
        ]

        box_color = random.choice(box_colors)

        box_x1, box_y1 = 90, 60
        box_x2, box_y2 = size[0] - 90, size[1] - 60
        draw.rounded_rectangle([(box_x1, box_y1), (box_x2, box_y2)], radius=75, fill=box_color)

        font_arial_path = "arial unicode ms.otf"
        font_emoji_path = "emoji.ttf"
        
        try:
            font_text_large = ImageFont.truetype(font_arial_path, size=76)
            font_text_big = ImageFont.truetype(font_arial_path, size=68)
            font_text_small = ImageFont.truetype(font_arial_path, size=64)
            font_text_bot = ImageFont.truetype(font_arial_path, size=58)
            font_time = ImageFont.truetype(font_arial_path, size=56)
            font_icon = ImageFont.truetype(font_emoji_path, size=60)
            font_icon_large = ImageFont.truetype(font_emoji_path, size=175)
            font_name = ImageFont.truetype(font_emoji_path, size=60)
        except Exception as e:
            print(f"❌ Loi tai font: {e}")
            font_text_large = ImageFont.load_default(size=76)
            font_text_big = ImageFont.load_default(size=68)
            font_text_small = ImageFont.load_default(size=64)
            font_text_bot = ImageFont.load_default(size=58)
            font_time = ImageFont.load_default(size=56)
            font_icon = ImageFont.load_default(size=60)
            font_icon_large = ImageFont.load_default(size=175)
            font_name = ImageFont.load_default(size=60)

        def draw_text_with_shadow(draw, position, text, font, fill, shadow_color=(0, 0, 0, 250), shadow_offset=(2, 2)):
            x, y = position
            draw.text((x + shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=shadow_color)
            draw.text((x, y), text, font=font, fill=fill)

        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        vietnam_now = datetime.now(vietnam_tz)
        hour = vietnam_now.hour
        formatted_time = vietnam_now.strftime("%H:%M")
        time_icon = "🌤️" if 6 <= hour < 18 else "🌙"
        time_text = f" {formatted_time}"
        time_x = box_x2 - 250
        time_y = box_y1 + 10
        
        box_rgb = box_color[:3]
        box_luminance = (0.299 * box_rgb[0] + 0.587 * box_rgb[1] + 0.114 * box_rgb[2]) / 255
        last_lines_color = (255, 255, 255, 220) if box_luminance < 0.5 else (0, 0, 0, 220)

        time_color = last_lines_color

        if time_x >= 0 and time_y >= 0 and time_x < size[0] and time_y < size[1]:
            try:
                icon_x = time_x - 75
                icon_color = random_contrast_color(box_color)
                draw_text_with_shadow(draw, (icon_x, time_y - 8), time_icon, font_icon, icon_color)
                draw.text((time_x, time_y), time_text, font=font_time, fill=time_color)
            except Exception as e:
                print(f"❌ Loi ve thoi gian len anh: {e}")
                draw_text_with_shadow(draw, (time_x - 75, time_y - 8), "⏰", font_icon, (255, 255, 255, 255))
                draw.text((time_x, time_y), " ??;??", font=font_time, fill=time_color)

        user_info = bot.fetchUserInfo(author_id) if author_id else None
        user_name = "Unknown"
        if user_info and hasattr(user_info, 'changed_profiles') and author_id in user_info.changed_profiles:
            user = user_info.changed_profiles[author_id]
            user_name = getattr(user, 'name', None) or getattr(user, 'displayName', None) or f"ID_{author_id}"

        greeting_name = "Chu Nhan" if is_admin(bot, author_id) else user_name # FIX: Used is_admin function correctly

        emoji_colors = {
            "🎵": random_contrast_color(box_color),
            "😁": random_contrast_color(box_color),
            "🖤": random_contrast_color(box_color),
            "💞": random_contrast_color(box_color),
            "🤖": random_contrast_color(box_color),
            "💻": random_contrast_color(box_color),
            "📅": random_contrast_color(box_color),
            "🎧": random_contrast_color(box_color),
            "🌙": random_contrast_color(box_color),
            "🌤️": (200, 150, 50, 255)
        }
        
        # FIX: Use getattr to access bot attributes safely, preventing crashes.
        prefix = getattr(bot, 'prefix', '/')
        bot_name = getattr(bot, 'me_name', 'MyBot')
        version = getattr(bot, 'version', '1.0')
        date_update = getattr(bot, 'date_update', 'N/A')

        text_lines = [
            f"Hi, {greeting_name}",
            f"💞 Chao mung đen voi menu 🤖 BOT",
            f"{prefix}bot on/off: 🚀 Bat/Tat tinh nang",
            "😁 Bot San Sang Phuc 🖤",
            f"🤖Bot: {bot_name} 💻Version: {version} 📅Update {date_update}"
        ]

        color1 = random_contrast_color(box_color)
        color2 = random_contrast_color(box_color)
        while color1 == color2:
            color2 = random_contrast_color(box_color)
        text_colors = [
            color1,
            color2,
            last_lines_color,
            last_lines_color,
            last_lines_color
        ]

        text_fonts = [
            font_text_large,
            font_text_big,
            font_text_bot,
            font_text_bot,
            font_text_small
        ]

        line_spacing = 85
        start_y = box_y1 + 10

        avatar_url = user_info.changed_profiles[author_id].avatar if user_info and hasattr(user_info, 'changed_profiles') and author_id in user_info.changed_profiles else None
        avatar_path = download_avatar(avatar_url)
        if avatar_path and os.path.exists(avatar_path):
            avatar_size = 200
            try:
                avatar_img = Image.open(avatar_path).convert("RGBA").resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)
                mask = Image.new("L", (avatar_size, avatar_size), 0)
                draw_mask = ImageDraw.Draw(mask)
                draw_mask.ellipse((0, 0, avatar_size, avatar_size), fill=255)
                border_size = avatar_size + 10
                rainbow_border = Image.new("RGBA", (border_size, border_size), (0, 0, 0, 0))
                draw_border = ImageDraw.Draw(rainbow_border)
                steps = 360
                for i in range(steps):
                    h = i / steps
                    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
                    draw_border.arc([(0, 0), (border_size-1, border_size-1)], start=i, end=i + (360 / steps), fill=(int(r * 255), int(g * 255), int(b * 255), 255), width=5)
                avatar_y = (box_y1 + box_y2 - avatar_size) // 2
                overlay.paste(rainbow_border, (box_x1 + 40, avatar_y), rainbow_border)
                overlay.paste(avatar_img, (box_x1 + 45, avatar_y + 5), mask)
            except Exception as e:
                print(f"❌ Loi xu ly avatar: {e}")
                draw.text((box_x1 + 60, (box_y1 + box_y2) // 2 - 140), "🐳", font=font_icon, fill=(0, 139, 139, 255))
        else:
            draw.text((box_x1 + 60, (box_y1 + box_y2) // 2 - 140), "🐳", font=font_icon, fill=(0, 139, 139, 255))

        current_line_idx = 0
        for i, line in enumerate(text_lines):
            if not line:
                current_line_idx += 1
                continue

            parts = []
            current_part = ""
            for char in line:
                if ord(char) > 0xFFFF:
                    if current_part:
                        parts.append(current_part)
                        current_part = ""
                    parts.append(char)
                else:
                    current_part += char
            if current_part:
                parts.append(current_part)

            total_width = 0
            part_widths = []
            current_font = font_text_bot if i == 4 else text_fonts[i]
            for part in parts:
                font_to_use = font_icon if any(ord(c) > 0xFFFF for c in part) else current_font
                width = draw.textbbox((0, 0), part, font=font_to_use)[2]
                part_widths.append(width)
                total_width += width

            max_width = box_x2 - box_x1 - 300
            if total_width > max_width:
                font_size = int(current_font.getbbox("A")[3] * max_width / total_width * 0.9)
                if font_size < 60:
                    font_size = 60
                try:
                    current_font = ImageFont.truetype(font_arial_path, size=font_size) if os.path.exists(font_arial_path) else ImageFont.load_default(size=font_size)
                except Exception as e:
                    print(f"❌ Loi đieu chinh font size: {e}")
                    current_font = ImageFont.load_default(size=font_size)
                total_width = 0
                part_widths = []
                for part in parts:
                    font_to_use = font_icon if any(ord(c) > 0xFFFF for c in part) else current_font
                    width = draw.textbbox((0, 0), part, font=font_to_use)[2]
                    part_widths.append(width)
                    total_width += width

            text_x = (box_x1 + box_x2 - total_width) // 2
            text_y = start_y + current_line_idx * line_spacing + (current_font.getbbox("A")[3] // 2)

            current_x = text_x
            for part, width in zip(parts, part_widths):
                if any(ord(c) > 0xFFFF for c in part):
                    emoji_color = emoji_colors.get(part, random_contrast_color(box_color))
                    draw_text_with_shadow(draw, (current_x, text_y), part, font_icon, emoji_color)
                    if part == "🤖" and i == 4:
                        draw_text_with_shadow(draw, (current_x, text_y - 5), part, font_icon, emoji_color)
                else:
                    if i < 2:
                        draw_text_with_shadow(draw, (current_x, text_y), part, current_font, text_colors[i])
                    else:
                        draw.text((current_x, text_y), part, font=current_font, fill=text_colors[i])
                current_x += width
            current_line_idx += 1

        right_icons = ["🤖"]
        right_icon = random.choice(right_icons)
        icon_right_x = box_x2 - 225
        icon_right_y = (box_y1 + box_y2 - 180) // 2
        draw_text_with_shadow(draw, (icon_right_x, icon_right_y), right_icon, font_icon_large, emoji_colors.get(right_icon, (80, 80, 80, 255)))

        final_image = Image.alpha_composite(bg_image, overlay)
        final_image = final_image.resize(final_size, Image.Resampling.LANCZOS)
        os.makedirs(os.path.dirname(OUTPUT_IMAGE_PATH), exist_ok=True)
        final_image.save(OUTPUT_IMAGE_PATH, "PNG", quality=95)
        print(f"✅ Anh menu đa đuoc luu: {OUTPUT_IMAGE_PATH}")
        return OUTPUT_IMAGE_PATH

    except Exception as e:
        print(f"❌ Loi xu ly anh menu: {e}")
        return None

def handle_bot_command(bot, message_object, author_id, thread_id, thread_type, command):
    def send_bot_response():
        settings = read_settings(bot.uid)
        allowed_thread_ids = settings.get('allowed_thread_ids', [])
        admin_bot = settings.get("admin_bot", [])
        banned_users = settings.get("banned_users", [])
        chat_user = (thread_type == ThreadType.USER)

        if author_id in banned_users:
            return

        if not (is_admin(bot, author_id) or thread_id in allowed_thread_ids or chat_user): # FIX: Use is_admin function
            return
        try:
            # FIX: Use getattr to prevent crash if bot.prefix is not set
            prefix = getattr(bot, 'prefix', '/')

            spam_enabled = settings.get('spam_enabled', {}).get(str(thread_id), True)
            anti_poll = settings.get('anti_poll', True)
            video_enabled = settings.get('video_enabled', True)
            card_enabled = settings.get('card_enabled', True)
            file_enabled = settings.get('file_enabled', True)
            image_enabled = settings.get('image_enabled', True)
            chat_enabled = settings.get('chat_enabled', True)
            voice_enabled = settings.get('voice_enabled', True)
            sticker_enabled = settings.get('sticker_enabled', True)
            gif_enabled = settings.get('gif_enabled', True)
            doodle_enabled = settings.get('doodle_enabled', True)
            allow_link = settings.get('allow_link', {}).get(str(thread_id), True)
            sos_status = settings.get('sos_status', True)

            status_icon = lambda enabled: "⭕️" if enabled else "✅"

            f"{status_icon(spam_enabled)} Anti-Spam 💢\n"
            f"{status_icon(anti_poll)} Anti-Poll 👍\n"
            f"{status_icon(video_enabled)} Anti-Video ▶️\n"
            f"{status_icon(card_enabled)} Anti-Card 🛡️\n"
            f"{status_icon(file_enabled)}Anti-File 🗂️\n"
            f"{status_icon(image_enabled)} Anti-Photo 🏖\n"
            f"{status_icon(chat_enabled)} SafeMode 🩹\n"
            f"{status_icon(voice_enabled)} Anti-Voice 🔊\n"
            f"{status_icon(sticker_enabled)} Anti-Sticker 😊\n"
            f"{status_icon(gif_enabled)} Anti-Gif 🖼️\n"
            f"{status_icon(doodle_enabled)} Anti-Draw ✏️\n"
            f"{status_icon(sos_status)}SOS 🆘\n"
            f"{status_icon(allow_link)} Anti-Link 🔗\n"

            parts = command.split()
            response = ""
            if len(parts) == 1:
                # FIX: Use `prefix` variable
                response = (
                        f"{get_user_name_by_id(bot, author_id)}\n"
                        f"➜ {prefix}bot info/policy: ♨️ Thong tin/Tac gia/Thoi gian/Chinh sach BOT\n"
                        f"➜ {prefix}bot setup on/off: ⚙️ Bat/Tat Noi quy BOT (OA)\n"
                        f"➜ {prefix}bot anti on/off/setup: 🚦Bat/Tat Anti (OA)\n"
                        f"➜ {prefix}bot newlink/dislink: 🔗 Tao/huy link nhom (OA)\n"
                        f"➜ {prefix}bot fix: 🔧 Sua loi treo lenh(OA)"
                        f"➜ {prefix}bot safemode on/off: 🩹 Che đo an toan text (OA)\n"
                        f"➜ {prefix}bot on/off: ⚙️ Bat/Tat BOT (OA)\n"
                        f"➜ {prefix}bot admin add/remove/list: 👑 Them/xoa Admin 🤖BOT\n"
                        f"➜ {prefix}bot skip add/remove/list: 👑 Them/xoa uu tien 🤖BOT (OA)\n"
                        f"➜ {prefix}bot leader add/remove/list: 👑 Them/xoa Truong/Pho (OA)\n"
                        f"➜ {prefix}bot autosend on/off: ✉️ Gui tin nhan(OA)\n"
                        f"➜ {prefix}bot noiquy: 💢 Noi quy box\n"
                        f"➜ {prefix}bot ban/vv/unban list: 😷 Khoa user\n"
                        f"➜ {prefix}bot kick: 💪 Kick user (OA)\n"
                        f"➜ {prefix}bot sos: 🆘 Khoa box (OA)\n"
                        f"➜ {prefix}bot block/unblock/list: 💪 Chan nguoi dung (OA)\n"
                        f"➜ {prefix}bot link on/off: 🔗 Cam link (OA)\n"
                        f"➜ {prefix}bot file on/off: 🗂️ Cam file (OA)\n"
                        f"➜ {prefix}bot video on/off: ▶️ Cam video (OA)\n"
                        f"➜ {prefix}bot sticker on/off: 😊 Cam sticker (OA)\n"
                        f"➜ {prefix}bot gif on/off: 🖼️ Cam Gif (OA)\n"
                        f"➜ {prefix}bot voice on/off: 🔊 Cam voice (OA)\n"
                        f"➜ {prefix}bot photo on/off: 🏖 Cam anh (OA)\n"
                        f"➜ {prefix}bot draw on/off: ✏️ Cam ve hinh (OA)\n"
                        f"➜ {prefix}bot anti poll on/off: 👍 Cam binh chon (OA)\n"
                        f"➜ {prefix}bot rule word [n] [m]: 📖 Cam n lan vi pham, phat m phut (OA)\n"
                        f"➜ {prefix}bot word add/remove/list [tu cam]: ✍️ Them/xoa tu cam (OA)\n"
                        f" ➜ {prefix}bot welcome on/off: 🎊 Welcome (OA)\n"
                        f"➜ {prefix}bot card on/off: 🛡️ Cam Card (OA)\n"
                        f"🤖 BOT {get_user_name_by_id(bot, bot.uid)} luon san sang phuc vu ban! 🌸\n"
                    )
            else:
                action = parts[1].lower()
                
                if action == 'on':
                    if not admin_cao(bot, author_id):
                        response = "❌Ban khong phai admin bot!"
                    elif thread_type != ThreadType.GROUP:
                        response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                    else:
                        response = bot_on_group(bot, thread_id)
                elif action == 'off':
                    if not is_admin(bot, author_id):
                        response = "❌Ban khong phai admin bot!"
                    elif thread_type != ThreadType.GROUP:
                        response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                    else:
                        response = bot_off_group(bot, thread_id)

                elif action == 'fix':
                    response = reload_modules(bot, message_object, thread_id, thread_type)

                elif action == 'autostk':
                    if not is_admin(bot, author_id):
                        response = "❌ Ban khong phai admin bot!"
                    else:
                        sub_action = parts[2].lower() if len(parts) > 2 else None
                        if sub_action == 'start':
                            if thread_id in autostk_loops and not autostk_loops[thread_id].is_set():
                                response = "Tính năng auto sticker liên tục đã được bật từ trước."
                            else:
                                stop_event = threading.Event()
                                autostk_loops[thread_id] = stop_event
                                loop_thread = threading.Thread(target=sticker_loop, args=(bot, thread_id, thread_type))
                                loop_thread.daemon = True
                                loop_thread.start()
                                response = "✅ Đã BẬT tính năng auto sticker liên tục."
                        elif sub_action == 'stop':
                            if thread_id in autostk_loops and not autostk_loops[thread_id].is_set():
                                autostk_loops[thread_id].set()
                                response = "⏹️ Đã TẮT tính năng auto sticker liên tục."
                            else:
                                response = "Tính năng này chưa được bật."
                        else:
                            response = f"Cú pháp không hợp lệ. Sử dụng:\n{prefix}bot autostk start\n{prefix}bot autostk stop"
                
                # FIX: Added logic for the 'autosend' command.
                elif action == 'autosend':
                    if not is_admin(bot, author_id):
                        response = "❌ Bạn không có quyền sử dụng lệnh này!"
                    else:
                        if len(parts) < 3:
                            response = (
                                f"🚦 Hướng dẫn sử dụng autosend:\n"
                                f"➜ {prefix}bot autosend on - Bật autosend\n"
                                f"➜ {prefix}bot autosend off - Tắt autosend\n"
                                f"➜ {prefix}bot autosend status - Xem trạng thái\n"
                                f"➜ {prefix}bot autosend list - Danh sách nhóm đã bật"
                            )
                        else:
                            sub_action = parts[2].lower()
                            if sub_action == "on":
                                response = handle_autosend_on(bot, thread_id, author_id, prefix)
                            elif sub_action == "off":
                                response = handle_autosend_off(bot, thread_id, author_id, prefix)
                            elif sub_action == "status":
                                status = get_autosend_status(bot, thread_id)
                                status_text = "🟢 Đang bật" if status else "🔴 Đang tắt"
                                try:
                                    group_info = bot.fetchGroupInfo(thread_id)
                                    group_name = group_info.gridInfoMap.get(thread_id, {}).get('name', 'Unknown Group')
                                except Exception:
                                    group_name = 'Unknown Group'
                                response = f"🚦 Trạng thái autosend:\n📌 Nhóm: {group_name}\n🔧 Trạng thái: {status_text}"
                            elif sub_action == "list":
                                response = list_autosend_groups(bot)
                            else:
                                response = f"❌ Lệnh không hợp lệ! Sử dụng: {prefix}bot autosend [on/off/status/list]"

                elif action == 'policy':
                    if thread_type != ThreadType.GROUP:
                        response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                    else:
                        response = list_bots(bot, thread_id)

                elif action == 'removelink':
                    if not is_admin(bot, author_id):
                        response = "❌Ban khong phai admin bot!"
                    else:
                        response = remove_link(bot, thread_id)
                elif action == 'newlink':
                    if not is_admin(bot, author_id):
                        response = "❌Ban khong phai admin bot!"
                    else:
                        response = newlink(bot, thread_id)
                elif action == 'skip':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [add/remove/list] sau lenh: {prefix}bot skip 🤧\n➜ Vi du: {prefix}bot skip add @Heoder ✅"
                    else:
                        sub_action = parts[2].lower()
                        if sub_action == 'add':
                            if len(parts) < 4:
                                response = f"➜ Vui long @tag ten nguoi dung sau lenh: {prefix}bot skip add ??\n➜ Vi du: {prefix}bot skip add @Heoder ✅"
                            else:
                                mentioned_uids = extract_uids_from_mentions(message_object)
                                settings = read_settings(bot.uid)
                                
                                if not is_admin(bot, author_id):
                                    response = "❌Ban khong phai admin bot!"
                                else:
                                    response = add_skip(bot, author_id, mentioned_uids)
                        elif sub_action == 'remove':
                            if len(parts) < 4:
                                response = f"➜ Vui long @tag ten nguoi dung sau lenh: {prefix}bot skip remove 🤧\n➜ Vi du: {prefix}bot skip remove @Heoder ✅"
                            else:
                                mentioned_uids = extract_uids_from_mentions(message_object)
                                settings = read_settings(bot.uid)
                                
                                if not is_admin(bot, author_id):
                                    response = "❌Ban khong phai admin bot!"
                                else:
                                    response = remove_skip(bot, author_id, mentioned_uids)
                        elif sub_action == 'list':
                            settings = read_settings(bot.uid)
                            skip_list = settings.get("skip_bot", [])
                            if skip_list:
                                response = "🚦 Danh sach nguoi dung đuoc uu tien: \n"
                                for uid in skip_list:
                                    response += f"👑 {get_user_name_by_id(bot, uid)} - {uid}\n"
                            else:
                                response = "🚦 Chua co nguoi dung nao trong danh sach uu tien 🤖"
                elif action == 'leader':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [add/remove] sau lenh: {prefix}bot leader 🤧\n➜ Vi du: {prefix}bot leader add @Hero ✅"
                    else:
                        sub_action = parts[2].lower()
                        
                      
                        if sub_action == 'add':
                            if len(parts) < 4:
                                response = f"➜ Vui long @tag ten nguoi dung sau lenh: {prefix}bot leader add 🤧\n➜ Vi du: {prefix}bot leader add @Hero ✅"
                            else:
                                mentioned_uids = extract_uids_from_mentions(message_object)
                                
                                if not is_admin(bot, author_id):
                                    response = "❌Ban khong phai admin bot!"
                                else:
                                    response = promote_to_admin(bot, mentioned_uids, thread_id)
                        elif sub_action == 'remove':
                            if len(parts) < 4:
                                response = f"➜ Vui long @tag ten nguoi dung sau lenh: {prefix}bot admin remove 🤧\n➜ Vi du: {prefix}bot admin remove @Hero ✅"
                            else:
                                mentioned_uids = extract_uids_from_mentions(message_object)
                                
                                if not is_admin(bot, author_id):
                                    response = "❌Ban khong phai admin bot!"
                                else:
                                    response = remove_adminn(bot, mentioned_uids, thread_id)
                        
                        elif sub_action == 'list':
                            
                            response = get_group_admins(bot, thread_id)

                        
                        else:
                            response = "➜ Lenh khong hop le. Vui long chon tu [add/remove/list]."
        
                elif action == 'anti':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [poll on/off] sau lenh: {prefix}bot anti 🤧\n➜ Vi du: {prefix}bot anti poll on ✅"
                    else:
                        sub_action = parts[2].lower()
                        if sub_action == 'poll':
                            if len(parts) < 4:
                                response = f"➜ Vui long nhap [on/off] sau lenh: {prefix}bot anti poll 🤧\n➜ Vi du: {prefix}bot anti poll on ✅"
                            else:
                                sub_sub_action = parts[3].lower()
                                if not is_admin(bot, author_id):
                                    response = "❌Ban khong phai admin bot!"
                                elif sub_sub_action == 'off':  
                                    settings = read_settings(bot.uid)
                                    settings["anti_poll"] = True
                                    write_settings(bot.uid, settings)
                                    response = f"{status_icon(True)} Anti-Poll 👍\n" # FIX: Show correct status
                                elif sub_sub_action == 'on':  
                                    settings = read_settings(bot.uid)
                                    settings["anti_poll"] = False
                                    write_settings(bot.uid, settings)
                                    response = f"{status_icon(False)} Anti-Poll 👍\n" # FIX: Show correct status
                                else:
                                    response = "➜ Lenh khong hop le. Vui long chon 'on' hoac 'off' sau lenh anti poll 🤧"
                                
                elif action == 'safemode':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [on/off] sau lenh: {prefix}bot chat 🤧\n➜ Vi du: {prefix}bot chat on hoac {prefix}bot chat off ✅"
                    else:
                        chat_action = parts[2].lower()
                        settings = read_settings(bot.uid)

                        if chat_action == 'off':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['chat_enabled'] = True  
                                response = f"{status_icon(True)} SafeMode 🩹\n"
                        elif chat_action == 'on':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['chat_enabled'] = False  
                                response = f"{status_icon(False)} SafeMode 🩹\n"
                        
                        write_settings(bot.uid, settings)  

                elif action == 'sticker':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [on/off] sau lenh: {prefix}bot sticker 🤧\n➜ Vi du: {prefix}bot sticker on hoac {prefix}bot sticker off ✅"
                    else:
                        sticker_action = parts[2].lower()
                        settings = read_settings(bot.uid)

                        if sticker_action == 'off':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['sticker_enabled'] = True  
                                response = f"{status_icon(True)} Anti-Sticker 😊\n"
                                
                        elif sticker_action == 'on':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['sticker_enabled'] = False  
                                response = f"{status_icon(False)} Anti-Sticker 😊\n"
                        
                        write_settings(bot.uid, settings)

                elif action == 'draw':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [on/off] sau lenh: {prefix}bot draw 🤧\n➜ Vi du: {prefix}bot draw on hoac {prefix}bot draw off ✅"
                    else:
                        draw_action = parts[2].lower()
                        settings = read_settings(bot.uid)

                        if draw_action == 'off':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['doodle_enabled'] = True  
                                response = f"{status_icon(True)} Anti-Draw ✏️\n"
                        elif draw_action == 'on':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['doodle_enabled'] = False  
                                response = f"{status_icon(False)} Anti-Draw ✏️\n"
                        
                        write_settings(bot.uid, settings)

                elif action == 'gif':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [on/off] sau lenh: {prefix}bot gif 🤧\n➜ Vi du: {prefix}bot gif on hoac {prefix}bot gif off ✅"
                    else:
                        gif_action = parts[2].lower()
                        settings = read_settings(bot.uid)

                        if gif_action == 'off':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['gif_enabled'] = True  
                                response = f"{status_icon(True)} Anti-Gif 🖼️\n"
                        elif gif_action == 'on':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['gif_enabled'] = False  
                                response = f"{status_icon(False)} Anti-Gif 🖼️\n"
                        
                        write_settings(bot.uid, settings)

                elif action == 'video':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [on/off] sau lenh: {prefix}bot video 🤧\n➜ Vi du: {prefix}bot video on hoac {prefix}bot video off ✅"
                    else:
                        video_action = parts[2].lower()
                        settings = read_settings(bot.uid)

                        if video_action == 'off':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['video_enabled'] = True  
                                response = f"{status_icon(True)} Anti-Video ▶️\n"
                        elif video_action == 'on':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['video_enabled'] = False  
                                response = f"{status_icon(False)} Anti-Video ▶️\n"
                        
                        write_settings(bot.uid, settings)

                elif action == 'photo':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [on/off] sau lenh: {prefix}bot image 🤧\n➜ Vi du: {prefix}bot image on hoac {prefix}bot image off ✅"
                    else:
                        image_action = parts[2].lower()
                        settings = read_settings(bot.uid)

                        if image_action == 'off':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['image_enabled'] = True  
                                response = f"{status_icon(True)} Anti-Photo 🏖\n"
                        elif image_action == 'on':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['image_enabled'] = False  
                                response = f"{status_icon(False)} Anti-Photo 🏖\n"
                        
                        write_settings(bot.uid, settings)

                elif action == 'voice':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [on/off] sau lenh: {prefix}bot voice 🤧\n➜ Vi du: {prefix}bot voice on hoac {prefix}bot voice off ✅"
                    else:
                        voice_action = parts[2].lower()
                        settings = read_settings(bot.uid)

                        if voice_action == 'off':
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['voice_enabled'] = True  
                                response = f"{status_icon(True)} Anti-Voice 🔊\n"
                        elif voice_action == 'on':
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['voice_enabled'] = False  
                                response = f"{status_icon(False)} Anti-Voice 🔊\n"
                        
                        write_settings(bot.uid, settings)

                elif action == 'file':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [on/off] sau lenh: {prefix}bot file 🤧\n➜ Vi du: {prefix}bot file on hoac {prefix}bot file off ✅"
                    else:
                        file_action = parts[2].lower()
                        settings = read_settings(bot.uid)

                        if file_action == 'off':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['file_enabled'] = True  
                                response = f"{status_icon(True)} Anti-File 🗂️\n"
                                
                        elif file_action == 'on':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['file_enabled'] = False  
                                response = f"{status_icon(False)} Anti-File 🗂️\n"
                        
                        write_settings(bot.uid, settings)

                elif action == 'card':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [on/off] sau lenh: {prefix}bot card 🤧\n➜ Vi du: {prefix}bot card on hoac {prefix}bot card off ✅"
                    else:
                        card_action = parts[2].lower()
                        settings = read_settings(bot.uid)

                        if card_action == 'on':
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['card_enabled'] = False  
                                response = f"{status_icon(False)} Anti-Card 🛡️\n"
                        elif card_action == 'off':  
                            if not is_admin(bot, author_id):  
                                response = "❌Ban khong phai admin bot!"
                            else:
                                settings['card_enabled'] = True  
                                response = f"{status_icon(True)} Anti-Card 🛡️\n"
                        
                        write_settings(bot.uid, settings)

                elif action == 'welcome':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [on/off] sau lenh: {prefix}bot welcome 🤧\n➜ Vi du: {prefix}bot welcome on hoac {prefix}bot welcome off ✅"
                    else:
                        settings = read_settings(bot.uid)
                        setup_action = parts[2].lower()
                        if setup_action == 'on':
                            if not is_admin(bot, author_id):
                                response = "❌Ban khong phai admin bot!"
                            elif thread_type != ThreadType.GROUP:
                                response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                            else:
                                response = handle_welcome_on(bot, thread_id)
                        elif setup_action == 'off':
                            if not is_admin(bot, author_id):
                                response = "❌Ban khong phai admin bot!"
                            elif thread_type != ThreadType.GROUP:
                                response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                            else:
                                response = handle_welcome_off(bot, thread_id)
                        
                elif action == 'spam':
                    if not is_admin(bot, author_id):
                        response = "❌Ban khong phai admin bot!"
                    elif len(parts) < 3:
                        response = f"➜ Vui long nhap [on/off] sau lenh: {prefix}bot spam 🤧\n➜ Vi du: {prefix}bot spam on hoac {prefix}bot spam off ✅"
                    else:
                        spam_action = parts[2].lower()
                        settings = read_settings(bot.uid)

                        if 'spam_enabled' not in settings:
                            settings['spam_enabled'] = {}

                        if spam_action == 'on':
                            settings['spam_enabled'][thread_id] = True  
                            response = f"{status_icon(True)} Anti-Spam 💢\n"
                        elif spam_action == 'off':
                            settings['spam_enabled'][thread_id] = False  
                            response = f"{status_icon(False)} Anti-Spam 💢\n"
                        
                        write_settings(bot.uid, settings)
                elif action == 'info':
                    response = (
                        "╭────────────────────────────╮\n"
                        f"│ 🤖 Bot phien ban: {getattr(bot, 'version', '1.0')}\n"
                        f"│ 📅 Cap nhat lan cuoi: {getattr(bot, 'date_update', 'N/A')}\n"
                        f"│ 👨‍💻 Nha phat trien: {getattr(bot, 'me_name', 'MyBot')}\n"
                        f"│ 📖 Huong dan: Dung lenh [{prefix}bot/help]\n"
                        "│ ⏳ Thoi gian phan hoi: 1 giay\n"
                        "│ ⚡ Tinh nang noi bat:\n"
                        "│  ├➜ 🛡️ Anti-spam,anti-radi, chan link, tu cam\n"
                        "│  ├➜ 🤬 Kiem soat noi dung chui the\n"
                        "│  ├➜ 🚫 Tu đong duyet & chan spammer\n"
                        "│  ├➜ 🔊 Quan ly giong noi & sticker\n"
                        "│  ├➜ 🖼️ Ho tro hinh anh, GIF, video\n"
                        "│  ├➜ 🗳️ Kiem soat cuoc khao sat\n"
                        "│  ├➜ 🔗 Bao ve nhom khoi link đoc hai\n"
                        "│  └➜ 🔍 Kiem tra & phan tich tin nhan\n"
                        "╰────────────────────────────╯"
                    )

                elif action == 'admin':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [list/add/remove] sau lenh: {prefix}bot admin 🤧\n➜ Vi du: {prefix}bot admin list hoac {prefix}bot admin add @Heoder hoac {prefix}bot admin remove @Heoder ✅"
                    else:
                        settings = read_settings(bot.uid)
                        admin_bot = settings.get("admin_bot", [])  
                        sub_action = parts[2].lower()
                        if sub_action == 'add':
                            if len(parts) < 4:
                                response = f"➜ Vui long @tag ten nguoi dung sau lenh: {prefix}bot admin add 🤧\n➜ Vi du: {prefix}bot admin add @Heoder ✅"
                            else:
                                if not admin_cao(bot, author_id):
                                    response = "❌Ban khong phai admin bot!"
                                else:
                                    mentioned_uids = extract_uids_from_mentions(message_object)
                                    response = add_admin(bot, author_id, mentioned_uids)
                        elif sub_action == 'remove':
                            if len(parts) < 4:
                                response = f"➜ Vui long @tag ten nguoi dung sau lenh: {prefix}bot admin remove 🤧\n➜ Vi du: {prefix}bot admin remove @Heoder ✅"
                            else:
                                if not admin_cao(bot, author_id):
                                    response = "❌Ban khong phai admin bot!"
                                else:
                                    mentioned_uids = extract_uids_from_mentions(message_object)
                                    response = remove_admin(bot, author_id, mentioned_uids)
                        elif sub_action == 'list':
                            if admin_bot:
                                response = f"🚦🧑‍💻 Danh sach Admin 🤖BOT {get_user_name_by_id(bot, bot.uid)}\n"
                                for idx, uid in enumerate(admin_bot, start=1):
                                    response += f"➜   {idx}. {get_user_name_by_id(bot, uid)} - {uid}\n"
                            else:
                                response = "➜ Khong co Admin BOT nao trong danh sach 🤧"

                elif action == 'setup':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [on/off] sau lenh: {prefix}bot setup 🤧\n➜ Vi du: {prefix}bot setup on hoac {prefix}bot setup off ✅"
                    else:
                        setup_action = parts[2].lower()
                        if setup_action == 'on':
                            if not is_admin(bot, author_id):
                                response = "❌Ban khong phai admin bot!"
                            elif thread_type != ThreadType.GROUP:
                                response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                            else:
                                response = setup_bot_on(bot, thread_id)
                        elif setup_action == 'off':
                            if not is_admin(bot, author_id):
                                response = "❌Ban khong phai admin bot!"
                            elif thread_type != ThreadType.GROUP:
                                response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                            else:
                                response = setup_bot_off(bot,thread_id)
                        
                elif action == 'link':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [on/off] sau lenh: {prefix}bot link 🤧\n➜ Vi du: {prefix}bot link on hoac {prefix}bot link off ✅"
                    else:
                        link_action = parts[2].lower()
                        if not is_admin(bot, author_id):
                            response = "❌Ban khong phai admin bot!"
                        elif thread_type != ThreadType.GROUP:
                            response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                        else:
                            settings = read_settings(bot.uid)

                            if 'allow_link' not in settings:
                                settings['allow_link'] = {}

                            
                            if link_action == 'on':
                                settings['allow_link'][thread_id] = True
                                response = f"{status_icon(True)} Anti-Link 🔗\n"
                            elif link_action == 'off':
                                settings['allow_link'][thread_id] = False
                                response = f"{status_icon(False)} Anti-Link 🔗\n"
                        write_settings(bot.uid, settings)
                elif action == 'word':
                    if len(parts) < 3: # FIX: Should be < 4
                        response = f"➜ Vui long nhap [add/remove] [tu khoa] sau lenh: {prefix}bot word 🤧\n➜ Vi du: {prefix}bot word add [tu khoa] hoac {prefix}bot word remove [tu khoa] ✅"
                    else:
                        if not is_admin(bot, author_id):
                            response = "❌Ban khong phai admin bot!"
                        elif thread_type != ThreadType.GROUP:
                            response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                        else:
                            word_action = parts[2].lower()
                            word = ' '.join(parts[3:]) 
                            if word_action == 'add':
                                response = add_forbidden_word(bot, author_id, word)
                            elif word_action == 'remove':
                                response = remove_forbidden_word(bot, author_id, word)
                            # FIX: Added list option
                            elif word_action == 'list':
                                forbidden_words = settings.get('forbidden_words', [])
                                if forbidden_words:
                                    response = "✍️ Danh sách từ cấm:\n - " + "\n - ".join(forbidden_words)
                                else:
                                    response = "✍️ Danh sách từ cấm đang trống."
                elif action == 'noiquy':
                    settings = read_settings(bot.uid)
                    rules=settings.get("rules", {})
                    word_rule = rules.get("word", {"threshold": 3, "duration": 30})
                    threshold_word = word_rule["threshold"]
                    duration_word = word_rule["duration"]
                    group_admins = settings.get('group_admins', {})
                    admins = group_admins.get(thread_id, [])
                    group = bot.fetchGroupInfo(thread_id).gridInfoMap[thread_id]
                    if admins:
                        response = (
                            f"➜ 💢 Noi quy 🤖BOT {getattr(bot, 'me_name', 'MyBot')} đuoc ap dung cho nhom: {group.name} - ID: {thread_id} ✅\n"
                            f"➜ 🚫 Cam su dung cac tu ngu tho tuc 🤬 trong nhom\n"
                            f"➜ 💢 Vi pham {threshold_word} lan se bi 😷 khoa mom {duration_word} phut\n"
                            f"➜ ⚠️ Neu tai pham 2 lan se bi 💪 kick khoi nhom 🤧"
                        )
                    else:
                        response = (
                            f"➜ 💢 Noi quy khong ap dung cho nhom: {group.name} - ID: {thread_id} 💔\n➜ Ly do: 🤖BOT {getattr(bot, 'me_name', 'MyBot')} chua đuoc setup hoac BOT khong co quyen cam key quan tri nhom 🤧"
                        )
                elif action == 'ban':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap 'list' hoac 'ban @tag' sau lenh: {prefix}bot 🤧\n➜ Vi du: {prefix}bot ban list hoac {prefix}bot ban @user ✅"
                    else:
                        sub_action = parts[2].lower()

                        if sub_action == 'list':
                            response = print_muted_users_in_group(bot, thread_id)
                        elif sub_action == 'vv':
                            if not is_admin(bot, author_id):
                                response = "➜ Lenh nay chi kha thi voi quan tri vien 🤧"
                            elif thread_type != ThreadType.GROUP:
                                response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                            elif not check_admin_group(bot, thread_id):
                                response = "➜ 🤖BOT khong co quyen quan tri nhom đe thuc hien lenh nay 🤧"
                            else:
                                uids = extract_uids_from_mentions(message_object)
                                if not uids:
                                    response = f"➜ Vui long tag nguoi can ban sau lenh: {prefix}bot ban vv @username 🤧"
                                else:
                                    response = ban_users_permanently(bot, uids, thread_id)
                        else:
                            if not is_admin(bot, author_id):
                                response = "➜ Lenh nay chi kha thi voi quan tri vien 🤧"
                            elif thread_type != ThreadType.GROUP:
                                response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                            elif not check_admin_group(bot, thread_id):
                                response = "➜ Lenh nay khong kha thi do 🤖BOT khong co quyen quan tri nhom 🤧"
                            else:
                                uids = extract_uids_from_mentions(message_object)
                                response = add_users_to_ban_list(bot, uids, thread_id, "Quan tri vien cam")

                elif action == 'unban':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap @tag ten sau lenh: {prefix}bot unban 🤧\n➜ Vi du: {prefix}bot unban @Heoder ✅"
                    else:
                        if not is_admin(bot, author_id):
                            response = "❌Ban khong phai admin bot!"
                        elif thread_type != ThreadType.GROUP:
                            response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                        else:
                            
                            uids = extract_uids_from_mentions(message_object)
                            response = remove_users_from_ban_list(bot, uids, thread_id)
                elif action == 'block':
                      
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap @tag ten sau lenh: {prefix}bot block 🤧\n➜ Vi du: {prefix}bot block @Heoder ✅"
                    else:
                        s_action = " ".join(parts[2:])
                      
                        if s_action == 'list':
                            response = print_blocked_users_in_group(bot, thread_id)
                        else:
                         
                            if not is_admin(bot, author_id):
                                response = "❌Ban khong phai admin bot!"
                            elif thread_type != ThreadType.GROUP:
                                response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                            elif check_admin_group(bot,thread_id)==False:
                                response = "➜ Lenh nay khong kha thi do 🤖BOT khong co quyen cam 🔑 key nhom 🤧"
                            else:
                              
                                uids = extract_uids_from_mentions(message_object)
                                response = block_users_from_group(bot, uids, thread_id)
                elif action == 'sos':
                    if not is_admin(bot, author_id):
                        response = "❌Ban khong phai admin bot!"
                    else:
                        settings = read_settings(bot.uid)
                        sos_status = settings.get("sos_status", False)

                        if sos_status:
                            bot.changeGroupSetting(groupId=thread_id, lockSendMsg=0)
                            settings["sos_status"] = False
                            response = f"{status_icon(False)}SOS 🆘\n"
                        else:
                            bot.changeGroupSetting(groupId=thread_id, lockSendMsg=1)
                            settings["sos_status"] = True
                            response = f"{status_icon(True)}SOS 🆘\n"

                        write_settings(bot.uid, settings)
  
                elif action == 'unblock':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap UID sau lenh: {prefix}bot unblock 🤧\n➜ Vi du: {prefix}bot unblock 8421834556970988033, 842183455697098804... ✅"
                    else:
                        if not is_admin(bot, author_id):
                            response = "❌Ban khong phai admin bot!"
                        elif thread_type != ThreadType.GROUP:
                            response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                        else:
                           
                            ids_str = parts[2]  
                            print(f"Chuoi UIDs: {ids_str}")

                            uids = [uid.strip() for uid in ids_str.split(',') if uid.strip()]
                            print(f"Danh sach UIDs: {uids}")

                            if uids:
                              
                                response = unblock_users_from_group(bot, uids, thread_id)
                            else:
                                response = "➜ Khong co UID nao hop le đe bo chan 🤧"

                elif action == 'kick':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap @tag ten sau lenh: {prefix}bot kick 🤧\n➜ Vi du: {prefix}bot kick @Heoder ✅"
                    else:
                        if not is_admin(bot, author_id):
                            response = "❌Ban khong phai admin bot!"
                        elif thread_type != ThreadType.GROUP:
                            response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                        elif check_admin_group(bot,thread_id)==False:
                                response = "➜ Lenh nay khong kha thi do 🤖BOT khong co quyen cam 🔑 key nhom 🤧"
                        else:
                            uids = extract_uids_from_mentions(message_object)
                            response = kick_users_from_group(bot, uids, thread_id)
                
                elif action == 'rule':
                    if len(parts) < 5:
                        response = f"➜ Vui long nhap word [n lan] [m phut] sau lenh: {prefix}bot rule 🤧\n➜ Vi du: {prefix}bot rule word 3 30 ✅"
                    else:
                        rule_type = parts[2].lower()
                        try:
                            threshold = int(parts[3])
                            duration = int(parts[4])
                        except ValueError:
                            response = "➜ So lan va phut phat phai la so nguyen 🤧"
                        else:
                            settings = read_settings(bot.uid)
                            if rule_type not in ["word", "spam"]:
                                response = f"➜ Lenh {prefix}bot rule {rule_type} khong đuoc ho tro 🤧\n➜ Vi du: {prefix}bot rule word 3 30✅"
                            else:
                                if not is_admin(bot, author_id):
                                    response = "❌Ban khong phai admin bot!"
                                elif thread_type != ThreadType.GROUP:
                                    response = "➜ Lenh nay chi kha thi trong nhom 🤧"
                                else:
                                    settings.setdefault("rules", {})
                                    settings["rules"][rule_type] = {
                                        "threshold": threshold,
                                        "duration": duration
                                    }
                                    write_settings(bot.uid, settings)
                                    response = f"➜ 🔄 Đa cap nhat noi quy cho {rule_type}: Neu vi pham {threshold} lan se bi phat {duration} phut ✅"
                elif action == 'cam':
                    if len(parts) < 3:
                        response = f"➜ Vui long nhap [add/remove/list] sau lenh: {prefix}bot cam 🤧\n➜ Vi du: {prefix}bot cam add @Heoder ✅"
                    else:
                        sub_action = parts[2].lower()
                        if sub_action == 'add':
                            if len(parts) < 4:
                                response = f"➜ Vui long @tag ten nguoi dung sau lenh: {prefix}bot cam add 🤧\n➜ Vi du: {prefix}bot cam add @Heoder ✅"
                            if not admin_cao(bot, author_id):
                                response = "❌Ban khong phai admin bot!"
                            else:
                                mentioned_uids = extract_uids_from_mentions(message_object)
                                response = ban_user_from_commands(bot, author_id, mentioned_uids)
                        elif sub_action == 'remove':
                            if len(parts) < 4:
                                response = f"➜ Vui long @tag ten nguoi dung sau lenh: {prefix}bot cam remove 🤧\n➜ Vi du: {prefix}bot cam remove @Heoder ✅"
                            if not admin_cao(bot, author_id):
                                response = "❌Ban khong phai admin bot!"
                            else:
                                mentioned_uids = extract_uids_from_mentions(message_object)
                                response = unban_user_from_commands(bot, author_id, mentioned_uids)
                        elif sub_action == 'list':
                            response = list_banned_users(bot)


                else:
                    bot.sendReaction(message_object, "❌", thread_id, thread_type)
            
            if response:
                if len(parts) == 1:
                    os.makedirs(CACHE_PATH, exist_ok=True)
    
                    image_path = generate_menu_image(bot, author_id, thread_id, thread_type)
                    if not image_path:
                        bot.sendMessage("❌ Khong the tao anh menu!", thread_id, thread_type)
                        return
                    reaction = [
                        "❌", "🤧", "🐞", "😊", "🔥", "👍", "💖", "🚀",
                        "😍", "😂", "😢", "😎", "🙌", "💪", "🌟", "🍀",
                        "🎉", "🦁", "🌈", "🍎", "⚡", "🔔", "🎸", "🍕",
                        "🏆", "📚", "🦋", "🌍", "⛄", "🎁", "💡", "🐾",
                        "😺", "🐶", "🐳", "🦄", "🌸", "🍉", "🍔", "🎄"
                    ]

                    num_reactions = random.randint(2, 3)
                    selected_reactions = random.sample(reaction, num_reactions)

                    for emoji in selected_reactions:
                        bot.sendReaction(message_object, emoji, thread_id, thread_type)
                    bot.sendLocalImage(
                        imagePath=image_path,
                        message=Message(text=response, mention=Mention(author_id, length=len(f"{get_user_name_by_id(bot, author_id)}"), offset=0)),
                        thread_id=thread_id,
                        thread_type=thread_type,
                        width=1920,
                        height=600,
                        ttl=240000
                    )
                    
                    try:
                        if os.path.exists(image_path):
                            os.remove(image_path)
                    except Exception as e:
                        print(f"❌ Loi khi xoa anh: {e}")
                else:
                    reaction = [
                        "❌", "🤧", "🐞", "😊", "🔥", "👍", "💖", "🚀",
                        "😍", "😂", "😢", "😎", "🙌", "💪", "🌟", "🍀",
                        "🎉", "🦁", "🌈", "🍎", "⚡", "🔔", "🎸", "🍕",
                        "🏆", "📚", "🦋", "🌍", "⛄", "🎁", "💡", "🐾",
                        "😺", "🐶", "🐳", "🦄", "🌸", "🍉", "🍔", "🎄"
                    ]

                    num_reactions = random.randint(2, 3)
                    selected_reactions = random.sample(reaction, num_reactions)

                    for emoji in selected_reactions:
                        bot.sendReaction(message_object, emoji, thread_id, thread_type)
                    bot.replyMessage(Message(text=response),message_object, thread_id=thread_id, thread_type=thread_type,ttl=9000)
        
        except Exception as e:
            print(f"Error in handle_bot_command: {e}") # FIX: Added more detailed error logging
            bot.replyMessage(Message(text="➜ 🐞 Đa xay ra loi gi đo 🤧"), message_object, thread_id=thread_id, thread_type=thread_type)

    thread = Thread(target=send_bot_response)
    thread.start()

font_path_emoji = os.path.join("emoji.ttf")
font_path_arial = os.path.join("arial unicode ms.otf")

def create_gradient_colors(num_colors: int) -> List[tuple[int, int, int]]:
    return [(random.randint(30, 255), random.randint(30, 255), random.randint(30, 255)) for _ in range(num_colors)]

def interpolate_colors(colors: List[tuple[int, int, int]], text_length: int, change_every: int) -> List[tuple[int, int, int]]:
    gradient = []
    num_segments = len(colors) - 1
    steps_per_segment = max((text_length // change_every) + 1, 1)

    for i in range(num_segments):
        for j in range(steps_per_segment):
            if len(gradient) < text_length:
                ratio = j / steps_per_segment
                interpolated_color = (
                    int(colors[i][0] * (1 - ratio) + colors[i + 1][0] * ratio),
                    int(colors[i][1] * (1 - ratio) + colors[i + 1][1] * ratio),
                    int(colors[i][2] * (1 - ratio) + colors[i + 1][2] * ratio)
                )
                gradient.append(interpolated_color)

    while len(gradient) < text_length:
        gradient.append(colors[-1])

    return gradient[:text_length]

def is_emoji(character: str) -> bool:
    return character in emoji.EMOJI_DATA

def create_text(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont, 
                emoji_font: ImageFont.FreeTypeFont, text_position: tuple[int, int], 
                gradient_colors: List[tuple[int, int, int]]):
    gradient = interpolate_colors(gradient_colors, text_length=len(text), change_every=4)
    current_x = text_position[0]

    for i, char in enumerate(text):
        color = tuple(gradient[i])
        try:
            selected_font = emoji_font if is_emoji(char) and emoji_font else font
            draw.text((current_x, text_position[1]), char, fill=color, font=selected_font)
            text_bbox = draw.textbbox((current_x, text_position[1]), char, font=selected_font)
            text_width = text_bbox[2] - text_bbox[0]
            current_x += text_width
        except Exception as e:
            print(f"Loi khi ve ky tu '{char}': {e}. Bo qua ky tu nay.")
            continue

def draw_gradient_border(draw: ImageDraw.Draw, center_x: int, center_y: int, 
                        radius: int, border_thickness: int, 
                        gradient_colors: List[tuple[int, int, int]]):
    num_segments = 80
    gradient = interpolate_colors(gradient_colors, num_segments, change_every=10)

    for i in range(num_segments):
        start_angle = i * (360 / num_segments)
        end_angle = (i + 1) * (360 / num_segments)
        color = tuple(gradient[i])
        draw.arc(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
            start=start_angle, end=end_angle, fill=color, width=border_thickness
        )

def load_image_from_url(url: str) -> Image.Image:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert('RGBA')
    except Exception as e:
        print(f"Loi khi tai anh tu URL {url}: {e}")
        return Image.new('RGBA', (100, 100), (0, 0, 0, 0))

def generate_short_filename(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def load_random_background(background_dir: str = "background") -> Image.Image:
    if not os.path.exists(background_dir):
        print(f"Error: Background folder '{background_dir}' does not exist.")
        return None
    background_files = [os.path.join(background_dir, f) for f in os.listdir(background_dir) 
                       if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not background_files:
        print(f"Error: No valid image files found in '{background_dir}'")
        return None
    background_path = random.choice(background_files)
    try:
        return Image.open(background_path).convert("RGBA")
    except Exception as e:
        print(f"Error loading image {background_path}: {e}")
        return None

def create_default_background(width: int, height: int) -> Image.Image:
    return Image.new('RGBA', (width, height), (0, 100, 0, 255))

def create_default_avatar(name: str) -> Image.Image:
    avatar = Image.new('RGBA', (170, 170), (200, 200, 200, 255))
    draw = ImageDraw.Draw(avatar)
    draw.ellipse((0, 0, 170, 170), fill=(100, 100, 255, 255))
    initials = (name[:2].upper() if name else "??")
    font = ImageFont.truetype(font_path_arial, 60)
    text_bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    draw.text(
        ((170 - text_width) // 2, (170 - text_height) // 2),
        initials,
        font=font,
        fill=(255, 255, 255, 255)
    )
    return avatar

def create_banner(bot, uid: str, thread_id: str, group_name: str = None, 
                 avatar_url: str = None, event_type: str = None, 
                 event_data = None, background_dir: str = "background") -> str:
    try:
        settings = read_settings(bot.uid)
        if not settings.get("welcome", {}).get(thread_id, False):
            return None
            
        member_info = bot.fetchUserInfo(uid).changed_profiles.get(uid)
        if not member_info:
            print(f"[ERROR] Khong tim thay thong tin user {uid}")
            return None
            
        avatar_url = member_info.avatar if not avatar_url else avatar_url
        user_name = getattr(member_info, 'zaloName', f"User{uid}")

        group_info = bot.group_info_cache.get(thread_id, {})
        group_name = group_info.get('name', "Nhom khong xac đinh") if not group_name else group_name
        total_members = group_info.get('total_member', 0)
        thread_type = ThreadType.GROUP

        ow_name = ""
        ow_avatar_url = ""
        if event_data and hasattr(event_data, 'sourceId'):
            try:
                ow_info = bot.fetchUserInfo(event_data.sourceId).changed_profiles.get(event_data.sourceId)
                ow_name = getattr(ow_info, 'zaloName', f"Admin{event_data.sourceId}") if ow_info else "Quan tri vien"
                ow_avatar_url = ow_info.avatar if ow_info else ""
            except Exception as e:
                print(f"[WARNING] Loi khi lay thong tin admin: {e}")
                ow_name = "Quan tri vien"

        event_config = {
            GroupEventType.JOIN: {
                'main_text': f'Chao mung, {user_name} 💜',
                'group_name_text': group_name,
                'credit_text': "Đa đuoc duyet vao nhom",
                'msg': f"✨ {user_name}",
                'mention': None
            },
            GroupEventType.LEAVE: {
                'main_text': f'Tam biet, {user_name} 💔',
                'group_name_text': group_name,
                'credit_text': "Đa roi khoi nhom",
                'msg': f'💔 {user_name}',
                'mention': None
            },
            GroupEventType.ADD_ADMIN: {
                'main_text': f'Chuc mung, {user_name}',
                'group_name_text': group_name,
                'credit_text': f"bo nhiem lam pho nhom🔑",
                'msg': f'🎉 {user_name}',
                'mention': None
            },
            GroupEventType.REMOVE_ADMIN: {
                'main_text': f'Rat tiec, {user_name}',
                'group_name_text': group_name,
                'credit_text': f"Đa bi xoa vai tro nhom❌",
                'msg': f'⚠️ {user_name}',
                'mention': None
            },
            GroupEventType.REMOVE_MEMBER: {
                'main_text': f'Nhay nay, {user_name}',
                'group_name_text': group_name,
                'credit_text': f"Đa bi kick khoi nhom🚫",
                'msg': f'🚫 {user_name}',
                'mention': None
            },
            GroupEventType.JOIN_REQUEST: {
                'main_text': f'Yeu cau tham gia ✋',
                'group_name_text': group_name,
                'credit_text': f"{user_name}",
                'msg': f'✋ {user_name}',
                'mention': None
            }
        }

        config = event_config.get(event_type)
        if not config:
            print(f"[ERROR] Su kien {event_type} khong đuoc ho tro")
            return None
        
        banner_width, banner_height = 980, 350
        
        try:
            background = load_random_background(background_dir) or create_default_background(banner_width, banner_height)
            background = background.resize((banner_width, banner_height), Image.LANCZOS)
            background_blurred = background.filter(ImageFilter.GaussianBlur(radius=5))
        except Exception as e:
            print(f"[ERROR] Loi background: {e}")
            background = create_default_background(banner_width, banner_height)
            background_blurred = background

        overlay = Image.new("RGBA", (banner_width, banner_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        glass_color = (
            random.randint(30, 80),
            random.randint(30, 80), 
            random.randint(30, 80),
            random.randint(170, 220)
        )
        
        rect_margin = 60
        rect_x0, rect_y0 = rect_margin, 30
        rect_x1, rect_y1 = banner_width - rect_margin, banner_height - 30
        draw.rounded_rectangle([rect_x0, rect_y0, rect_x1, rect_y1], radius=30, fill=glass_color)

        member_circle_radius = 25
        member_circle_x = rect_x1 - member_circle_radius - 20 
        member_circle_y = rect_y0 + member_circle_radius + 15
        
        circle_border_color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255),
            255 
        )
        
        draw.ellipse(
            [member_circle_x - member_circle_radius, 
             member_circle_y - member_circle_radius,
             member_circle_x + member_circle_radius, 
             member_circle_y + member_circle_radius],
            outline=circle_border_color,
            width=6
        )
        
        member_font = ImageFont.truetype(font_path_arial, 20)
        member_count_text = str(total_members)
        member_bbox = draw.textbbox((0, 0), member_count_text, font=member_font)
        member_text_width = member_bbox[2] - member_bbox[0]
        member_text_height = member_bbox[3] - member_bbox[1]
        
        member_text_x = member_circle_x - (member_text_width // 2)
        member_text_y = member_circle_y - (member_text_height // 2 + 10)
        draw.text(
            (member_text_x, member_text_y),
            member_count_text,
            font=member_font,
            fill=(255, 255, 255, 255)
        )

        banner = Image.alpha_composite(background_blurred, overlay)

        try:
            avatar = load_image_from_url(avatar_url) or create_default_avatar(user_name)
            avatar_size = 135
            mask = Image.new('L', (avatar_size, avatar_size), 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, avatar_size, avatar_size), fill=255)
            
            avatar = avatar.resize((avatar_size, avatar_size), Image.LANCZOS)
            avatar_x = rect_x0 + 25
            avatar_y = rect_y1 - avatar_size - 70
            banner.paste(avatar, (avatar_x, avatar_y), mask)
            
            border_size = 4
            border = Image.new('RGBA', (avatar_size + border_size*2, avatar_size + border_size*2), (255, 255, 255, 255))
            border_mask = Image.new('L', (avatar_size + border_size*2, avatar_size + border_size*2), 0)
            border_draw = ImageDraw.Draw(border_mask)
            border_draw.ellipse((0, 0, avatar_size + border_size*2, avatar_size + border_size*2), fill=255)
            banner.paste(border, (avatar_x - border_size, avatar_y - border_size), border_mask)
            banner.paste(avatar, (avatar_x, avatar_y), mask)
        except Exception as e:
            print(f"[WARNING] Loi avatar nguoi dung: {e}")

        if ow_avatar_url:
            try:
                ow_avatar = load_image_from_url(ow_avatar_url) or create_default_avatar(ow_name)
                ow_avatar = ow_avatar.resize((avatar_size, avatar_size), Image.LANCZOS)
                ow_avatar_x = rect_x1 - avatar_size - 25
                ow_avatar_y = avatar_y
                banner.paste(ow_avatar, (ow_avatar_x, ow_avatar_y), mask)
                
                banner.paste(border, (ow_avatar_x - border_size, ow_avatar_y - border_size), border_mask)
                banner.paste(ow_avatar, (ow_avatar_x, ow_avatar_y), mask)
            except Exception as e:
                print(f"[WARNING] Loi avatar nguoi thuc hien: {e}")

        draw = ImageDraw.Draw(banner)
        
        def get_vibrant_color():
            colors = [
                (255, 90, 90), (90, 255, 90), (90, 90, 255),
                (255, 255, 90), (255, 90, 255), (90, 255, 255)
            ]
            return random.choice(colors)
        
        font_main = ImageFont.truetype(font_path_arial, 50)
        main_text = config['main_text']
        main_bbox = draw.textbbox((0, 0), main_text, font=font_main)
        main_width = main_bbox[2] - main_bbox[0]
        main_x = rect_x0 + (rect_x1 - rect_x0 - main_width) // 2
        main_y = rect_y0 + 10
        draw.text((main_x, main_y), main_text, font=font_main, fill=get_vibrant_color())

        font_group = ImageFont.truetype(font_path_arial, 48)
        group_text = config['group_name_text']
        group_bbox = draw.textbbox((0, 0), group_text, font=font_group)
        group_width = group_bbox[2] - group_bbox[0]
        group_x = rect_x0 + (rect_x1 - rect_x0 - group_width) // 2
        group_y = main_y + main_bbox[3] + 15
        max_width = rect_x1 - rect_x0 - 20
        if group_width > max_width:
            while group_bbox[2] - group_bbox[0] > max_width and len(group_text) > 0:
                group_text = group_text[:-1]
                group_bbox = draw.textbbox((0, 0), group_text + "...", font=font_group)
            group_text += "..."
        draw.text((group_x, group_y), group_text, font=font_group, fill=get_vibrant_color())

        font_credit = ImageFont.truetype(font_path_arial, 38)
        credit_text = config['credit_text']
        credit_bbox = draw.textbbox((0, 0), credit_text, font=font_credit)
        credit_width = credit_bbox[2] - credit_bbox[0]
        credit_x = rect_x0 + (rect_x1 - rect_x0 - credit_width) // 2
        credit_y = group_y + group_bbox[3] + 15
        draw.text((credit_x, credit_y), credit_text, font=font_credit, fill=(255, 255, 255))

        time_text = f"📅 {time.strftime('%d/%m/%Y')}  ⏰ {time.strftime('%H:%M:%S')}    🔑 Executed by {ow_name}" if ow_name else f"📅 {time.strftime('%d/%m/%Y')}     ⏰ {time.strftime('%H:%M:%S')}"
        font_footer = ImageFont.truetype(font_path_arial, 22)
        footer_bbox = draw.textbbox((0, 0), time_text, font=font_footer)
        footer_x = rect_x0 + (rect_x1 - rect_x0 - footer_bbox[2]) // 2 + 20
        footer_y = rect_y1 - footer_bbox[3] - 15
        draw.text((footer_x, footer_y), time_text, font=font_footer, fill=(220, 220, 220))

        file_name = f"banner_{int(time.time())}.jpg"
        try:
            banner.convert('RGB').save(file_name, quality=95)
            if event_type:
                bot.sendMultiLocalImage(
                    [file_name],
                    thread_id=thread_id,
                    thread_type=thread_type,
                    width=banner_width,
                    height=banner_height,
                    message=Message(text=config['msg'], mention=config.get('mention')),
                    ttl=60000 * 60
                )
        except Exception as e:
            print(f"[ERROR] Loi khi luu/gui banner: {e}")
            return None
        finally:
            try:
                delete_file(file_name)
            except:
                pass

        return file_name

    except Exception as e:
        print(f"[CRITICAL] Loi nghiem trong: {str(e)}")
        return None

def delete_file(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Đa xoa tep: {file_path}")
    except Exception as e:
        print(f"Loi khi xoa tep: {e}")

def load_emoji_font(size: int) -> ImageFont.FreeTypeFont:
    try:
        if os.path.exists(font_path_emoji):
            return ImageFont.truetype(font_path_emoji, size)
        if os.name == 'nt':
            return ImageFont.truetype("seguiemj.ttf", size)
        elif os.path.exists("/System/Library/Fonts/Apple Color Emoji.ttc"):
            return ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", size)
    except Exception:
        return None

def handle_event(client, event_data, event_type):
    try:
        if not hasattr(event_data, 'groupId'):
            print(f"Du lieu su kien khong co groupId: {event_data}")
            return

        thread_id = event_data.groupId
        thread_type = ThreadType.GROUP
        
        settings = read_settings(client.uid)
        if not settings.get("welcome", {}).get(thread_id, False):
            return
            
        group_info = client.fetchGroupInfo(thread_id)
        group_name = group_info.gridInfoMap.get(str(thread_id), {}).get('name', 'nhom')
        total_member = group_info.gridInfoMap[str(thread_id)]['totalMember']

        client.group_info_cache[thread_id] = {
            "name": group_name,
            "member_list": group_info.gridInfoMap[str(thread_id)]['memVerList'],
            "total_member": total_member
        }

        for member in event_data.updateMembers:
            member_id = member['id']
            member_name = member['dName']
            user_info = client.fetchUserInfo(member_id)
            avatar_url = user_info.changed_profiles[member_id].avatar

            banner_path = create_banner(
                client, 
                member_id, 
                thread_id, 
                group_name=group_name, 
                avatar_url=avatar_url, 
                event_type=event_type, 
                event_data=event_data
            )

            if not banner_path or not os.path.exists(banner_path):
                print(f"Khong tao đuoc banner cho {member_name} voi event {event_type}")
                continue

            if event_type == GroupEventType.JOIN:
                msg = Message(
                    text=f"🚦 {member_name}",
                    mention=Mention(uid=member_id, length=len(member_name), offset=3)
                )
                client.sendLocalImage(banner_path, thread_id=thread_id, thread_type=thread_type, 
                                    width=980, height=350, message=msg, ttl=60000 * 60)
            elif event_type == GroupEventType.LEAVE:
                client.sendLocalImage(banner_path, thread_id=thread_id, thread_type=thread_type, 
                                    width=980, height=350, ttl=60000 * 60)
            else:
                print(f"Su kien {event_type} khong đuoc ho tro")

            delete_file(banner_path)

    except Exception as e:
        print(f"Loi khi xu ly event {event_type}: {e}")

def handle_welcome_on(bot, thread_id: str) -> str:
    settings = read_settings(bot.uid)
    if "welcome" not in settings:
        settings["welcome"] = {}
    settings["welcome"][thread_id] = True
    write_settings(bot.uid, settings)
    return f"🚦Che đo welcome đa 🟢 Bat 🎉"

def handle_welcome_off(bot, thread_id: str) -> str:
    settings = read_settings(bot.uid)
    if "welcome" in settings and thread_id in settings["welcome"]:
        settings["welcome"][thread_id] = False
        write_settings(bot.uid, settings)
        return f"🚦Che đo welcome đa 🔴 Tat 🎉"
    return "🚦Nhom chua co thong tin cau hinh welcome đe 🔴 Tat 🤗"

def get_allow_welcome(bot, thread_id: str) -> bool:
    settings = read_settings(bot.uid)
    return settings.get("welcome", {}).get(thread_id, False)

def initialize_group_info(bot, allowed_thread_ids: List[str]):
    for thread_id in allowed_thread_ids:
        group_info = bot.fetchGroupInfo(thread_id).gridInfoMap.get(thread_id, None)
        if group_info:
            bot.group_info_cache[thread_id] = {
                "name": group_info['name'],
                "member_list": group_info['memVerList'],
                "total_member": group_info['totalMember']
            }
        else:
            print(f"Bo qua nhom {thread_id}")

def check_member_changes(bot, thread_id: str) -> tuple[set, set]:
    current_group_info = bot.fetchGroupInfo(thread_id).gridInfoMap.get(thread_id, None)
    cached_group_info = bot.group_info_cache.get(thread_id, None)

    if not cached_group_info or not current_group_info:
        return set(), set()

    old_members = set([member.split('_')[0] for member in cached_group_info["member_list"]])
    new_members = set([member.split('_')[0] for member in current_group_info['memVerList']])

    joined_members = new_members - old_members
    left_members = old_members - new_members

    bot.group_info_cache[thread_id] = {
        "name": current_group_info['name'],
        "member_list": current_group_info['memVerList'],
        "total_member": current_group_info['totalMember']
    }

    return joined_members, left_members

def handle_group_member(bot, message_object, author_id: str, thread_id: str, thread_type: str):
    if not get_allow_welcome(bot, thread_id):
        return
        
    current_group_info = bot.fetchGroupInfo(thread_id).gridInfoMap.get(thread_id, None)
    cached_group_info = bot.group_info_cache.get(thread_id, None)

    if not cached_group_info or not current_group_info:
        print(f"Khong co thong tin nhom cho thread_id {thread_id}")
        return

    old_members = set([member.split('_')[0] for member in cached_group_info["member_list"]])
    new_members = set([member.split('_')[0] for member in current_group_info['memVerList']])

    joined_members = new_members - old_members
    left_members = old_members - new_members

    for member_id in joined_members:
        banner = create_banner(bot, member_id, thread_id, event_type=GroupEventType.JOIN, 
                             event_data=type('Event', (), {'sourceId': author_id or bot.uid})())
        if banner and os.path.exists(banner):
            try:
                user_name = bot.fetchUserInfo(member_id).changed_profiles[member_id].zaloName
                bot.sendLocalImage(
                    banner,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    width=980,
                    height=350,
                    message=Message(
                        text=f"🚦 {user_name}",
                        mention=Mention(uid=member_id, length=len(user_name), offset=3)
                    ),
                    ttl=86400000
                )
                delete_file(banner)
            except Exception as e:
                print(f"Loi khi gui banner cho {member_id} (JOIN): {e}")
                if os.path.exists(banner):
                    delete_file(banner)

    for member_id in left_members:
        banner = create_banner(bot, member_id, thread_id, event_type=GroupEventType.LEAVE, 
                             event_data=type('Event', (), {'sourceId': author_id or bot.uid})())
        if banner and os.path.exists(banner):
            try:
                bot.sendLocalImage(
                    banner,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    width=980,
                    height=350,
                    ttl=86400000
                )
                delete_file(banner)
            except Exception as e:
                print(f"Loi khi gui banner cho {member_id} (LEAVE): {e}")
                if os.path.exists(banner):
                    delete_file(banner)

    bot.group_info_cache[thread_id] = {
        "name": current_group_info['name'],
        "member_list": current_group_info['memVerList'],
        "total_member": current_group_info['totalMember']
    }

def start_member_check_thread(bot, allowed_thread_ids: List[str]):
    def check_members_loop():
        while True:
            for thread_id in allowed_thread_ids:
                if not get_allow_welcome(bot, thread_id):
                    continue
                handle_group_member(bot, None, None, thread_id, ThreadType.GROUP)
            time.sleep(2)

    thread = threading.Thread(target=check_members_loop, daemon=True)
    thread.start()