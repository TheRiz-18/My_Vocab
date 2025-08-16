import pandas as pd
import requests
from datetime import datetime
import pytz

# --- Config ---
TOKEN = "8256439502:AAHtuLFtIFXoByvOP_5SrDrX-_BKZjVV0ZQ"
CHAT_ID = "6893797334"
CSV_FILE = "Vocab.csv"

# --- Load CSV ---
try:
    df = pd.read_csv(CSV_FILE, encoding='utf-8')
    if not all(col in df.columns for col in ['Word', 'Meaning', 'Example']):
        raise ValueError("CSV must have columns: Word, Meaning, Example")
    total_words = len(df)
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit(1)

# --- Current time in IST ---
tz = pytz.timezone("Asia/Kolkata")
now = datetime.now(tz)
hour = now.hour
minute = now.minute

# --- Only send between 10 AM - 11 PM IST ---
if 10 <= hour <= 23:
    # Each hour has 2 slots: :00 and :30
    half_hour_index = 0 if minute < 30 else 1

    # Calculate total half-hour periods passed since 10 AM
    total_half_hours = (hour - 10) * 2 + half_hour_index

    # Index in CSV
    index = total_half_hours % total_words

    word = df.iloc[index]['Word']
    meaning = df.iloc[index]['Meaning']
    example = df.iloc[index]['Example']

    # --- Send Telegram message ---
    message = f"📚 Word of the Hour:\n\n*{word}*\n\nMeaning: {meaning}\n\nExample: {example}"
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
        else:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")
else:
    print(f"Current hour {hour} is outside the scheduled range (10 AM - 11 PM IST).")
