import json
import sqlite3
import os

DEVELOPER_ID = 7294948308

print("🔧 ইমার্জেন্সি ফিক্স চালু হচ্ছে...")

# 1. blocked_users.json ফিক্স
if os.path.exists("blocked_users.json"):
    with open("blocked_users.json", "r") as f:
        data = json.load(f)
    
    if DEVELOPER_ID in data:
        data.remove(DEVELOPER_ID)
        with open("blocked_users.json", "w") as f:
            json.dump(data, f)
        print("✅ blocked_users.json থেকে রিমুভ করা হয়েছে")
    else:
        print("ℹ️ blocked_users.json এ ডেভেলপার নেই")

# 2. SQLite ডাটাবেস ফিক্স
if os.path.exists("bot_data.db"):
    try:
        conn = sqlite3.connect("bot_data.db")
        c = conn.cursor()
        c.execute("UPDATE users SET is_banned = 0 WHERE user_id = ?", (DEVELOPER_ID,))
        c.execute("UPDATE users SET temp_ban_until = NULL WHERE user_id = ?", (DEVELOPER_ID,))
        conn.commit()
        conn.close()
        print("✅ SQLite ডাটাবেস আপডেট করা হয়েছে")
    except Exception as e:
        print(f"⚠️ SQLite ত্রুটি: {e}")

# 3. user_language.json চেক
if os.path.exists("user_language.json"):
    with open("user_language.json", "r") as f:
        lang_data = json.load(f)
    if str(DEVELOPER_ID) not in lang_data:
        lang_data[str(DEVELOPER_ID)] = "bn"
        with open("user_language.json", "w") as f:
            json.dump(lang_data, f)
        print("✅ user_language.json আপডেট করা হয়েছে")

print("\n✅ সম্পূর্ণ! এখন বট রিস্টার্ট করুন এবং /start দিন")