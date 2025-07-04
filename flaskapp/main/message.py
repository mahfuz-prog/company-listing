from flaskapp import mail
from flask_mail import Message
from flask import current_app

def contact_us_email(subject, email, name, description):
	sender_email = current_app.config.get('MAIL_USERNAME')
	msg = Message(subject, sender=sender_email, recipients=[email, sender_email])
	msg.body = f'''Name: {name}
Description: {description}

Thanks for connecting with WebWaymark. We’ll get back to you as soon as we can.
'''
	try:
		mail.send(msg)
		return True
	except Exception as e:
		return False