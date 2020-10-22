from flask import render_template,Blueprint,redirect,url_for
from flask_login import login_required,current_user,logout_user
import random

student = Blueprint("student",__name__,url_prefix="/student" ,template_folder="templates",static_folder="static")

@student.route("/home")
@login_required
def home():
    quotes = ["Let us study things that are no more. It is necessary to understand them, if only to avoid them.","The authority of those who teach is often an obstacle to those who want to learn","To acquire knowledge, one must study; but to acquire wisdom, one must observe."]
    random.shuffle(quotes)
    if current_user.student is None:
        logout_user()
        #return error page ERROR 403
        return "unauthorized acess attempted you have been logged out"
    return render_template("student_home.html",quotes = quotes, title = "Home")

@student.route("/quiz")
def quiz():
    questions = [x for x in range(10)]
    return render_template('quiz.html', questions = questions)