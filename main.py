import os
import threading
from pyrogram import Client, filters
from flask import Flask

# --- Render ke liye Dummy Web Server ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running perfectly on Render!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

# Web server ko background mein start karna
threading.Thread(target=run_web, daemon=True).start()
# ----------------------------------------

# Aapke variables (Inhe yahan daalein ya Render Environment Variables mein set karein)
API_ID = "33603340"        # Yahan apna API_ID daalein (Bina quotes ke agar integer hai, par string bhi chalega)
API_HASH = "0f1a7f670519f9e44d0d7fdb6aa8efba"    # Yahan apna API_HASH daalein
BOT_TOKEN = "7874642792:AAF08vl1-qcMUHOIUZrL5IwJS1A7zoD5ucw"  # Yahan apna BOT_TOKEN daalein

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("acceptall") & filters.admin)
async def approve_all_requests(client, message):
    chat_id = message.chat.id
    msg = await message.reply_text("Saari pending requests approve ho rahi hain... thoda wait karein.")
    
    try:
        await client.approve_all_chat_join_requests(chat_id)
        await msg.edit_text("✅ Sabhi pending requests ko successfully channel members bana diya gaya hai!")
    except Exception as e:
        await msg.edit_text(f"❌ Error aaya: {e}")

# Bot start karna
print("Bot Started...")
app.run()
