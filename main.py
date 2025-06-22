import time
import telebot

bot = telebot.TeleBot("7410532517:AAFM0X4ibp3-9ahQs2bkaZnGwkIZp2mb1t4")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Привет, я работаю 24/7!")

print("Бот запущен")
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
