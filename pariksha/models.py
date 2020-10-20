from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from pariksha import db,login_manager
from flask import current_app
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#----------------------------------Users-----------------------------------------------

class User(db.Model,UserMixin):

    id = db.Column(db.Integer,
        primary_key = True)
    
    name = db.Column(db.String(20),
        nullable = False)

    email = db.Column(db.String(50),
        unique = True,
        nullable = False)

    password = db.Column(db.String(50),
        nullable = False)

    
    verified = db.Column(db.Boolean,
        nullable = False,
        default = False)

    student = db.relationship('Student',
        backref = 'user',
        uselist = False)

    teacher = db.relationship('Teacher',
        backref = 'user',
        uselist = False)
    
    def get_reset_token(self,expire_sec = 600):
        s = Serializer(current_app.config["SECRET_KEY"],expire_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")
    
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']    
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User {self.id}, {self.name}, {self.email}, {self.password}"


class Student(db.Model):
    id = db.Column(db.Integer,
        primary_key = True)
    
    user_id = db.Column(db.Integer,
         db.ForeignKey('user.id'))

    submitted_assignment = db.relationship('Assignment',
        secondary = 'submits_assign',
        backref = db.backref('submitted_by', lazy = 'dynamic'))

    submitted_quiz = db.relationship('Quiz',
        secondary = 'submits_quiz',
        backref = db.backref('submitted_by', lazy = 'dynamic'))

class Teacher(db.Model):
    id = db.Column(db.Integer,
        primary_key = True)
    
    user_id = db.Column(db.Integer,
         db.ForeignKey('user.id'))
    
    assignment_created = db.relationship('Assignment',
        backref = 'created_by')

    quiz_created = db.relationship('Quiz',
        backref = 'created_by')
    
    students = db.relationship('Student',
        secondary = 'teaches',
        backref = db.backref('taught_by', lazy = 'dynamic'))
    

teaches = db.Table('teaches',
    db.Column('student_id',db.Integer, db.ForeignKey('student.id')),
    db.Column('teacher_id',db.Integer, db.ForeignKey('teacher.id')))

#-----------------------------------------------Assignment-----------------------------------------------

class Assignment(db.Model):
    id = db.Column(db.Integer,
        primary_key = True)

    title = db.Column(db.String(30),
        nullable = False)
    
    start_time = db.Column(db.DateTime,
        nullable = False)

    end_time = db.Column(db.DateTime,
        nullable = False)

    time_created = db.Column(db.DateTime,
        nullable = False,
        default = datetime.now)

    teacher_id = db.Column(db.Integer,
        db.ForeignKey('teacher.id'))
        
    marks = db.Column(db.Integer)

    questions = db.relationship('Assignment_Questions',
        backref = 'assignment')



class Assignment_Questions(db.Model):
    id = db.Column(db.Integer,
        primary_key = True)
    
    question_desc = db.Column(db.String(700),
        nullable = False)

    marks = db.Column(db.Integer)
    
    photo_uri = db.String(db.String(30))

    option_1 = db.Column(db.String(400),
        nullable = False)

    option_2 = db.Column(db.String(400),
        nullable = False)
    
    option_3 = db.Column(db.String(400),
        nullable = False)
    
    option_4 = db.Column(db.String(400),
        nullable = False)

    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))


# Subnmit_Table
submits_assign = db.Table('submits_assign',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('assignment_id', db.Integer, db.ForeignKey('assignment.id')),
    db.Column('time_submitted', db.DateTime, nullable = False, default = datetime.now),
    db.Column('marks', db.Integer))

#-----------------------------------------------Quiz-----------------------------------------------

class Quiz(db.Model):
    id = db.Column(db.Integer,
        primary_key = True)

    title = db.Column(db.String(30),
        nullable = False)
    
    start_time = db.Column(db.DateTime,
        nullable = False)

    end_time = db.Column(db.DateTime,
        nullable = False)

    active = db.Column(db.Boolean,
        nullable = False,
        default = False)

    time_created = db.Column(db.DateTime,
        nullable = False,
        default = datetime.now)

    teacher_id = db.Column(db.Integer,
        db.ForeignKey('teacher.id'))
        
    marks = db.Column(db.Integer)

    questions = db.relationship('Quiz_Questions',
        backref = 'quiz')



class Quiz_Questions(db.Model):
    id = db.Column(db.Integer,
        primary_key = True)
    
    question_desc = db.Column(db.String(700),
        nullable = False)

    marks = db.Column(db.Integer)
    
    photo_uri = db.String(db.String(30))

    option_1 = db.Column(db.String(400),
        nullable = False)

    option_2 = db.Column(db.String(400),
        nullable = False)
    
    option_3 = db.Column(db.String(400),
        nullable = False)
    
    option_4 = db.Column(db.String(400),
        nullable = False)

    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))


# Submits_Quiz
submits_quiz = db.Table('submits_quiz',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('quiz_id', db.Integer, db.ForeignKey('quiz.id')),
    db.Column('time_submitted', db.DateTime, nullable = False, default = datetime.now),
    db.Column('marks', db.Integer))









