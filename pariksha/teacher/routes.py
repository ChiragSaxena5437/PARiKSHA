from flask import render_template,Blueprint,flash,redirect,url_for,request
from flask_login import login_required,current_user,logout_user
from pariksha.models import Quiz,Quiz_Questions
from pariksha import db

teacher = Blueprint('teacher',__name__,url_prefix="/teacher",template_folder='templates')

@teacher.route('/home')
@login_required
def home():
    if current_user.teacher is None:
        flash("Permission denied to access the page",'danger')
        return redirect(url_for('student.home'))
    return render_template('teacher_home.html',title = 'Home')

@teacher.route("/create_new_quiz")
@login_required
def create_new_quiz():
    if current_user.teacher is None:
        flash("Permission denied to access the page",'danger')
        return redirect(url_for('student.home'))
    return render_template('teacherinput.html',title = 'Create Quiz')

@teacher.route("/create_new_quiz")
@login_required
def create_new_quiz_post():
    current_teacher = current_user.teacher
    response = request.form
    no_of_questions = len(response)/6
    list_of_questions = dict()
    for num in range(1,int(no_of_questions)+1):
        question_key = "Question"+str(num)
        question = [ response[question_key] ,response["Option"+str(num)+"A"] ,response["Option"+str(num)+"B"] ,response["Option"+str(num)+"C"] ,response["Option"+str(num)+"D"] ]
        list_of_questions[num] = question
    return list_of_questions

    
    
    

