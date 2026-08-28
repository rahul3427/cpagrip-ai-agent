import os
import requests

class Notifier:
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

    def send_notification(self, message):
        """Sends notification to Telegram if credentials are set, otherwise prints to console."""
        print("\n" + "="*50)
        print("📢 AGENT NOTIFICATION OUTPUT")
        print("="*50)
        print(message)
        print("="*50 + "\n")

        if self.bot_token and self.chat_id and self.bot_token != "your_telegram_bot_token":
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            try:
                res = requests.post(url, json=payload, timeout=10)
                if res.status_code == 200:
                    print("✅ [Telegram] Push notification successfully delivered to your device!")
                else:
                    print(f"[!] [Telegram] Failed to send: {res.text}")
            except Exception as e:
                print(f"[!] [Telegram] Network error sending notification: {e}")
        else:
            print("ℹ️ Telegram credentials not configured. Notification printed to console.")
