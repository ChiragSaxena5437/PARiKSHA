from flask import Blueprint,redirect ,render_template,url_for,flash
from flask_login import login_user,logout_user, current_user,login_required
from pariksha.auth.forms import *
from pariksha.models import User,Student,Teacher
from pariksha.auth.utils import send_reset_email,send_verification_email
from pariksha import bcrypt,db

auth = Blueprint("auth",__name__,template_folder="templates",static_folder="static")

@auth.route("/register", methods = ["POST","GET"])
def register():
    if current_user.is_authenticated == False:
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(name = form.name.data, email = form.email.data,password = hashed_password)
            if form.acc_type.data == "Student":
                student = Student(user = user)
                db.session.add(user)
                db.session.add(student)
            else:
                teacher = Teacher(user = user)
                db.session.add(user)
                db.session.add(teacher)
            db.session.commit()
            send_verification_email(user)
            flash("Your Account has been created and ready to be logged in !!", 'success')
            return redirect(url_for("main.welcome"))
        return render_template("register.html",form = form,title = "Register")

@auth.route("/login", methods=["POST","GET"])
def login():
    if current_user.is_authenticated == False:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                if user.verified:
                    if user.student is not None:
                        login_user(user, remember=False)    
                        flash("Logged in!!",'sucess')
                        return redirect(url_for('student.home'))
                    if user.teacher is not None:
                        login_user(user, remember=False)    
                        flash("Logged in!!",'sucess')
                        return redirect(url_for('teacher.home'))
                else:
                    return "verify your account"
            else:
                return "not logged in"
        return render_template("login.html",form = form, titile = "Login")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.welcome"))


@auth.route("/verify_account/<token>")
def verify(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash("The token has expired!!")
        return redirect(url_for("auth.login"))
    user.verified = True
    db.session.commit()
    flash("Your Account has been verified","success")
    return redirect(url_for("auth.login"))

@auth.route("/reset_password", methods=["GET", "POST"])
def request_reset():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            f"An email has been sent to {user.email} for changing the password", "info")
        return redirect(url_for("auth.login"))
    return render_template("request_reset.html", tilte="Reset Password", form=form)


@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash("The token is invalid or expired please try again", "danger")
        return redirect(url_for("users.request_reset"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Your account password has been changed", 'success')
        return redirect(url_for("auth.login"))
    return(render_template("reset_password.html", title="Reset Password", form=form))