from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from bot.handlers import start_quiz, handle_answer
from config import TELEGRAM_TOKEN

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_quiz))
    app.add_handler(CallbackQueryHandler(handle_answer, pattern="^answer:"))
    app.run_polling()

if __name__ == "__main__":
    main()