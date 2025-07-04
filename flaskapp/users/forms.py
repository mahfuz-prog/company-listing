from flask_wtf import FlaskForm
from flaskapp.users.utils import user_filter
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

# sign up form
class SignUp(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email address', validators=[DataRequired(), Email(), Length(min=13, max=30)])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message='Password must match')])
	submit = SubmitField('Create account')

	def validate_username(self, username):
		user = user_filter(username=username.data)
		if user:
			raise ValidationError(f'{username.data} already taken. Try different.')

	def validate_email(self, email):
		user = user_filter(email=email.data)
		if user:
			raise ValidationError(f'{email.data} already taken. Try different.')

# sign in / login form
class SignIn(FlaskForm):
	email = StringField('Email address', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')


# forget password form
class ForgotPassword(FlaskForm):
	email = StringField('Email address', validators=[DataRequired(), Email()])
	submit = SubmitField('Reset password')

	def validate_email(self, email):
		user = user_filter(email=email.data)
		if not user:
			raise ValidationError(f'Please register first!')

# set new password form
class SetNewPassword(FlaskForm):
	password = PasswordField('New password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message='Password must match')])
	submit = SubmitField('Set password')
