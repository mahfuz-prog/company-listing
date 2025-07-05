import json

with open('config.json', 'r') as f:
# with open('/etc/config.json', 'r') as f:
	conf = json.load(f)

class Config():
	SECRET_KEY = conf.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = conf.get('SQLALCHEMY_DATABASE_URI')
	ADMIN_EMAIL = conf.get('ADMIN_EMAIL')
	SERVER_ADDR = conf.get('SERVER_ADDR')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAX_CONTENT_LENGTH = 2 * 1024 * 1024

	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USERNAME = conf.get('MAIL_USERNAME') 	#email
	MAIL_PASSWORD = conf.get('MAIL_PASSWORD')	#app password
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True