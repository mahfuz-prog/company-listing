from flaskapp import mail
from flask_mail import Message
from flask import current_app

# send signup email verification token
def signup_email_verification(token, email):
	msg = Message('Create account email confirmation - WebWaymark', sender='noreply@webwaymark.com', recipients=[email])
	msg.body = f'''To confirm your email, visit the following link:
{current_app.config.get("SERVER_ADDR")}/verify-email/{token}. This link will expire after 20 minutes.

If you did not make this request then simply ignore this email and no account will be created.
'''
	try:
		mail.send(msg)
		return True
	except Exception as e:
		return False


# password reset email verification token send
def password_reset_varification(token, email):
	msg = Message('Reset password - WebWaymark', sender='noreply@webwaymark.com', recipients=[email])
	msg.body = f'''To reset your password visit the following link:
{current_app.config.get("SERVER_ADDR")}/verify-reset/{token}. This link will expire after 20 minutes.

If you did not make this request then simply ignore this email and no changes will be made.
'''
	try:
		mail.send(msg)
		return True
	except Exception as e:
		return False