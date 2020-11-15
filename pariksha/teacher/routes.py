from flask import render_template,Blueprint,flash,redirect,url_for,request,send_from_directory
from flask_login import login_required,current_user,logout_user
from pariksha.models import Quiz,Quiz_Questions,Student
from pariksha import db
import datetime
import csv
import os

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
    return render_template('create_quiz.html',title = 'Create Quiz')


@teacher.route("/create_new_quiz", methods = ['POST'])
@login_required
def create_new_quiz_post():
    current_teacher = current_user.teacher
    response = request.form
    no_of_questions = int((len(response)-3)/6)
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


@teacher.route('/activate_quiz_list')
@login_required
def activate_quiz_list():
    if current_user.teacher is None:
        flash('Access Denide','danger')
        return redirect(url_for('student.home'))
    teacher = current_user.teacher
    quiz_list = list(teacher.quiz_created)
    quiz_list = [quiz for quiz in quiz_list if quiz.start_time <= datetime.datetime.now() <= quiz.end_time]
    quiz_exists = bool(len(quiz_list))
    return render_template('quiz_list_activate.html',title = 'Activate Quiz', quiz_list = quiz_list, quiz_exists = quiz_exists)


@teacher.route('/activate_quiz/<int:quiz_id>')
@login_required
def activate_quiz(quiz_id):
    if current_user.teacher is None:
        flash('Access Denide','danger')
        return redirect(url_for('student.home'))
    teacher = current_user.teacher
    quiz = Quiz.query.filter_by(id = quiz_id).first_or_404()
    if quiz.teacher_id == teacher.id:
        quiz.active ^= 1
        db.session.commit()
        return redirect(url_for('teacher.activate_quiz_list'))
    else:
        return redirect(url_for('teacher.home'))

@teacher.route('/view_performance_list')
@login_required
def view_performance_list():
    if current_user.teacher is None:
        flash('Access Denied','danger')
        return redirect(url_for('student.home'))
    teacher = current_user.teacher
    quiz_list = list(teacher.quiz_created) 
    quiz_exists = bool(len(quiz_list))
    return render_template('quiz_list_teacher.html',title = 'View Performace', quiz_list = quiz_list, quiz_exists = quiz_exists)

@teacher.route('/view_performance/<int:quiz_id>', methods = ['POST','GET'])
@login_required
def view_performance(quiz_id):
    if current_user.teacher is None:
        flash('Access Denide','danger')
        return redirect(url_for('student.home'))
    quiz = Quiz.query.filter_by(id = quiz_id).first_or_404()
    teacher = current_user.teacher
    marks = list(db.session.execute(f'SELECT student_id,marks FROM submits_quiz WHERE quiz_id = {quiz_id}'))
    data = list()
    for i,entry in enumerate(marks):
        student_name = Student.query.filter_by(id = entry[0]).first().user.name
        data_entry = dict()
        data_entry['sr_no'] = i+1
        data_entry['student_id'] = entry[0]
        data_entry['student_name'] = student_name
        data_entry['marks'] = entry[1]
        data.append(data_entry)
    data_exists = bool(len(data))
    if request.method == 'POST':
        path = os.getcwd() + f'/pariksha/results/{quiz.title}_results.csv'
        try:
            with open(path,'w',newline='',encoding='utf-8') as file:
                field_names = list(data[0])
                writer = csv.DictWriter(file, fieldnames = field_names)
                writer.writeheader()
                for entry in data:
                    writer.writerow(entry)
            return send_from_directory(directory='results', filename=f'{quiz.title}_results.csv', as_attachment = True)
        except IOError:
            flash('Downloading Error Occured','warning')
            return redirect(url_for('teacher.home'))
    else:
        return render_template('view_quiz_performance.html',title = "View Performace", quiz_title = quiz.title, data = data)




    






    
    
    

