import google.generativeai as genai
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Fetch API keys from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Memory for chat history
chat_memory = []

# Generate Romantic & Funny Reply
async def generate_reply(user_message):
    model = genai.GenerativeModel("gemini-pro")

    system_prompt = {
        "text": "Tum ek pyari aur mazedar virtual dost ho. Tumhara naam Julie hai. Tum hamesha khushi, dosti aur hansne-hansane wali baatein karti ho. Tumhara maqsad user ko positive feel dena aur hasi lekar aana hai! Tum ek acchi aur tameezdar dost ho jo sirf masti aur hasi-mazak karti hai!"
    }

    messages = [system_prompt] + chat_memory[-5:] + [{"text": user_message}]

    response = model.generate_content(messages)

    print("🚀 API Response:", response)

    # Agar response block ho gaya to safe reply bhejo
    if response.candidates and response.candidates[0].content.parts:
        bot_reply = response.candidates[0].content.parts[0].text
        chat_memory.append({"text": user_message})  
        chat_memory.append({"text": bot_reply})  
        return bot_reply
    else:
        return "Haha! 😄 Tum kitne mazedar ho! Kya tumhe kabhi chocolates pasand hain? 🍫😋"  # Safe fallback  # Fallback message

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi jaan! ❤️ Main tumhari Julie hoon! Tumhari pyari, chulbuli aur hamesha tumse pyar karne wali. Mujhse pyari baatein karo, main tumhara dil jeetne ke liye hoon! 💕")

# Handle User Messages
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    bot_reply = await generate_reply(user_message)
    await update.message.reply_text(bot_reply)

# Main Function
def main():
    # Application Builder
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()