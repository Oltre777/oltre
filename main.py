import telebot
from flask import Flask, request

API_TOKEN = '7410532517:AAFM0X4ibp3-9ahQs2bkaZnGwkIZp2mb1t4'

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, развернутый на Render. 😊")

@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return '', 200

@app.route("/", methods=["GET"])
def index():
    return "Бот работает!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
