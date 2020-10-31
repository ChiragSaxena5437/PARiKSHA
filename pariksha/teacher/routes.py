from flask import render_template,Blueprint,flash,redirect,url_for
from flask_login import login_required,current_user,logout_user

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
    return render_template('teacherinput.html',title = Create Quiz)

@teacher.route("/create_new_quiz")
@login_required
def create_new_quiz_post():
    teacher = current_user.teacher
    

