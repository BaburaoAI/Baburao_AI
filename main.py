        import openai
        from telegram import Update
        from telegram.ext import Application, CommandHandler, MessageHandler, filters

        # Directly set your OpenAI API key here
        openai.api_key = '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'  # Replace with your OpenAI API Key

        # Directly set your Telegram Bot Token here
        TELEGRAM_TOKEN = '7727943124:AAHNMewJvkC82n1MbpM5jdg38fJtW8lZf4c'  # Replace with your Telegram Bot Token

        # Define the /start command
        async def start(update: Update, context):
            await update.message.reply_text('Hello! I am your ChatGPT-powered bot. Ask me anything!')

        # Define a function to interact with OpenAI API (ChatGPT)
        async def chatgpt_response(update: Update, context):
            user_message = update.message.text  # Get the message text from the user

            try:
                # Call OpenAI API to get a response from GPT
                response = openai.Completion.create(
                    model="text-davinci-003",  # Or use "gpt-4" if you have access
                    prompt=user_message,
                    max_tokens=150,
                    temperature=0.7
                )

                # Extract the response from OpenAI
                gpt_message = response.choices[0].text.strip()

                # Send the GPT response back to the user
                await update.message.reply_text(gpt_message)

            except Exception as e:
                await update.message.reply_text(f"Sorry, there was an error: {str(e)}")

        # Main function to set up the bot
        def main():
            # Create the Application instance
            application = Application.builder().token(TELEGRAM_TOKEN).build()

            # Add handlers for /start and text messages
            application.add_handler(CommandHandler("start", start))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt_response))

            # Run the bot
            application.run_polling()

        if __name__ == '__main__':
            main()
