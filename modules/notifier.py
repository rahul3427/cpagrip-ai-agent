import os
import requests

class Notifier:
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

    def send_notification(self, message):
        """Sends notification to Telegram if credentials are set, with auto-chunking and safe delivery."""
        print("\n" + "="*50)
        print("📢 AGENT NOTIFICATION OUTPUT")
        print("="*50)
        print(message)
        print("="*50 + "\n")

        if self.bot_token and self.chat_id and self.bot_token != "your_telegram_bot_token":
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            
            # Telegram max message size is 4096 chars. Split safely if needed.
            chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
            
            for index, chunk in enumerate(chunks):
                # Try sending with Markdown
                payload = {
                    "chat_id": self.chat_id,
                    "text": chunk,
                    "parse_mode": "Markdown"
                }
                try:
                    res = requests.post(url, json=payload, timeout=10)
                    # If Telegram markdown parsing fails, fallback to plain text
                    if not res.ok and "can't parse entities" in res.text:
                        payload.pop("parse_mode", None)
                        res = requests.post(url, json=payload, timeout=10)
                    
                    if res.ok:
                        print(f"✅ [Telegram] Message chunk {index+1}/{len(chunks)} delivered!")
                    else:
                        print(f"[!] [Telegram] Error sending chunk {index+1}: {res.text}")
                except Exception as e:
                    print(f"[!] [Telegram] Network error sending notification: {e}")
        else:
            print("ℹ️ Telegram credentials not configured. Notification printed to console.")

    def send_photo(self, photo_path, caption=""):
        """Sends a generated Pin image directly to Telegram."""
        if self.bot_token and self.chat_id and os.path.exists(photo_path):
            url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
            try:
                with open(photo_path, "rb") as photo_file:
                    files = {"photo": photo_file}
                    data = {"chat_id": self.chat_id, "caption": caption[:1024]}
                    res = requests.post(url, data=data, files=files, timeout=20)
                    if res.ok:
                        print("🎨 [Telegram] Pinterest Pin image delivered to your phone!")
                    else:
                        print(f"[!] [Telegram] Failed to send photo: {res.text}")
            except Exception as e:
                print(f"[!] [Telegram] Error uploading photo: {e}")
