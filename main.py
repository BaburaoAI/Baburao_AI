import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from flask import Flask
import threading
import os

# 🔹 API Keys from Environment Variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# 🔹 Check if API keys are set
if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Please set TELEGRAM_BOT_TOKEN and OPENAI_API_KEY as environment variables.")

# 🔹 Set OpenAI API Key
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
