import os
import requests
from django.conf import settings

def send_telegram_message(message: str) -> None:
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    if not bot_token or not chat_id:
        print("Telegram bot credentials are not set in .env")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Failed to send telegram message: {response.text}")
    except requests.RequestException as e:
        print(f"Error connecting to Telegram API: {e}")
