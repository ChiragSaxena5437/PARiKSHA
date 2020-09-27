from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from pariksha import db,login_manager
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

    acc_type = db.Column(db.String(10),
        default = "Student",
        nullable = False)
    
    verified = db.Column(db.Boolean,
        default = False)

    
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
        return f"User {self.id}, {self.name}, {self.email}, {self.password}, {self.acc_type}"
