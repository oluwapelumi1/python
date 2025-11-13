# -------------------------------
# IMPORTS
# -------------------------------
import requests               # To fetch the HTML content of the Zealy page
from bs4 import BeautifulSoup # To parse HTML and extract task titles
from telegram import Bot      # To send messages via your Telegram bot
import time                   # To pause between checks

# -------------------------------
# CONFIGURATION
# -------------------------------
BOT_TOKEN = "8469480625:AAGjppHqNG7bD1lljcuFvOfLseqAX_rMvYw"  # <-- Your Telegram bot token
CHAT_ID = "1938127032"                                       # <-- Your Telegram chat ID
ZEALY_URL = "https://zealy.io/cw/inference/questboard"       # <-- Zealy questboard URL

# Initialize the bot
bot = Bot(token=BOT_TOKEN)

# Keep track of tasks we already sent notifications for
known_tasks = set()

# -------------------------------
# FUNCTION: Check Zealy
# -------------------------------
def check_zealy():
    global known_tasks
    try:
        # Fetch the Zealy page
        r = requests.get(ZEALY_URL)
        # Parse the page HTML
        soup = BeautifulSoup(r.text, "html.parser")

        # Find all task titles
        # Note: This assumes tasks are inside <h3> tags
        tasks = [t.text.strip() for t in soup.find_all("h3")]

        # Find tasks that are new (not in known_tasks)
        new_tasks = [t for t in tasks if t not in known_tasks]

        # If there are new tasks, send a Telegram message
        if new_tasks:
            for task in new_tasks:
                message = f"🚀 New Zealy Task Found!\n\n{task}\n\n{ZEALY_URL}"
                bot.send_message(chat_id=CHAT_ID, text=message)
            # Remember these tasks so we don’t send duplicates
            known_tasks.update(new_tasks)

    except Exception as e:
        # If there’s an error (like network issue), print it
        print("Error:", e)

# -------------------------------
# MAIN LOOP
# -------------------------------
if __name__ == "__main__":
    print("🤖 Zealy alert bot is running... Checking every 30 seconds.")
    # Infinite loop: check Zealy every 30 seconds
    while True:
        check_zealy()
        time.sleep(30)
