import os
from flask import Flask, request
import telebot

API_TOKEN = "7410532517:AAFM0X4ibp3-9ahQs2bkaZnGwkIZp2mb1t4"

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# ⬇️ ответ на /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, развернутый на Render 😊")

# ⬇️ Telegram будет слать сюда обновления
@app.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "", 200

# ⬇️ проверка, что сервер жив
@app.route("/")
def index():
    return "Бот работает!"

# ⬇️ единственный старт-блок
if __name__ == "__main__":
    # ставим вебхук
    bot.remove_webhook()
    bot.set_webhook(url=f"https://ha-telegram-bot.onrender.com/{API_TOKEN}")

    # PORT приходит от Render, иначе 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
