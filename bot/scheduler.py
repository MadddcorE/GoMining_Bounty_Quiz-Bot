from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from threading import Timer
from database import store_answer

active_timers = {}

def send_question(update, context):
    question = "Was ist die Hauptstadt von Frankreich?"
    answers = ["Berlin", "Paris", "Rom", "Madrid"]
    correct_index = 1

    keyboard = [
        [InlineKeyboardButton(a, callback_data=f"answer:{i}")]
        for i, a in enumerate(answers)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = update.message.reply_text(question, reply_markup=reply_markup)

    chat_id = update.message.chat_id
    message_id = msg.message_id

    def timeout():
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"{question}\n⏰ Zeit abgelaufen!",
        )

    t = Timer(15.0, timeout)
    active_timers[chat_id] = t
    t.start()
