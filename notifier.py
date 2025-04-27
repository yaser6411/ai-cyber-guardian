# utils/notifier.py
import telebot
from config import TELEGRAM_TOKEN, ADMIN_CHAT_ID

class Notifier:
    def __init__(self):
        self.bot = telebot.TeleBot(TELEGRAM_TOKEN)
        
    def send_alert(self, message):
        try:
            self.bot.send_message(ADMIN_CHAT_ID, f"🚨 ALERT: {message}")
        except Exception as e:
            print(f"فشل إرسال التنبيه: {e}")
            
    def send_log(self, command, output):
        log_msg = f"📄 Command executed:\n`{command}`\n\nOutput:\n```\n{output}\n```"
        self.bot.send_message(ADMIN_CHAT_ID, log_msg, parse_mode="Markdown")