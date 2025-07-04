from flask import Flask, render_template
from database.models import Session, User

app = Flask(__name__)

@app.route("/stats/<username>")
def stats(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        return f"User '{username}' nicht gefunden."
    stats = {
        "total_questions": len(user.answers),
        "correct": sum(1 for a in user.answers if a.correct),
    }
    return render_template("stats.html", stats=stats, user=user)

if __name__ == "__main__":
    app.run(debug=True)