from flask import Flask
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flaskapp.config import Config
from itsdangerous.url_safe import URLSafeTimedSerializer

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "users.sign_in"
login_manager.login_message = u"Login required! Please login and try again."
login_manager.login_message_category = 'info'

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	mail.init_app(app)
	login_manager.init_app(app)

	from flaskapp.main.routes import main
	from flaskapp.companies.routes import companies
	from flaskapp.posts.routes import posts
	from flaskapp.users.routes import users
	from flaskapp.admin.routes import admin
	from flaskapp.errors.handlers import errors

	app.register_blueprint(main, url_prefix='')
	app.register_blueprint(companies, url_prefix='/companies')
	app.register_blueprint(posts, url_prefix='/blog')
	app.register_blueprint(users, url_prefix='')
	app.register_blueprint(admin, url_prefix='/admin')
	app.register_blueprint(errors, url_prefix='')

	return app