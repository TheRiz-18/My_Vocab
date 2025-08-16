import pandas as pd
import requests
from datetime import datetime
import csv

# --- Config ---
TOKEN = "8256439502:AAHtuLFtIFXoByvOP_5SrDrX-_BKZjVV0ZQ"
CHAT_ID = "6893797334"
CSV_FILE = "Vocab.csv"

# Load vocabulary with additional parameters
try:
    df = pd.read_csv(
        CSV_FILE,
        delimiter=',',
        quoting=csv.QUOTE_MINIMAL,
        encoding='utf-8',
        on_bad_lines='warn'  # Change to 'error' after fixing CSV
    )
    print(f"Loaded {len(df)} rows")
    print("Columns:", df.columns.tolist())
    print("First few rows:\n", df.head())
except pd.errors.ParserError as e:
    print(f"Error reading CSV: {e}")
    exit(1)

# Function to send Telegram message
def send_message(word, meaning, example):
    message = f"📚 Word of the Hour:\n\n*{word}*\nMeaning: {meaning}\nExample: {example}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")
    else:
        print(f"Message sent successfully: {word}")

# Determine current hour (24h format)
now = datetime.now()
hour = now.hour

# Send word according to the hour (10 AM = 10, 11 PM = 23)
if 10 <= hour <= 23:
    index = hour - 10  # first word at 10 AM
    if index < len(df):
        # Access columns explicitly to handle potential mismatches
        word = df.iloc[index]['Word']
        meaning = df.iloc[index]['Meaning']
        example = df.iloc[index]['Example']
        print(f"Sending word for hour {hour}: {word}, {meaning}, {example}")
        send_message(word, meaning, example)
    else:
        print(f"No word available for hour {hour}. Index {index} is out of range.")
else:
    print(f"Current hour {hour} is outside the scheduled range (10 AM - 11 PM).")
