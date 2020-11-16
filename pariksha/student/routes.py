from flask import render_template,Blueprint,redirect,url_for,request,flash
from flask_login import login_required,current_user,logout_user
from pariksha import db
from pariksha.student.utils import shuffle,random
from pariksha.models import Student,Teacher,Quiz
from pariksha.student.utils import bar_graph
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

@student.route("/quiz/<int:quiz_id>")
@login_required
def quiz(quiz_id):
    if current_user.student is None:
        logout_user()
        return redirect(url_for('main.welcome'))
    quiz = Quiz.query.filter_by(id = quiz_id).first_or_404()
    if quiz in current_user.student.submitted_quiz:
        flash('You have already submitted this quiz!!','warning')
        return redirect(url_for('student.home'))
    teacher_id_list = [teacher.id for teacher in current_user.student.taught_by.all()]
    if quiz.teacher_id not in teacher_id_list:
        flash("You are not allowed to access the page you requested","warning")
        return redirect(url_for('student.home'))
    if not quiz.active:
        flash("The quiz you are trying to attemp is not active right now","warning")
        return redirect(url_for('student.home'))
    
    questions = quiz.questions
    orig_questions = dict()
    index = 1
    for question in questions:
        orig_questions[ str(question.question_desc)] = [str(question.option_1),str(question.option_2),str(question.option_3),str(question.option_4)]
        index += 1


    questions = copy.deepcopy(orig_questions)
    shuffled_q = shuffle(questions)

    for i in questions.keys():
        random.shuffle(questions[i])
    
    question_count = len(orig_questions)

    return render_template('quiz.html', title = quiz.title, shuffled_questions = shuffled_q , questions = questions, question_count = question_count)

@student.route("/quiz/<int:quiz_id>", methods = ["POST"])
@login_required
def quiz_post(quiz_id):

    quiz = Quiz.query.filter_by(id = quiz_id).first_or_404()
    if not quiz.active:
        flash('QUIZ NOT SUBMITTED The quiz you are trying to submit has expired','danger')
        return redirect(url_for('student.home'))
    if quiz in current_user.student.submitted_quiz:
        flash('You have already submitted this quiz!!','warning')
        return redirect(url_for('student.home'))
    questions = quiz.questions
    orig_questions = dict()
    orig_questions_marks = dict()
    for question in questions:
        orig_questions[str(question.question_desc)] = [str(question.option_1),str(question.option_2),str(question.option_3),str(question.option_4)]
        orig_questions_marks[str(question.question_desc)] = question.marks
    
    questions = copy.deepcopy(orig_questions)

    marks = 0
    for i in questions.keys():
        answered = request.form[i]
        if orig_questions[i][0] == answered:
            marks += orig_questions_marks[i]
    
    current_user.student.submitted_quiz.append(quiz)
    db.session.commit()
    db.session.execute(f'UPDATE submits_quiz SET marks = {marks} WHERE student_id = {current_user.student.id} and quiz_id = {quiz_id};')
    db.session.commit()
    flash(f'Your response for Quiz : {quiz.title} has been submitted','success')
    return redirect(url_for('student.home'))

@student.route("/list_quiz")
@login_required
def list_quiz():
    if current_user.student is None:
        flash('Access Denied','danger')
        return redirect(url_for('teacher.home'))
    teachers_lis = current_user.student.taught_by.all()
    quiz_list = [quiz for teacher in teachers_lis for quiz in teacher.quiz_created]
    quiz_list = [quiz for quiz in quiz_list if quiz.active]
    quiz_exists = bool(len(quiz_list))
    return render_template('quiz_list.html',quiz_list = quiz_list,quiz_exists = quiz_exists, title = "Quizzes")


@student.route("/view_performance")
@login_required
def view_performance():
    if current_user.student is None:
        flash('Access Denied','danger')
        return redirect(url_for('teacher.home'))
    student = current_user.student
    quiz_submitted_query = tuple(db.session.execute(f'SELECT * FROM submits_quiz WHERE student_id = {student.id};'))
    quiz_submitted = list()
    
    for quiz in quiz_submitted_query:
        quiz_title = Quiz.query.filter_by(id = quiz[1]).first().title
        all_marks = list(db.session.execute(f'SELECT marks FROM submits_quiz WHERE quiz_id = {quiz[1]}'))
        all_marks = [x[0] for x in all_marks]
        quiz_submitted.append(dict(quiz_title = quiz_title,marks = quiz[3],all_marks = all_marks ))
    graph = bar_graph(quiz_submitted)

    return render_template('view_performance.html',graph = graph, title = 'Your Performance')
   
@student.route('/view_result')
@login_required
def view_result():
    if current_user.student is None:
        flash('Access Denied','danger')
        return redirect(url_for('teacher.home'))
    student = current_user.student
    quiz_submitted_query = tuple(db.session.execute(f'SELECT * FROM submits_quiz WHERE student_id = {student.id};'))
    quiz_submitted = list()
    
    for quiz in quiz_submitted_query:
        quiz_title = Quiz.query.filter_by(id = quiz[1]).first().title
        total_marks = Quiz.query.filter_by(id = quiz[1]).first().marks
        quiz_submitted.append(dict(title = quiz_title,marks = quiz[3],total_marks = total_marks))

    quiz_exists = bool(len(quiz_submitted))
    return render_template('view_result.html',quiz_list = quiz_submitted, title = "View Result", quiz_exists = quiz_exists)



    
@student.route('/add_teacher', methods = ['GET','POST'])
@login_required
def add_teacher():
    if current_user.student is None:
        flash('Access Denied','danger')
        return redirect(url_for('teacher.home'))
    if request.method == 'GET':
        return render_template('add_teacher.html',title = 'Add Teacher')
    if request.method == 'POST':
        teacher_id = request.form['teacher_id']
        teacher = Teacher.query.filter_by(id = teacher_id).first()
        if teacher is None:
            flash(f'Teacher with teacher id {teacher_id} does not exist','danger')
            return redirect(url_for('student.add_teacher'))
        if current_user.student in teacher.students:
            flash('The teacher is already added','info')
            return redirect(url_for('student.add_teacher'))
        teacher.students.append(current_user.student)
        db.session.commit()
        flash('Teacher has been added','success')
        return redirect(url_for('student.add_teacher'))
            
        

