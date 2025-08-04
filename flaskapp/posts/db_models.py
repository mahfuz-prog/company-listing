from flaskapp import db
from datetime import datetime

# one to many relationship with user and post
class Post(db.Model):
	__tablename__ = 'post'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	featured_image = db.Column(db.String(), nullable=False)
	title = db.Column(db.String(100), unique=True, nullable=False)
	excerpt = db.Column(db.String(200), nullable=False)
	description = db.Column(db.Text, nullable=False)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)

	categories = db.relationship(
		'PostCategory',
		secondary='post_cat_association',
		lazy='selectin',
		backref=db.backref('posts', lazy='dynamic'),
	)

	def __repr__(self):
		return f'<Title: {self.title} | Date: {self.date_posted}>'


# categories for post
class PostCategory(db.Model):
	__tablename__ = 'post_category'
	id = db.Column(db.Integer, primary_key=True)
	category_name = db.Column(db.String(50), unique=True, nullable=False)

	def __repr__(self):
		return f'<category: {self.category_name}>'


# Association Table: Post ↔ PostCategory (many-to-many)
class PostCategoryAssociation(db.Model):
	__tablename__ = 'post_cat_association'

	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
	category_id = db.Column(db.Integer, db.ForeignKey('post_category.id'), primary_key=True)

	def __repr__(self):
		return f'<post: {self.post_id} | category: {self.category_id}>'