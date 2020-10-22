from flask import render_template,Blueprint
from flask_login import login_required,current_user,logout_user

teacher = Blueprint('teacher',__name__,url_prefix="/teacher",template_folder='templates')

@teacher.route('/home')
@login_required
def home():
    if current_user.teacher is None:
        logout_user()
        #return error page ERROR 403
        return "unauthorized acess attempted you have been logged out"
    return render_template('teacher_home.html',title = 'Home')
