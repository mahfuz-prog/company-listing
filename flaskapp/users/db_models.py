from datetime import datetime
from flask_login import UserMixin
from flaskapp.posts.db_models import Post
from flaskapp import db, serializer, login_manager


# login manager user loder
@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))


# user information. this table has a relationship with post table
# POST table belong from post bluprint db_models
class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)

	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

	@staticmethod
	def verify_reset(token, max_age):
		try:
			user_id = serializer.loads(token, max_age=max_age)
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f'<username: {self.username} | email: {self.email}>'


# temporary user table for signup emai verification
class UnverifiedUser(db.Model):
	__tablename__ = 'unverified_user'
	id = db.Column(db.Integer, primary_key=True)

	username = db.Column(db.String(20), unique=False, nullable=False)
	email = db.Column(db.String(50), unique=False, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

	@staticmethod
	def verify_email_token(token, max_age):
		try:
			user_id = serializer.loads(token, max_age=max_age)
		except:
			return None
		return UnverifiedUser.query.get(user_id)