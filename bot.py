import telebot
import requests
import os
from flask import Flask, request

API_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

def get_rate(currency):
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    data = requests.get(url).json()
    for item in data:
        if item["Ccy"] == currency:
            return item["Rate"]
    return None

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("USD", "EUR", "RUB")
    markup.add("💳 To'lov qilish")
    bot.send_message(
        message.chat.id,
        "Xush kelibsiz!\nQuyidagi tugmalardan foydalaning:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: True)
def handler(message):
    text = message.text.upper()
    if text in ["USD", "EUR", "RUB"]:
        rate = get_rate(text)
        bot.reply_to(message, f"{text} kursi: {rate} so'm")
    elif "TO'LOV" in text or "TOLOV" in text:
        bot.reply_to(message, "To'lov qilish uchun:\n1. Click/Payme oching.\n2. Pul yuboring.\n3. Screenshot yuboring.")
    else:
        bot.reply_to(message, "USD, EUR, RUB yoki To'lov tugmasini tanlang.")

# Webhook endpoint
@app.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/", methods=["GET"])
def index():
    return "Bot is running", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
