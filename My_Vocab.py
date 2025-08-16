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
day_number = now.timetuple().tm_yday  # Day of the year (1-366)

# --- Calculate index without TXT ---
# Each day: 10 AM to 11 PM = 14 words
# Total words sent so far = (day_number - start_day) * 14 + (hour - 10)
start_day = 1  # or change to the day you start
if 10 <= hour <= 23:
    total_hours_passed = (day_number - start_day) * 14 + (hour - 10)
    index = total_hours_passed % total_words

    word = df.iloc[index]['Word']
    meaning = df.iloc[index]['Meaning']
    example = df.iloc[index]['Example']

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
        else:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")
else:
    print(f"Current hour {hour} is outside the scheduled range (10 AM - 11 PM IST).")
