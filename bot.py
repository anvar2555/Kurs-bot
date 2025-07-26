import telebot
import requests
from telebot import types

API_TOKEN = "8367337009:AAHRoZtirygSX5lELeKYmUm461znP0LoPak"  # BotFather bergan token

bot = telebot.TeleBot(API_TOKEN)

# Valyuta kursini olish funksiyasi
def get_rate(currency):
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    data = requests.get(url).json()
    for item in data:
        if item["Ccy"] == currency:
            return item["Rate"]
    return None

# Start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("USD", "EUR", "RUB")
    markup.add("💳 To'lov qilish")
    bot.send_message(
        message.chat.id,
        "Xush kelibsiz!\nQuyidagi tugmalardan foydalaning:",
        reply_markup=markup
    )

# Xabarlarni qayta ishlash
@bot.message_handler(func=lambda m: True)
def handler(message):
    text = message.text.upper()

    if text == "USD" or text == "EUR" or text == "RUB":
        rate = get_rate(text)
        bot.reply_to(message, f"{text} kursi: {rate} so'm")

    elif "TO'LOV" in text or "TOLOV" in text:
        # To'lov bo'limi
        bot.reply_to(
            message,
            "To'lov qilish uchun quyidagilarni bajaring:\n\n"
            "1. Click yoki Payme ilovasini oching.\n"
            "2. Bizning hisob raqamimizga pul yuboring.\n"
            "3. To'lov qilinganidan keyin screenshotni yuboring."
        )
        # Keyinchalik bu joyga to‘liq API orqali to‘lov integratsiyasi qo‘shiladi.

    else:
        bot.reply_to(message, "USD, EUR, RUB yoki To'lov tugmasini tanlang.")

# Botni ishga tushirish
bot.polling(none_stop=True, interval=0, timeout=20)
