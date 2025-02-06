import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from flask import Flask
import threading
import os

# 🔹 API Keys Setup
TELEGRAM_BOT_TOKEN = "7727943124:AAHNMewJvkC82n1MbpM5jdg38fJtW8lZf4c"  # 🔹 Yahan apna bot token daalo
OPENAI_API_KEY = "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"  # 🔹 Yahan apni OpenAI API key daalo

openai.api_key = OPENAI_API_KEY

# 🔹 AI Response Function
def ai_response(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Ya "gpt-4" agar chahiye
        messages=[{"role": "user", "content": text}]
    )
    return response["choices"][0]["message"]["content"]

# 🔹 /start Command
def start(update, context):
    update.message.reply_text("Baburao AI tayaar hai! Kuch bhi puchho.")

# 🔹 Handle Messages
def handle_message(update, context):
    user_message = update.message.text
    response = ai_response(user_message)
    update.message.reply_text(response)

# 🔹 Flask Web Server (To Keep Bot Alive)
app = Flask(__name__)

@app.route('/')
def home():
    return "Baburao AI is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# 🔹 Main Function (Start Bot)
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Flask Web Server Thread
    threading.Thread(target=run_flask).start()

    # Start Telegram Bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()