import os
import asyncio
from pyrogram import Client, filters, idle
from aiohttp import web

# Aapke variables jo aapne diye hain
API_ID = 33603340  # Dhyan rakhein, yeh number bina quotes ke hona chahiye
API_HASH = "0f1a7f670519f9e44d0d7fdb6aa8efba"
BOT_TOKEN = "7874642792:AAF08vl1-qcMUHOIUZrL5IwJS1A7zoD5ucw"

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

# --- Render ke liye Dummy Web Server ---
async def web_server():
    async def handle(request):
        return web.Response(text="Bot is running smoothly on Render!")
    
    webapp = web.Application()
    webapp.router.add_get('/', handle)
    runner = web.AppRunner(webapp)
    await runner.setup()
    
    # Render khud PORT deta hai, agar nahi mila toh 8080 use karega
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server started on port {port}")

# Bot aur server ko ek sath start karne ka sahi tareeqa
async def main():
    await web_server()
    await app.start()
    print("Bot Started Successfully! Ab channel mein /acceptall command use karein.")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
