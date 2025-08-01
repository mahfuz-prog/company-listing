from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flaskapp.posts.db_models import Post, PostCategory
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms import StringField, TextAreaField, SubmitField, BooleanField

# create new post form
class NewPost(FlaskForm):
	featured_img = FileField('Featured image', validators=[FileAllowed(['jpg', 'png'], 'Images only! jpg, png')])
	title = StringField('Title', validators=[DataRequired(), Length(min=20, max=100)])
	excerpt = StringField('Excerpt', validators=[DataRequired(), Length(min=20, max=200)])
	description = TextAreaField('Description', validators=[DataRequired()])
	option = BooleanField('Option')
	submit = SubmitField('Add new post')

	def validate_featured_img(self, featured_img):
		if not featured_img.data:
			raise ValidationError('Featured image required')

	def validate_title(self, title):
		title_ = title.data.lower().replace(' ', '-')
		post = Post.query.filter_by(title=title_).first()
		if post:
			raise ValidationError('This title already taken')

	def validate_excerpt(self, excerpt):
		post = Post.query.filter_by(excerpt=excerpt.data).first()
		if post:
			raise ValidationError('Excerpt already taken!')

	def validate_description(self, description):
		post = Post.query.filter_by(description=description.data).first()
		if post:
			raise ValidationError('This description already taken')
	
	def validate_option(self, option):
		if not option.data:
			raise ValidationError('Please select a category')

# edit post form
class EditPost(FlaskForm):
	featured_img = FileField('Featured image', validators=[FileAllowed(['jpg', 'png'], 'Images only! jpg, png')])
	title = StringField('Title', validators=[DataRequired(), Length(min=20, max=100)])
	excerpt = StringField('Excerpt', validators=[DataRequired(), Length(min=20, max=200)])
	description = TextAreaField('Description', validators=[DataRequired()])
	remove_category = BooleanField('remove_category')
	add_category = BooleanField('add_category')
	submit = SubmitField('Update post')

	def __init__(self, id=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.id = int(id)

	def validate_title(self, title):
		title_ = title.data.lower().replace(' ', '-')
		post = Post.query.filter_by(title=title_).first()
		if post and post.id != self.id:
			raise ValidationError('This title already taken')

	def validate_excerpt(self, excerpt):
		post = Post.query.filter_by(excerpt=excerpt.data).first()
		if post and post.id != self.id:
			raise ValidationError('Excerpt already taken!')

	def validate_description(self, description):
		post = Post.query.filter_by(description=description.data).first()
		if post and post.id != self.id:
			raise ValidationError('This description already taken')


# create post category form
class NewCategory(FlaskForm):
	category_name = StringField('Category name', validators=[DataRequired(), Length(min=3, max=50)])
	submit_add = SubmitField('Add new category')

	def validate_category_name(self, category_name):
		cat = category_name.data.replace(' ', '-').lower()
		cat = PostCategory.query.filter_by(category_name=cat).first()

		if cat:
			raise ValidationError('Category already exist')

# delete post category form
class DeleteCategory(FlaskForm):
	category_name = StringField('Category name', validators=[DataRequired(), Length(min=3, max=50)])
	submit_delete = SubmitField('Delete category')

	def validate_category_name(self, category_name):
		cat = category_name.data.replace(' ', '-').lower()
		cat = PostCategory.query.filter_by(category_name=cat).first()

		if not cat:
			raise ValidationError('Category does not exist')
