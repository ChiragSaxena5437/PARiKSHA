from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from pariksha.config import Config

mail = Mail()
bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_message_category = "info"
login_manager.login_view = "auth.login"



def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)

    from pariksha.main.routes import main
    from pariksha.auth.routes import auth
    from pariksha.student.routes import student
    from pariksha.teacher.routes import teacher

    #extra blueprint to be removed before production 
    from pariksha.extra.routes import extra
    app.register_blueprint(extra)


    app.register_blueprint(student)
    app.register_blueprint(teacher)
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app

