from flask import render_template,Blueprint,flash,redirect,url_for,request
from flask_login import login_required,current_user,logout_user
from pariksha.models import Quiz,Quiz_Questions
from pariksha import db
import datetime

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
    return render_template('teacher_input.html',title = 'Create Quiz')


@teacher.route("/create_new_quiz", methods = ['POST'])
@login_required
def create_new_quiz_post():
    current_teacher = current_user.teacher
    response = request.form
    no_of_questions = len(response)/6
    total_marks = 0
    start_time = response['start_time']
    end_time = response['end_time']
    start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d')
    end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d')
    end_time += datetime.timedelta(seconds=24*60*60 - 1)


    quiz = Quiz(title = response['title'],start_time = start_time, end_time = end_time, teacher_id = current_teacher.id)
    for num in range(1,int(no_of_questions)+1):
        total_marks += int(response['Marks'+str(num)])
        question = Quiz_Questions(question_desc = response['Question'+str(num)] , option_1 = response['Option'+str(num)+'A'], option_2 = response['Option'+str(num)+'B'], option_3 = response['Option'+str(num)+'C'], option_4 = response['Option'+str(num)+'D'], marks = int(response['Marks'+str(num)]))
        question.quiz = quiz
        db.session.add(question)
    
    quiz.marks = total_marks
    db.session.add(quiz)
    db.session.commit()

    flash('The Quiz has been created', 'success')
    return redirect(url_for('teacher.home'))

@teacher.route('/activate_quizzes')
@login_required
def activate_quizzes():
    if current_user.teacher is None:
        flash('Access Denide','danger')
        return redirect(url_for('student.home'))
    return "HOLA"


@teacher.route('/view_performance')
@login_required
def view_performance():
    if current_user.teacher is None:
        flash('Access Denide','danger')
        return redirect(url_for('student.home'))
    teacher = current_user.teacher
    quiz_list = list(teacher.quiz_created) 
    quiz_exists = bool(len(quiz_list))
    return render_template('quiz_list_teacher.html',title = 'View Performace', quiz_list = quiz_list, quiz_exists = quiz_exists)

@teacher.route('/view_performance/<int:quiz_id>')
@login_required
def view_performance_quiz(quiz_id):
    if current_user.teacher is None:
        flash('Access Denide','danger')
        return redirect(url_for('student.home'))
    quiz = Quiz.query.filter_by(id = quiz_id).first_or_404()
    teacher = current_user.teacher
    marks = list(db.session.execute(f'SELECT student_id,marks FROM submits_quiz WHERE quiz_id = {quiz_id}'))

    





    
    
    

