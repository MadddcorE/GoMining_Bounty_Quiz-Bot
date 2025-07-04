@app.route("/stats/<username>")
def stats(username):
    user = User.query.filter_by(username=username).first()
    stats = {
        "total_questions": len(user.answers),
        "correct": sum(1 for a in user.answers if a.correct),
        "avg_time": round(sum(a.response_time for a in user.answers) / len(user.answers), 2)
    }
    return render_template("stats.html", stats=stats, user=user)
