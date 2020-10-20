class Config():
    SECRET_KEY = "7c9270027a164800f09e52vb828q1384523667f"
    #change if not using gmail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    #mail port info ends

    #add email and password 
    MAIL_USERNAME = "pariksha.contact@gmail.com"
    MAIL_PASSWORD = "pycavmail"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"