from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    answers = relationship("UserAnswer", back_populates="user")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    correct = Column(Boolean)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="answers")

class UserAnswer(Base):
    __tablename__ = "user_answers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    answer_id = Column(Integer, ForeignKey("answers.id"))
    correct = Column(Boolean)
    user = relationship("User", back_populates="answers")