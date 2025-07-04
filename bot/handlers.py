from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from threading import Timer
from database.models import Session, User, Question, Answer
import random

timers = {}

def start_quiz(update, context):
    user_id = update.effective_user.id
    username = update.effective_user.username or f"user_{user_id}"
    session = Session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    if not user:
        user = User(telegram_id=user_id, username=username)
        session.add(user)
        session.commit()
    send_question(update, context, user)

def send_question(update, context, user):
    session = Session()
    question = random.choice(session.query(Question).all())
    answers = question.answers
    keyboard = [
        [InlineKeyboardButton(ans.text, callback_data=f"answer:{ans.id}:{question.id}")]
        for ans in answers
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = context.bot.send_message(
        chat_id=user.telegram_id,
        text=question.text,
        reply_markup=reply_markup
    )

    def timeout():
        context.bot.edit_message_text(
            chat_id=user.telegram_id,
            message_id=message.message_id,
            text=f"{question.text}\n⏰ Zeit abgelaufen!",
        )

    t = Timer(15.0, timeout)
    timers[user.telegram_id] = t
    t.start()

def handle_answer(update, context):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    data = query.data.split(":")
    answer_id = int(data[1])
    question_id = int(data[2])

    if user_id in timers:
        timers[user_id].cancel()

    session = Session()
    answer = session.query(Answer).filter_by(id=answer_id).first()
    text = "✅ Richtig!" if answer.correct else "❌ Falsch."
    query.edit_message_text(f"{answer.question.text}\n{text}")