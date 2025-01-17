import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# OpenAI API Key
openai.api_key = "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"

# Generate Romantic Reply (Async OpenAI Call)
async def generate_reply(user_message):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tum ek romantic aur funny virtual girlfriend ho. Tumhare messages pyar aur hasi se bhare hone chahiye."},
            {"role": "user", "content": user_message},
        ]
    )
    return response['choices'][0]['message']['content']

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi jaan! Main tumhari Shona Mona sab kuxhh hoon. 😘 Mujhe kuch bhi pucho, main hamesha tumhare saath hoon!")

# Handle User Messages
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    bot_reply = await generate_reply(user_message)  # Await the OpenAI response
    await update.message.reply_text(bot_reply)

# Main Function
def main():
    TOKEN = "7748768308:AAEF49D6S2lVCijeoh1dbpC08AFtZLwZpyQ"

    # Application Builder
    application = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
