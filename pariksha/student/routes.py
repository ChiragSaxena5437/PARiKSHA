from flask import render_template,Blueprint,redirect,url_for,request
from flask_login import login_required,current_user,logout_user
from pariksha.student.utils import shuffle,random
import copy



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
    
    orig_questions = {
    "Question 1 (ans is A)":["A","B","C","D"],
    "Question 2 (ans is B)":["B","A","C","D"],
    "Question 3 (ans is C)":["C","B","A","D"],
    "Question 4 (ans is D)":["D","B","C","A"],
    }

    questions = copy.deepcopy(orig_questions)
    shuffled_q = shuffle(questions)

    for i in questions.keys():
        random.shuffle(questions[i])
    
    question_count = len(orig_questions)

    return render_template('quiz.html', shuffled_questions = shuffled_q , questions = questions, title = "Quiz", question_count = question_count)

@student.route("/quiz", methods = ["POST"])
def quiz_post():

    orig_questions = {
    "Question 1 (ans is A)":["A","B","C","D"],
    "Question 2 (ans is B)":["B","A","C","D"],
    "Question 3 (ans is C)":["C","B","A","D"],
    "Question 4 (ans is D)":["D","B","C","A"],
    }

    questions = copy.deepcopy(orig_questions)
    shuffled_q = shuffle(questions)

    correct = 0
    for i in questions.keys():
        answered = request.form[i]
        if orig_questions[i][0] == answered:
            correct = correct+1
    return '<h1> Marks : '+str(correct) + '</h1>'


