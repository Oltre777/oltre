import os
from flask import Flask, request
import telebot

# ====== 1. КЛЮЧИ И ФАЙЛЫ ======
TOKEN        = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_KEY   = os.environ["OPENAI_API_KEY"]
PDF_PATH     = "HomeAlanya_Bot_Knowledge_RU.pdf"
VECTOR_DIR   = "chroma_db"

# ====== 2. AI-БИБЛИОТЕКИ ======
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter     import RecursiveCharacterTextSplitter
from langchain.vectorstores      import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains            import RetrievalQA
from langchain.chat_models       import ChatOpenAI

# ====== 3. ИНИЦИАЛИЗАЦИЯ ======
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
os.environ["OPENAI_API_KEY"] = OPENAI_KEY

# Загружаем PDF в память
loader   = PyPDFLoader(PDF_PATH)
pages    = loader.load()
chunks   = RecursiveCharacterTextSplitter(
              chunk_size=700, chunk_overlap=100
          ).split_documents(pages)
vectordb = Chroma.from_documents(
              chunks, OpenAIEmbeddings(), persist_directory=VECTOR_DIR)
retriever = vectordb.as_retriever()

qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
        retriever=retriever)

# ====== 4. WEBHOOK ДЛЯ TELEGRAM ======
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def index():
    return "Бот работает!"

# ====== 5. ОБРАБОТКА СООБЩЕНИЙ ======
@bot.message_handler(commands=["start"])
def greet(m):
    msg = (
        "Здравствуйте! Я бот Home Alanya.\n"
        "Я помогу вам с:\n"
        "— покупкой недвижимости\n"
        "— оформлением ВНЖ/гражданства\n"
        "— переводами и юридической поддержкой\n"
        "Напишите вопрос или выберите тему."
    )
    bot.send_message(m.chat.id, msg)

@bot.message_handler(func=lambda _: True)
def answer(m):
    reply = qa.run(m.text)
    if "I don't know" in reply or reply.strip() == "":
        reply = (
            "К сожалению, у меня нет точного ответа.\n"
            "Я передам ваш вопрос специалисту. "
            "Пожалуйста, оставьте номер телефона 📞"
        )
    bot.send_message(m.chat.id, reply)

# ====== 6. ЗАПУСК ======
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://ha-telegram-bot.onrender.com/{TOKEN}")
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
