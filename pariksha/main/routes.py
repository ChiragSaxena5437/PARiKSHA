from flask import render_template,redirect,Blueprint,url_for
from flask_login import current_user

main = Blueprint("main",__name__,template_folder="templates",static_folder="static")

@main.route("/")
def welcome():
    if current_user.is_authenticated == False:
        return render_template("welcome.html",title = "Welcome")
    else:
        if current_user.student is not None:
            return redirect(url_for('student.home'))
        else:
            return redirect(url_for('teacher.home'))
