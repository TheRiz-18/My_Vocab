import pandas as pd
import requests
from datetime import datetime
import pytz
import os

# --- Config ---
TOKEN = "8256439502:AAHtuLFtIFXoByvOP_5SrDrX-_BKZjVV0ZQ"
CHAT_ID = "6893797334"
CSV_FILE = "Vocab.csv"
INDEX_FILE = "last_index.txt"

# --- Load CSV ---
try:
    df = pd.read_csv(CSV_FILE, encoding='utf-8')
    if not all(col in df.columns for col in ['Word', 'Meaning', 'Example']):
        raise ValueError("CSV must have columns: Word, Meaning, Example")
    total_words = len(df)
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit(1)

# --- Load last index ---
if os.path.exists(INDEX_FILE):
    with open(INDEX_FILE, 'r') as f:
        last_index = int(f.read().strip())
else:
    last_index = -1  # start before first word

# --- Determine next index ---
next_index = (last_index + 1) % total_words  # wrap around after last word

# --- Get current hour in IST ---
tz = pytz.timezone("Asia/Kolkata")
now = datetime.now(tz)
hour = now.hour

# --- Send only between 10 AM - 11 PM IST ---
if 10 <= hour <= 23:
    word = df.iloc[next_index]['Word']
    meaning = df.iloc[next_index]['Meaning']
    example = df.iloc[next_index]['Example']

    # --- Send Telegram message ---
    message = f"📚 Word of the Hour:\n\n*{word}*\nMeaning: {meaning}\nExample: {example}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"Message sent successfully: {word}")
            # --- Save last index ---
            with open(INDEX_FILE, 'w') as f:
                f.write(str(next_index))
        else:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")
else:
    print(f"Current hour {hour} is outside the scheduled range (10 AM - 11 PM IST).")
