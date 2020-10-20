from flask import render_template,Blueprint,redirect,url_for
from flask_login import login_required,current_user,logout_user

student = Blueprint("student",__name__,url_prefix="/student" ,template_folder="templates",static_folder="static")

@student.route("/home")
@login_required
def home():
    if current_user.student is None:
        logout_user()
        #return error page ERROR 403
        return "unauthorized acess attempted you have been logged out"
    return render_template("student_home.html")