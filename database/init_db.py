from database.models import Base, engine, Session, Question, Answer

Base.metadata.create_all(engine)
session = Session()

if not session.query(Question).first():
    q1 = Question(text="Was ist die Hauptstadt von Frankreich?")
    q1.answers = [
        Answer(text="Berlin", correct=False),
        Answer(text="Paris", correct=True),
        Answer(text="Rom", correct=False),
        Answer(text="Madrid", correct=False)
    ]
    session.add(q1)
    session.commit()
    print("Beispielfrage hinzugefügt.")