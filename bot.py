import os
import time
import telebot
import yt_dlp

from telebot import apihelper
from requests.exceptions import ConnectionError, ReadTimeout

# ==============================
# RD3B4T DOWNLOADER BOT
# ==============================

BOT_TOKEN = "8646123624:AAEnze6MUIBvWLW0hW55hcJElKVXsqUOBdI"

bot = telebot.TeleBot(BOT_TOKEN)

# ==============================
# TELEGRAM FIX
# ==============================

apihelper.READ_TIMEOUT = 60
apihelper.CONNECT_TIMEOUT = 60
apihelper.RETRY_ON_ERROR = True

# ==============================
# DOWNLOAD FOLDER
# ==============================

DOWNLOAD_DIR = "downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# ==============================
# START COMMAND
# ==============================

@bot.message_handler(commands=['start'])
def start(message):
    text = """
🔥 RD3B4T DOWNLOADER 🔥

✅ Instagram
✅ Facebook
✅ YouTube
✅ WhatsApp Public Links
✅ Pinterest

⚡ Fast Download
⚡ HD Quality
⚡ Stable System

📌 Send Video Link
"""
    bot.reply_to(message, text)

# ==============================
# DOWNLOAD FUNCTION
# ==============================

def download_video(url):
    ydl_opts = {
        'format': 'best[height<=720][ext=mp4]/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'noprogress': True,
        'socket_timeout': 30,
        'retries': 10,
        'fragment_retries': 10,
        'nocheckcertificate': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

        mp4_file = file_path.rsplit(".", 1)[0] + ".mp4"
        if os.path.exists(mp4_file):
            file_path = mp4_file

        if not os.path.exists(file_path):
            return None

        if os.path.getsize(file_path) == 0:
            return None

        return file_path

# ==============================
# HANDLE LINKS
# ==============================

@bot.message_handler(func=lambda m: True)
def downloader(message):
    url = message.text.strip()

    allowed = [
        "instagram.com",
        "facebook.com",
        "fb.watch",
        "youtube.com",
        "youtu.be",
        "whatsapp.com",
        "wa.me",
        "pinterest.com"
    ]

    if not any(site in url for site in allowed):
        bot.reply_to(message, "❌ Unsupported Link")
        return

    wait = bot.reply_to(message, "⚡ Downloading...")

    try:
        file_path = download_video(url)

        if not file_path:
            bot.reply_to(message, "❌ Download Failed")
            return

        file_size = os.path.getsize(file_path)

        # Telegram standard bot upload limit is 50MB
        if file_size > 49 * 1024 * 1024:
            with open(file_path, "rb") as file:
                bot.send_document(
                    message.chat.id,
                    file,
                    timeout=120,
                    caption="🔥 Downloaded By RD3B4T"
                )
        else:
            with open(file_path, "rb") as video:
                bot.send_video(
                    message.chat.id,
                    video,
                    supports_streaming=True,
                    timeout=120,
                    caption="🔥 Downloaded By RD3B4T"
                )

        # Clean up downloaded file
        try:
            os.remove(file_path)
        except Exception:
            pass

        # Delete processing message
        try:
            bot.delete_message(message.chat.id, wait.message_id)
        except Exception:
            pass

    except Exception as e:
        bot.reply_to(message, f"❌ Error:\n{e}")

# ==============================
# RUN BOT
# ==============================

print("🔥 RD3B4T BOT STARTED 🔥")

while True:
    try:
        bot.infinity_polling(
            timeout=60,
            long_polling_timeout=60,
            skip_pending=True
        )
    except (ConnectionError, ReadTimeout):
        print("⚠️ Reconnecting...")
        time.sleep(5)
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(5)
                    
