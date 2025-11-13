# ------------------------------- 
# IMPORTS
# -------------------------------
import requests                    # Fetch HTML content
from bs4 import BeautifulSoup      # Parse HTML
from telegram import Bot           # Telegram Bot API
import time                        # Sleep timer

# ------------------------------- 
# CONFIGURATION
# -------------------------------
BOT_TOKEN = "8469480625:AAGjppHqNG7bD1lljcuFvOfLseqAX_rMvYw"  # <-- Your Telegram bot token
CHAT_ID = "1938127032"                                       # <-- Your Telegram chat ID
ZEALY_URL = "https://zealy.io/cw/swisschainsa/questboard"       # <-- Zealy questboard URL

# Initialize bot
bot = Bot(token=BOT_TOKEN)

# Track tasks already seen
known_tasks = set()

# ------------------------------- 
# FUNCTION: CHECK ZEALY
# -------------------------------
def check_zealy():
    global known_tasks
    try:
        # Fetch page
        r = requests.get(ZEALY_URL)

        # Parse HTML
        soup = BeautifulSoup(r.text, "html.parser")

        # Extract task names (inside <h3> tags)
        tasks = [t.text.strip() for t in soup.find_all("h3")]

        # Find new tasks
        new_tasks = [t for t in tasks if t not in known_tasks]

        # Send notification if new tasks
        if new_tasks:
            for task in new_tasks:
                message = f"🚀 New Zealy Task Found!\n\n{task}\n\n{ZEALY_URL}"
                bot.send_message(chat_id=CHAT_ID, text=message)

            # Update known tasks
            known_tasks.update(new_tasks)

    except Exception as e:
        print("Error:", e)

# ------------------------------- 
# MAIN LOOP
# -------------------------------
if __name__ == "__main__":
    print("🤖 Zealy alert bot is running... Checking every 30 seconds...")

    while True:
        check_zealy()
        time.sleep(30)
