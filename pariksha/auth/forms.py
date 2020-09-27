from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from pariksha.models import User

class LoginForm(FlaskForm):
    
    email = StringField('Email',validators=[DataRequired(),Email()])

    password = PasswordField('Password',validators=[DataRequired(), Length(min=8,max = 30)])

    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired(),Length(min=4,max=20)])

    email = StringField('Email',validators=[DataRequired(),Email()])

    password = PasswordField('Password',validators=[DataRequired(), Length(min=8,max = 30)])

    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), Length(min=8,max = 30), EqualTo('password')])

    acc_type = SelectField("Accounte Type ",choices=[("Student","Student"),("Teacher","Teacher")])

    submit = SubmitField('Sign up')

    def validate_email(self,email):
        existing_email = User.query.filter_by(email = email.data).first()
        if existing_email:
            raise ValidationError("Email belongs to another account")

class ResetPasswordForm(FlaskForm):

    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=50)])

    confirm_password = PasswordField("Confirim Password", validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Change Password")


class RequestResetForm(FlaskForm):

    email = StringField("Email", validators = [DataRequired(), Email()])

    submit = SubmitField("Continue")

    def email_validator(self,email):
        existing_email = User.query.filter_by(email = email).first()

        if existing_email is None:
            raise ValidationError("Email doesn't belong to any account")

