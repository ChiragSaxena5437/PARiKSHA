from flask import url_for
from pariksha import mail
from flask_mail import Mail,Message


def send_verification_email(user):
    token = user.get_reset_token()
    message = Message("Verify PARiKSHA Account",
        sender = "PARiKSHA<vibhu.upamanyu@gmail.com>",
        recipients=[user.email])
    message.body = f''' To verify you PARiKSHA account please click on the link given below:
{url_for('auth.verify', token = token, _external=True )}

If you did not make this requet please ignore.
'''
    mail.send(message)

def send_reset_email(user):
    token = user.get_reset_token()
    message = Message("Reset Password",
        sender = "PARiKSHA<pariksha.contact@gmail.com>",
        recipients=[user.email])
    message.body = f''' To reset your password visit the link:
{url_for('auth.reset_password', token = token, _external=True )}

If you did not make this requet please ignore.
'''
    mail.send(message)