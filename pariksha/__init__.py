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

    from pariksha.user.routes import user
    from pariksha.main.routes import main
    from pariksha.auth.routes import auth


    app.register_blueprint(user)
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app

#===================================

# from flask import Flask
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail
# from flask_bcrypt import Bcrypt



# app = Flask(__name__)

# db = SQLAlchemy(app)

# login_manager = LoginManager(app)
# login_manager.login_message_category = "info"
# login_manager.login_view = "auth.login"

# mail = Mail(app)

# bcrypt = Bcrypt(app)

# from user.routes import user
# from main.routes import main
# from auth.routes import auth
# from config import Config

# app.config.from_object(Config)
# app.register_blueprint(user)
# app.register_blueprint(main)
# app.register_blueprint(auth)

# if __name__ == "__main__":
#     app.run(debug=True)
